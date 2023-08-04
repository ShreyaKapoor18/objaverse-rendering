#!/bin/bash -l
#
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --time=08:00:00
#SBATCH --gres=gpu:a40:1
#SBATCH --partition=a40
#SBATCH --export=NONE

unset SLURM_EXPORT_ENV

module load git
conda init
conda activate pyobjaverse
srun blenderproc run test_distribution_load_cluster.py