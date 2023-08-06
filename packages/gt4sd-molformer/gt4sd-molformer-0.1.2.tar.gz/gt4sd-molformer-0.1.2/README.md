# GT4SD's submodule for the MolFormer model

GT4SD submodule for the MolFormer model. The original MolFormer's codebase can be found at https://github.com/IBM/molformer. 
We refer the users to the original repo for usage information and further details about the model.


### Development setup & installation

The recommended way to install the `gt4sd-molformer` is to create a dedicated conda environment, this will ensure all requirements are satisfied:

```sh
git clone https://github.com/GT4SD/gt4sd-molformer.git
cd gt4sd-molformer/
conda env create -f conda.yml
conda activate gt4sd-molformer
```
Then run:
```sh
pip install .
```

If you would like to contribute to the package, you can install the package in editable mode:
```sh
pip install -e ".[dev]" 
```

Note: In order to be able to train or finetune a model, [Apex Optimizers](https://nvidia.github.io/apex/optimizers.html) must be compiled with CUDA and C++ extensions. This can be done using the provided install_apex.sh script. 
Before executing the script, the path to the CUDA 11 installation should have been saved in the CUDA_HOME env variable. 

```
export CUDA_HOME='Cuda 11 install'
bash install_apex.sh
```


### References

If you use `MolFormer` in your projects, please consider citing the following:

```bib
@article{10.1038/s42256-022-00580-7, 
year = {2022}, 
title = {{Large-scale chemical language representations capture molecular structure and properties}}, 
author = {Ross, Jerret and Belgodere, Brian and Chenthamarakshan, Vijil and Padhi, Inkit and Mroueh, Youssef and Das, Payel}, 
journal = {Nature Machine Intelligence}, 
doi = {10.1038/s42256-022-00580-7}, 
abstract = {{Models based on machine learning can enable accurate and fast molecular property predictions, which is of interest in drug discovery and material design. Various supervised machine learning models have demonstrated promising performance, but the vast chemical space and the limited availability of property labels make supervised learning challenging. Recently, unsupervised transformer-based language models pretrained on a large unlabelled corpus have produced state-of-the-art results in many downstream natural language processing tasks. Inspired by this development, we present molecular embeddings obtained by training an efficient transformer encoder model, MoLFormer, which uses rotary positional embeddings. This model employs a linear attention mechanism, coupled with highly distributed training, on SMILES sequences of 1.1 billion unlabelled molecules from the PubChem and ZINC datasets. We show that the learned molecular representation outperforms existing baselines, including supervised and self-supervised graph neural networks and language models, on several downstream tasks from ten benchmark datasets. They perform competitively on two others. Further analyses, specifically through the lens of attention, demonstrate that MoLFormer trained on chemical SMILES indeed learns the spatial relationships between atoms within a molecule. These results provide encouraging evidence that large-scale molecular language models can capture sufficient chemical and structural information to predict various distinct molecular properties, including quantum-chemical properties. Large language models have recently emerged with extraordinary capabilities, and these methods can be applied to model other kinds of sequence, such as string representations of molecules. Ross and colleagues have created a transformer-based model, trained on a large dataset of molecules, which provides good results on property prediction tasks.}}, 
pages = {1256--1264}, 
number = {12}, 
volume = {4}
}

@misc{https://doi.org/10.48550/arxiv.2106.09553,
  doi = {10.48550/ARXIV.2106.09553},
  url = {https://arxiv.org/abs/2106.09553},
  author = {Ross, Jerret and Belgodere, Brian and Chenthamarakshan, Vijil and Padhi, Inkit and Mroueh, Youssef and Das, Payel},
  keywords = {Machine Learning (cs.LG), Computation and Language (cs.CL), Biomolecules (q-bio.BM), FOS: Computer and information sciences, FOS: Computer and information sciences, FOS: Biological sciences, FOS: Biological sciences},
  title = {Large-Scale Chemical Language Representations Capture Molecular Structure and Properties},
  publisher = {arXiv},
  year = {2021},
  copyright = {arXiv.org perpetual, non-exclusive license}
}

```

If you use `gt4sd` in your projects, please consider citing the following:

```bib
@article{manica2022gt4sd,
  title={GT4SD: Generative Toolkit for Scientific Discovery},
  author={Manica, Matteo and Cadow, Joris and Christofidellis, Dimitrios and Dave, Ashish and Born, Jannis and Clarke, Dean and Teukam, Yves Gaetan Nana and Hoffman, Samuel C and Buchan, Matthew and Chenthamarakshan, Vijil and others},
  journal={arXiv preprint arXiv:2207.03928},
  year={2022}
}
```

### License

The `gt4sd` codebase is under MIT license.
For individual model usage, please refer to the model licenses found in the original packages.
