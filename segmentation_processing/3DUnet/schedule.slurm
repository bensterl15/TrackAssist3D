#!/usr/bin/env bash

#SBATCH --job-name=C_Elegan_Results
#SBATCH --output=C_Elegan_Results
#SBATCH --ntasks-per-node=1
#SBATCH --nodes=1
#SBATCH --time=60:00
#SBATCH -p gpu-long
#SBATCH --mail-type=BEGIN,END
#SBATCH --mail-user=benjamin.sterling@stonybrook.edu

source activate C_Elegan_boot
python -m pip install ./funlib.learn.torch
python -m pip install torch==1.10.0+cu113 -f https://download.pytorch.org/whl/torch_stable.html
python -m pip install torchvision==0.11.1+cu113 -f https://download.pytorch.org/whl/torchvision/
python train.py
