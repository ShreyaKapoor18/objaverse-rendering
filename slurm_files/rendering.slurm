#!/bin/bash -l
#
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --time=08:00:00
#SBATCH --gres=gpu:a40:1
#SBATCH --partition=a40
#SBATCH --export=NONE

unset SLURM_EXPORT_ENV
conda init
conda activate pyobjaverse
filename=$(cat ~/git/objaverse-rendering/input_models_path.json)
for item in $filename;
do
    ~/blender/blender-3.3.1-linux-x64/blender -b -P scripts/blender_script_2.py -- \
        --object_path $item \
        --output_dir /home/janus/iwi9-datasets/objaverse-rendering/textures \
        --engine CYCLES \
        --num_images 12 \
        --camera_dist 1.2
done