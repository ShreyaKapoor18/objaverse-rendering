#!/bin/bash -l
#
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=5
#SBATCH --time=08:00:00
#SBATCH --gres=gpu:a40:2
#SBATCH --partition=a40
#SBATCH --export=NONE
#SBATCH -o ./slurm_files/output/rendering.%j.out

unset SLURM_EXPORT_ENV
conda init
conda activate pyobjaverse
filename=$(cat ~/git/objaverse-rendering/input_models_path_lt_5.txt)
export SSL_CERT_DIR=/etc/ssl/certs
export SSL_CERT_FILE=/etc/ssl/ca-bundle.crt
module load cuda/12.1.1
export CYCLES_OPENCL_TEST=NONE
for item in $filename;
do  
    echo $item
    ~/blender/blender-3.3.1-linux-x64/blender -b -P scripts_custom/blender_script_2.py -- \
        --object_path $item \
        --output_dir /home/hpc/b112dc/b112dc10/all_less_than_5 \
        --engine CYCLES \
        --num_images 12 \
        --camera_dist 2 \
done
