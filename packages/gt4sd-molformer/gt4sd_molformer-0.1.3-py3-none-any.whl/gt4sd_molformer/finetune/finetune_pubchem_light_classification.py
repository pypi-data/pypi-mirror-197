import logging
import os
import random
import time
from argparse import Namespace
from functools import partial
from typing import Any, Dict

import importlib_resources
import numpy as np
import pandas as pd
import pytorch_lightning as pl
import torch
import torch.nn.functional as F
from rdkit import Chem
from fast_transformers.feature_maps import GeneralizedRandomFeatures
from fast_transformers.masking import LengthMask as LM
from pytorch_lightning.loggers import TensorBoardLogger
from pytorch_lightning.utilities import seed
from sklearn.metrics import accuracy_score, auc, roc_curve
from torch import nn
from torch.utils.data import DataLoader

from .ft_args import parse_args
from .ft_rotate_attention.ft_rotate_builder import (
    RotateEncoderBuilder as rotate_builder,
)
from .ft_tokenizer.ft_tokenizer import MolTranBertTokenizer

APEX_INSTALLED: bool
try:
    from apex import optimizers

    APEX_INSTALLED = True
except ImportError:
    APEX_INSTALLED = False

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

# from pytorch_lightning.plugins.ddp_plugin import DDPPlugin
# from pytorch_lightning.plugins.sharded_plugin import DDPShardedPlugin


def normalize_smiles(smi, canonical, isomeric):
    try:
        normalized = Chem.MolToSmiles(
            Chem.MolFromSmiles(smi), canonical=canonical, isomericSmiles=isomeric
        )
    except Exception:
        normalized = None
    return normalized


