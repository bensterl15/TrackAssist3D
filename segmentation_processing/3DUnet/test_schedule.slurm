#!/usr/bin/env bash

#SBATCH --job-name=AM_repellant20
#SBATCH --output=AM_repellant20
#SBATCH --ntasks-per-node=1
#SBATCH --nodes=1
#SBATCH --time=1:00:00
#SBATCH -p gpu
#SBATCH --mail-type=BEGIN,END
#SBATCH --mail-user=benjamin.sterling@stonybrook.edu

source activate C_Elegan_boot
#python -m pip install ./funlib.learn.torch
#python -m pip install torch==1.10.0+cu113 -f https://download.pytorch.org/whl/torch_stable.html
python test.py --image 20
