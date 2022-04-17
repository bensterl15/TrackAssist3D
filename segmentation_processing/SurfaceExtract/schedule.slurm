#!/usr/bin/env bash

#SBATCH --job-name=C_Elegan_Results
#SBATCH --output=C_Elegan_Results
#SBATCH --ntasks-per-node=1
#SBATCH --nodes=1
#SBATCH --time=10:00
#SBATCH -p short-24core
#SBATCH --mail-type=BEGIN,END
#SBATCH --mail-user=benjamin.sterling@stonybrook.edu


source activate C_Elegan_boot
python preprocess.py