class LightningModule(pl.LightningModule):
    def __init__(self, config, tokenizer):
        super(LightningModule, self).__init__()

        if type(config) is dict:
            config = Namespace(**config)

        self.config = config
        self.model_hparams = config
        self.mode = config.mode
        self.save_hyperparameters(config)
        self.tokenizer = tokenizer
        self.min_loss = {
            self.model_hparams.measure_name
            + "min_valid_loss": torch.finfo(torch.float32).max,
            self.model_hparams.measure_name + "min_epoch": 0,
        }

        # Word embeddings layer
        n_vocab, _ = len(tokenizer.vocab), config.n_embd
        # input embedding stem
        builder = rotate_builder.from_kwargs(
            n_layers=config.n_layer,
            n_heads=config.n_head,
            query_dimensions=config.n_embd // config.n_head,
            value_dimensions=config.n_embd // config.n_head,
            feed_forward_dimensions=config.n_embd,
            attention_type="linear",
            feature_map=partial(GeneralizedRandomFeatures, n_dims=config.num_feats),
            activation="gelu",
        )
        self.pos_emb = None
        self.tok_emb = nn.Embedding(n_vocab, config.n_embd)
        self.drop = nn.Dropout(config.d_dropout)
        # transformer
        self.blocks = builder.get()
        self.lang_model = self.lm_layer(config.n_embd, n_vocab)
        self.train_config = config
        # if we are starting from scratch set seeds
        #########################################
        # protein_emb_dim, smiles_embed_dim, dims=dims, dropout=0.2):
        #########################################

        self.fcs = []  # nn.ModuleList()
        self.loss = torch.nn.CrossEntropyLoss()

        self.net = self.Net(
            config.n_embd,
            self.model_hparams.num_classes,
            dims=config.dims,
            dropout=config.dropout,
        )

    class Net(nn.Module):
        dims = [150, 50, 50, 2]

        def __init__(self, smiles_embed_dim, num_classes, dims=dims, dropout=0.2):
            super().__init__()
            self.desc_skip_connection = True
            self.fcs = []  # nn.ModuleList()
            logger.info("dropout is {}".format(dropout))

            self.fc1 = nn.Linear(smiles_embed_dim, smiles_embed_dim)
            self.dropout1 = nn.Dropout(dropout)
            self.relu1 = nn.GELU()
            self.fc2 = nn.Linear(smiles_embed_dim, smiles_embed_dim)
            self.dropout2 = nn.Dropout(dropout)
            self.relu2 = nn.GELU()
            self.final = nn.Linear(smiles_embed_dim, num_classes)  # classif

        def forward(self, smiles_emb):
            x_out = self.fc1(smiles_emb)
            x_out = self.dropout1(x_out)
            x_out = self.relu1(x_out)

            if self.desc_skip_connection is True:
                x_out = x_out + smiles_emb

            z = self.fc2(x_out)
            z = self.dropout2(z)
            z = self.relu2(z)
            if self.desc_skip_connection is True:
                z = self.final(z + x_out)
            else:
                z = self.final(z)

            # z = self.layers(smiles_emb)
            return z

    class lm_layer(nn.Module):
        def __init__(self, n_embd, n_vocab):
            super().__init__()
            self.embed = nn.Linear(n_embd, n_embd)
            self.ln_f = nn.LayerNorm(n_embd)
            self.head = nn.Linear(n_embd, n_vocab, bias=False)

        def forward(self, tensor):
            tensor = self.embed(tensor)
            tensor = F.gelu(tensor)
            tensor = self.ln_f(tensor)
            tensor = self.head(tensor)
            return tensor

    def get_loss(self, smiles_emb, measures):
        z_pred = self.net.forward(smiles_emb).squeeze()
        measures = measures.long()
        # logger.info('z_pred:', z_pred.shape)
        # logger.info('measures:', measures.shape)
        return self.loss(z_pred, measures), z_pred, measures

    def on_save_checkpoint(self, checkpoint):
        # save RNG states each time the model and states are saved
        out_dict: Dict[str, Any] = dict()
        out_dict["torch_state"] = torch.get_rng_state()
        out_dict["cuda_state"] = torch.cuda.get_rng_state()
        if np:
            out_dict["numpy_state"] = np.random.get_state()
        if random:
            out_dict["python_state"] = random.getstate()
        checkpoint["rng"] = out_dict

    def on_load_checkpoint(self, checkpoint):
        # load RNG states each time the model and states are loaded from checkpoint
        rng = checkpoint["rng"]
        for key, value in rng.items():
            if key == "torch_state":
                torch.set_rng_state(value)
            elif key == "cuda_state":
                torch.cuda.set_rng_state(value)
            elif key == "numpy_state":
                np.random.set_state(value)
            elif key == "python_state":
                random.setstate(value)
            else:
                logger.info("unrecognized state")

    def _init_weights(self, module):
        if isinstance(module, (nn.Linear, nn.Embedding)):
            module.weight.data.normal_(mean=0.0, std=0.02)
            if isinstance(module, nn.Linear) and module.bias is not None:
                module.bias.data.zero_()
        elif isinstance(module, nn.LayerNorm):
            module.bias.data.zero_()
            module.weight.data.fill_(1.0)

    def configure_optimizers(self):

        if not APEX_INSTALLED:
            raise RuntimeError(
                "Apex is not installed. Molformer's training is not supported. Install Apex from source to enable training."
            )

        # separate out all parameters to those that will and won't experience regularizing weight decay
        decay = set()
        no_decay = set()
        whitelist_weight_modules = (torch.nn.Linear,)
        blacklist_weight_modules = (torch.nn.LayerNorm, torch.nn.Embedding)
        for mn, m in self.named_modules():
            for pn, p in m.named_parameters():
                fpn = "%s.%s" % (mn, pn) if mn else pn  # full param name

                if pn.endswith("bias"):
                    # all biases will not be decayed
                    no_decay.add(fpn)
                elif pn.endswith("weight") and isinstance(m, whitelist_weight_modules):
                    # weights of whitelist modules will be weight decayed
                    decay.add(fpn)
                elif pn.endswith("weight") and isinstance(m, blacklist_weight_modules):
                    # weights of blacklist modules will NOT be weight decayed
                    no_decay.add(fpn)

        if self.pos_emb is not None:
            no_decay.add("pos_emb")

        # validate that we considered every parameter
        param_dict = {pn: p for pn, p in self.named_parameters()}
        inter_params = decay & no_decay
        union_params = decay | no_decay
        assert (
            len(inter_params) == 0
        ), "parameters %s made it into both decay/no_decay sets!" % (str(inter_params),)
        assert (
            len(param_dict.keys() - union_params) == 0
        ), "parameters %s were not separated into either decay/no_decay set!" % (
            str(param_dict.keys() - union_params),
        )

        # create the pytorch optimizer object
        optim_groups = [
            {
                "params": [param_dict[pn] for pn in sorted(list(decay))],
                "weight_decay": 0.0,
            },
            {
                "params": [param_dict[pn] for pn in sorted(list(no_decay))],
                "weight_decay": 0.0,
            },
        ]
        if self.model_hparams.measure_name == "r2":
            betas = (0.9, 0.999)
        else:
            betas = (0.9, 0.99)
        logger.info("betas are {}".format(betas))
        learning_rate = self.train_config.lr_start * self.train_config.lr_multiplier
        optimizer = optimizers.FusedLAMB(optim_groups, lr=learning_rate, betas=betas)
        return optimizer

    def training_step(self, batch, batch_idx):
        idx = batch[0]
        mask = batch[1]
        targets = batch[-1]

        b, t = idx.size()
        token_embeddings = self.tok_emb(idx)  # each index maps to a (learnable) vector
        x = self.drop(token_embeddings)
        x = self.blocks(x, length_mask=LM(mask.sum(-1)))
        token_embeddings = x
        input_mask_expanded = mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
        sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        loss_input = sum_embeddings / sum_mask
        loss, pred, actual = self.get_loss(loss_input, targets)

        self.log("train_loss", loss, on_step=True)

        return {"loss": loss}

    def validation_step(self, val_batch, batch_idx, dataset_idx):
        idx = val_batch[0]
        mask = val_batch[1]
        targets = val_batch[-1]

        b, t = idx.size()
        token_embeddings = self.tok_emb(idx)  # each index maps to a (learnable) vector
        x = self.drop(token_embeddings)
        x = self.blocks(x, length_mask=LM(mask.sum(-1)))
        # input_mask_expanded = mask._mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        input_mask_expanded = mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
        sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        loss_input = sum_embeddings / sum_mask
        loss, pred, actual = self.get_loss(loss_input, targets)
        self.log("train_loss", loss, on_step=True)
        return {
            "val_loss": loss,
            "pred": pred.detach(),
            "actual": actual.detach(),
            "dataset_idx": dataset_idx,
        }

    def testing_step(self, val_batch, batch_idx, dataset_idx):
        idx = val_batch[0]
        mask = val_batch[1]

        b, t = idx.size()
        token_embeddings = self.tok_emb(idx)  # each index maps to a (learnable) vector
        x = self.drop(token_embeddings)
        x = self.blocks(x, length_mask=LM(mask.sum(-1)))
        # input_mask_expanded = mask._mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        input_mask_expanded = mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
        sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        loss_input = sum_embeddings / sum_mask

        z_pred = self.net.forward(loss_input).squeeze()

        if len(z_pred.shape) == 1:
            preds_cpu = F.softmax(z_pred.view(1, -1), dim=1).cpu().numpy()
        else:
            preds_cpu = F.softmax(z_pred, dim=1).cpu().numpy()

        return {
            "pred": preds_cpu,
        }

    def validation_epoch_end(self, outputs):
        # results_by_dataset = self.split_results_by_dataset(outputs)
        tensorboard_logs = {}
        for dataset_idx, batch_outputs in enumerate(outputs):
            dataset = self.model_hparams.dataset_names[dataset_idx]
            # logger.info("x_val_loss:", batch_outputs[0]["val_loss"])
            avg_loss = torch.stack([x["val_loss"] for x in batch_outputs]).mean()
            preds = torch.cat([x["pred"] for x in batch_outputs])
            actuals = torch.cat([x["actual"] for x in batch_outputs])
            val_loss = self.loss(preds, actuals)

            actuals_cpu = actuals.detach().cpu().numpy()
            # preds_cpu = preds.detach().cpu().numpy() #preds_cpu is logits
            preds_cpu = F.softmax(preds, dim=1).cpu().numpy()

            # classif
            preds_cpu = preds_cpu[:, 1]
            fpr, tpr, threshold = roc_curve(actuals_cpu, preds_cpu)
            roc_auc = auc(fpr, tpr)

            logger.info(f"{dataset}:rocauc: {roc_auc}")
            y_pred = np.where(preds_cpu >= 0.5, 1, 0)
            accuracy = accuracy_score(actuals_cpu, y_pred)
            tensorboard_logs.update(
                {
                    # dataset + "_avg_val_loss": avg_loss,
                    self.model_hparams.measure_name + "_" + dataset + "_loss": val_loss,
                    self.model_hparams.measure_name + "_" + dataset + "_acc": accuracy,
                    self.model_hparams.measure_name
                    + "_"
                    + dataset
                    + "_rocauc": roc_auc,
                }
            )

        if (
            tensorboard_logs[self.model_hparams.measure_name + "_valid_loss"]
            < self.min_loss[self.model_hparams.measure_name + "min_valid_loss"]
        ):
            self.min_loss[
                self.model_hparams.measure_name + "min_valid_loss"
            ] = tensorboard_logs[self.model_hparams.measure_name + "_valid_loss"]
            self.min_loss[
                self.model_hparams.measure_name + "min_test_loss"
            ] = tensorboard_logs[self.model_hparams.measure_name + "_test_loss"]
            self.min_loss[
                self.model_hparams.measure_name + "min_epoch"
            ] = self.current_epoch
            self.min_loss[
                self.model_hparams.measure_name + "max_valid_rocauc"
            ] = tensorboard_logs[self.model_hparams.measure_name + "_valid_rocauc"]
            self.min_loss[
                self.model_hparams.measure_name + "max_test_rocauc"
            ] = tensorboard_logs[self.model_hparams.measure_name + "_test_rocauc"]

        tensorboard_logs[
            self.model_hparams.measure_name + "_min_valid_loss"
        ] = self.min_loss[self.model_hparams.measure_name + "min_valid_loss"]
        tensorboard_logs[
            self.model_hparams.measure_name + "_min_test_loss"
        ] = self.min_loss[self.model_hparams.measure_name + "min_test_loss"]
        tensorboard_logs[
            self.model_hparams.measure_name + "_max_test_rocauc"
        ] = self.min_loss[self.model_hparams.measure_name + "max_test_rocauc"]
        tensorboard_logs[
            self.model_hparams.measure_name + "_max_valid_rocauc"
        ] = self.min_loss[self.model_hparams.measure_name + "max_valid_rocauc"]

        self.logger.log_metrics(tensorboard_logs, self.global_step)  # type: ignore

        for k in tensorboard_logs.keys():
            self.log(k, tensorboard_logs[k])

        logger.info(f"Validation: Current Epoch {self.current_epoch}")
        append_to_file(
            os.path.join(
                self.model_hparams.results_dir,
                "results_" + str(self.model_hparams.run_id) + ".csv",
            ),
            f"{self.model_hparams.measure_name}, {self.current_epoch},"
            + f"{tensorboard_logs[self.model_hparams.measure_name + '_valid_loss']},"
            + f"{tensorboard_logs[self.model_hparams.measure_name + '_test_loss']},"
            + f"{self.min_loss[self.model_hparams.measure_name + 'min_epoch']},"
            + f"{self.min_loss[self.model_hparams.measure_name + 'max_valid_rocauc']},"
            + f"{self.min_loss[self.model_hparams.measure_name + 'max_test_rocauc']}",
        )

        return {"avg_val_loss": avg_loss}


