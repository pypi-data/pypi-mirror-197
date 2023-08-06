#!/bin/bash

#download the model and database
echo 'Downloading started!'
wget -c https://github.com/HUST-NingKang-Lab/ONN4ARG/releases/download/v1.0.1/onn4arg-v1.0-model.tar.gz

#Decompressing files
echo 'Decompressing files'
tar zvxf onn4arg-v1.0-model.tar.gz
echo 'Done!'
