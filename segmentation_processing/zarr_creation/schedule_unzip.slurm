#!/usr/bin/env bash

#SBATCH --job-name=unzip_res
#SBATCH --output=unzip_res
#SBATCH --ntasks-per-node=1
#SBATCH --nodes=1
#SBATCH --time=20:00
#SBATCH -p short-28core
#SBATCH --mail-type=BEGIN,END
#SBATCH --mail-user=benjamin.sterling@stonybrook.edu

source activate C_Elegan_boot
python unzip.py