def get_dataset(data_root, filename, dataset_len, aug, measure_name):
    df = pd.read_csv(os.path.join(data_root, filename))
    logger.info(f"Length of dataset: {len(df)}")
    if dataset_len:
        df = df.head(dataset_len)
        logger.info(f"Warning entire dataset not used: {len(df)}")
    dataset = PropertyPredictionDataset(df, measure_name, aug)
    return dataset


class PropertyPredictionDataset(torch.utils.data.Dataset):
    def __init__(self, df, measure_name=None, tokenizer=None, aug=True):

        columns_of_interest = ["smiles"]
        if measure_name is not None:
            columns_of_interest.append(measure_name)

        df = df[columns_of_interest]
        df = df.dropna()
        self.measure_name = measure_name
        df["canonical_smiles"] = df["smiles"].apply(
            lambda smi: normalize_smiles(smi, canonical=True, isomeric=False)
        )
        df_good = df.dropna(
            subset=["canonical_smiles"]
        )  # TODO - Check why some rows are na

        len_new = len(df_good)
        logger.info("Dropped {} invalid smiles".format(len(df) - len_new))
        self.df = df_good
        self.df = self.df.reset_index(drop=True)

    def __getitem__(self, index):
        canonical_smiles = self.df.loc[index, "canonical_smiles"]

        measures = -1  # not initialized value
        if self.measure_name is not None:
            measures = self.df.loc[index, self.measure_name]
        return canonical_smiles, measures

    def __len__(self):
        return len(self.df)


