#!/bin/bash -l

#SBATCH --nodes=1
#SBATCH --cpus-per-task=16
#SBATCH --time=18:00:00
#SBATCH --gres=gpu:a40:8
#SBATCH --partition=a40
#SBATCH --export=NONE
#SBATCH -o ./slurm_files/output/rendering2.%j.out
#SBATCH -e ./slurm_files/errors/rendering2.%j.out

unset SLURM_EXPORT_ENV

# Initialize and activate conda environment
conda init
conda activate pyobjaverse

# Load the CUDA module
module load cuda

# Set SSL certificate directories
export SSL_CERT_DIR=/etc/ssl/certs
export SSL_CERT_FILE=/etc/ssl/ca-bundle.crt

# Set CYCLES_OPENCL_TEST
export CYCLES_OPENCL_TEST=NONE

output_dir="/home/hpc/b112dc/b112dc10/objaverse-rendering/meshes_lt_100_textures"
script="/home/hpc/b112dc/b112dc10/git/objaverse-rendering/scripts_custom/blender_script_2.py"
engine="CYCLES"
filename_original="/home/hpc/b112dc/b112dc10/git/objaverse-rendering/jsons/input_models_path_lt_100.json"

camera_dist=2
num_images=12

# Load CUDA module with version
module load cuda/12.1.1

# Make the distributed script executable
chmod +x ~/git/objaverse-rendering/scripts_custom/distributed2.py

# Modify the output directory path
which_dir="${output_dir%/*}"
output_filename="/home/hpc/b112dc/b112dc10/git/objaverse-rendering/jsons/input_models_path_remaining_${which_dir}.json"

# Run the Python script to write new files and check paths
python scripts_custom/write_new_files_check_paths.py --output_dir "$output_dir" --input_file "$filename_original" --num_images "$num_images"

# Use srun to run the distributed Python script
srun python /home/hpc/b112dc/b112dc10/git/objaverse-rendering/scripts_custom/distributed2.py \
     --num_gpus 8 --input_models_path "$filename_original" \
     --workers_per_gpu 14 --script "$script" --camera_dist "$camera_dist" --num_images "$num_images"

