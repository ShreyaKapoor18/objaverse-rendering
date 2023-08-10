#!/bin/bash -l
#
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --time=08:00:00
#SBATCH --gres=gpu:a40:1
#SBATCH --partition=a40
#SBATCH --export=NONE
#SBATCH -o ./slurm_files/output/generate_json.%j.out

unset SLURM_EXPORT_ENV

module load git
conda init
conda activate pyobjaverse
srun python ~/git/objaverse-rendering/scripts_custom/generate_json_from_text.py