class PropertyPredictionDataModule(pl.LightningDataModule):
    def __init__(self, hparams, tokenizer):
        super(PropertyPredictionDataModule, self).__init__()
        if type(hparams) is dict:
            hparams = Namespace(**hparams)
        self.model_hparams = hparams
        self.smiles_emb_size = hparams.n_embd
        self.tokenizer = tokenizer
        self.dataset_name = hparams.dataset_name

    def get_split_dataset_filename(dataset_name, split):
        return split + ".csv"

    def prepare_data(self):
        logger.info("Inside prepare_dataset")
        train_filename = PropertyPredictionDataModule.get_split_dataset_filename(
            self.dataset_name, "train"
        )

        valid_filename = PropertyPredictionDataModule.get_split_dataset_filename(
            self.dataset_name, "valid"
        )

        test_filename = PropertyPredictionDataModule.get_split_dataset_filename(
            self.dataset_name, "test"
        )

        train_ds = get_dataset(
            self.model_hparams.data_root,
            train_filename,
            self.model_hparams.train_dataset_length,
            self.model_hparams.aug,
            measure_name=self.model_hparams.measure_name,
        )

        val_ds = get_dataset(
            self.model_hparams.data_root,
            valid_filename,
            self.model_hparams.eval_dataset_length,
            aug=False,
            measure_name=self.model_hparams.measure_name,
        )

        test_ds = get_dataset(
            self.model_hparams.data_root,
            test_filename,
            self.model_hparams.eval_dataset_length,
            aug=False,
            measure_name=self.model_hparams.measure_name,
        )

        self.train_ds = train_ds
        self.val_ds = [val_ds] + [test_ds]
        self.test_ds = test_ds

        # logger.info(
        #     f"Train dataset size: {len(self.train_ds)}, val: {len(self.val_ds1), len(self.val_ds2)}, test: {len(self.test_ds)}"
        # )

    def collate(self, batch):
        tokens = self.tokenizer.batch_encode_plus(
            [smile[0] for smile in batch], padding=True, add_special_tokens=True
        )
        return (
            torch.tensor(tokens["input_ids"]),
            torch.tensor(tokens["attention_mask"]),
            torch.tensor([smile[1] for smile in batch]),
        )

    def val_dataloader(self):
        return [
            DataLoader(
                ds,
                batch_size=self.model_hparams.batch_size,
                num_workers=self.model_hparams.num_workers,
                shuffle=False,
                collate_fn=self.collate,
            )
            for ds in self.val_ds
        ]

    def train_dataloader(self):
        return DataLoader(
            self.train_ds,
            batch_size=self.model_hparams.batch_size,
            num_workers=self.model_hparams.num_workers,
            shuffle=True,
            collate_fn=self.collate,
        )

    def test_dataloader(self):
        return DataLoader(
            self.test_ds,
            batch_size=self.model_hparams.batch_size,
            num_workers=self.model_hparams.num_workers,
            shuffle=False,
            collate_fn=self.collate,
        )


