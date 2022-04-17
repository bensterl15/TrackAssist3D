#!/usr/bin/env bash

#SBATCH --job-name=Thresh_Results
#SBATCH --output=Thresh_Results
#SBATCH --ntasks-per-node=1
#SBATCH --nodes=1
#SBATCH --time=1:00:00
#SBATCH -p short-28core
#SBATCH --mail-type=BEGIN,END
#SBATCH --mail-user=benjamin.sterling@stonybrook.edu

source activate C_Elegan_boot
python apply_threshnet.py
