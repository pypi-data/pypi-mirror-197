#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
  name='onn4arg',
  version='1.0',
  description=('ONN4ARG is an ontology-aware neural network model, which employs a novel ontology-aware layer for antibiotic resistance gene prediction and classification.'),
  long_description=('ONN4ARG is an Ontology-aware Neural Network model for Antibiotic Resistance Gene (ARG) annotation predictions. It employs a novel ontology-aware layer to encourage annotation predictions satisfying the ontology rules (i.e., the ontology tree structure). It requires the Diamond and the HHblits alignment tools to run. Our source codes are available on GitHub, and our pre-built ARG database and our pre-trained model can be downloaded from Zenodo or release. ONN4ARG provides web service for fast ARG prediction.'),
  author='Yuguo Zha, Cheng Chen, Qihong Jiao, Xiaomei Zeng, Xuefeng Cui, Kang Ning',
  author_email='hugozha@hust.edu.cn',
  maintainer='Yuguo Zha',
  license='GPL-3 License',
  platforms=["all"],
  url='https://github.com/HUST-NingKang-Lab/ONN4ARG',
  packages=find_packages(),

  include_package_data = True,
  package_data={
    '': ['*.pl','*.sh','*.py'],
  },
  classifiers=[
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
  python_requires='>=3.7'
)