class CheckpointEveryNSteps(pl.Callback):
    """
    Save a checkpoint every N steps, instead of Lightning's default that checkpoints
    based on validation loss.
    """

    def __init__(
        self,
        save_step_frequency=-1,
        prefix="N-Step-Checkpoint",
        use_modelcheckpoint_filename=False,
    ):
        """
        Args:
        save_step_frequency: how often to save in steps
        prefix: add a prefix to the name, only used if
        use_modelcheckpoint_filename=False
        """
        self.save_step_frequency = save_step_frequency
        self.prefix = prefix
        self.use_modelcheckpoint_filename = use_modelcheckpoint_filename

    def on_batch_end(self, trainer: pl.Trainer, _):
        """Check if we should save a checkpoint after every train batch"""
        epoch = trainer.current_epoch
        global_step = trainer.global_step

        if (
            global_step % self.save_step_frequency == 0
            and self.save_step_frequency > 10
        ):
            if self.use_modelcheckpoint_filename:
                filename = trainer.checkpoint_callback.filename  # type: ignore
            else:
                filename = f"{self.prefix}_{epoch}_{global_step}.ckpt"
                # filename = f"{self.prefix}.ckpt"
            ckpt_path = os.path.join(trainer.checkpoint_callback.dirpath, filename)  # type: ignore
            trainer.save_checkpoint(ckpt_path)


class ModelCheckpointAtEpochEnd(pl.Callback):
    def on_epoch_end(self, trainer, pl_module):
        metrics = trainer.callback_metrics
        metrics["epoch"] = trainer.current_epoch
        if trainer.disable_validation:
            trainer.checkpoint_callback.on_validation_end(trainer, pl_module)


def append_to_file(filename, line):
    with open(filename, "a") as f:
        f.write(line + "\n")


def main():
    margs = parse_args()
    logger.info(f"Using {torch.cuda.device_count()} GPUs")
    pos_emb_type = "rot"
    logger.info("pos_emb_type is {}".format(pos_emb_type))

    run_name_fields = [
        margs.dataset_name,
        margs.measure_name,
        pos_emb_type,
        margs.fold,
        margs.mode,
        "lr",
        margs.lr_start,
        "batch",
        margs.batch_size,
        "drop",
        margs.dropout,
        margs.dims,
    ]

    run_name = "_".join(map(str, run_name_fields))

    logger.info(run_name)

    bert_vocab_path = (
        importlib_resources.files("gt4sd_molformer") / "finetune/bert_vocab.txt"
    )

    tokenizer = MolTranBertTokenizer(bert_vocab_path)

    datamodule = PropertyPredictionDataModule(margs, tokenizer)
    margs.dataset_names = "valid test".split()
    margs.run_name = run_name

    checkpoints_folder = margs.checkpoints_folder
    checkpoint_root = os.path.join(checkpoints_folder, margs.measure_name)
    margs.checkpoint_root = checkpoint_root
    margs.run_id = np.random.randint(30000)
    os.makedirs(checkpoints_folder, exist_ok=True)
    checkpoint_dir = os.path.join(checkpoint_root, "models_" + str(margs.run_id))
    results_dir = os.path.join(checkpoint_root, "results")
    margs.results_dir = results_dir
    margs.checkpoint_dir = checkpoint_dir
    os.makedirs(results_dir, exist_ok=True)
    os.makedirs(checkpoint_dir, exist_ok=True)

    # checkpoint_path = os.path.join(checkpoints_folder, margs.measure_name)
    checkpoint_callback = pl.callbacks.ModelCheckpoint(
        every_n_epochs=1,
        save_last=True,
        dirpath=checkpoint_dir,
        filename="checkpoint",
        verbose=True,
    )

    logger.info(margs)

    tensorboard_logger = TensorBoardLogger(
        save_dir=checkpoint_root,
        # version=run_name,
        name="lightning_logs",
        default_hp_metric=False,
    )

    seed.seed_everything(margs.seed)

    if margs.seed_path == "":
        logger.info("# training from scratch")
        model = LightningModule(margs, tokenizer)
    else:
        logger.info(f"# loaded pre-trained model from {margs.seed_path}")
        model = LightningModule(margs, tokenizer).load_from_checkpoint(
            margs.seed_path,
            strict=False,
            config=margs,
            tokenizer=tokenizer,
            vocab=len(tokenizer.vocab),
        )

    last_checkpoint_file = os.path.join(checkpoint_dir, "last.ckpt")
    resume_from_checkpoint = None
    if os.path.isfile(last_checkpoint_file):
        logger.info(f"resuming training from : {last_checkpoint_file}")
        resume_from_checkpoint = last_checkpoint_file
    else:
        logger.info("training from scratch")

    trainer = pl.Trainer(
        max_epochs=margs.max_epochs,
        default_root_dir=checkpoint_root,
        gpus=1,
        logger=tensorboard_logger,
        resume_from_checkpoint=resume_from_checkpoint,
        callbacks=[checkpoint_callback],
        num_sanity_val_steps=0,
    )

    tic = time.perf_counter()
    trainer.fit(model, datamodule)
    toc = time.perf_counter()
    logger.info("Time was {}".format(toc - tic))


if __name__ == "__main__":
    main()
