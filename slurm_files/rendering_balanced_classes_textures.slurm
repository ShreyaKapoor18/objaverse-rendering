#!/bin/bash -l
#SBATCH --cpus-per-task=2
#SBATCH --time=18:00:00
#SBATCH --gres=gpu:a40:1
#SBATCH --partition=a40
#SBATCH --export=NONE
#SBATCH -o ./slurm_files/output/rendering_balanced_classes_textures.%j.out
#SBATCH -e ./slurm_files/errors/rendering_balanced_classes_textures.%j.out
unset SLURM_EXPORT_ENV
script_name=$(basename "$0")
output_filename="$WORK/objaverse-rendering/jsons/input_models_path_lt_100_remaining_balanced_classes_textures.txt"

# Load CUDA module with version
module load cuda/12.1.1

# Activate Conda environment
source activate pyobjaverse

# Run the Python script to write new files and check paths
srun python scripts_custom/write_new_file_check_paths.py --output_dir /home/janus/iwi9-datasets/objaverse-rendering/balanced_classes_textures --input_file $WORK/objaverse-rendering/jsons/input_models_path_lt_100.txt --num_images 15  --output_file $WORK/objaverse-rendering/jsons/input_models_path_lt_100_remaining_balanced_classes_textures.txt

export PATH="/home/atuin/b112dc/b112dc10/blender-3.3.1-linux-x64:$PATH"
blender_cmd="blender -b -P scripts_custom/blender_script_2.py"

gpu_indices=(0)
mapfile -t -n 50 items < "$WORK/objaverse-rendering/jsons/input_models_path_lt_100_remaining_balanced_classes_textures.txt"
chosen_gpu="${gpu_indices[0]}"
num_items=${#items[@]}
export PATH="/home/atuin/b112dc/b112dc10/blender-3.3.1-linux-x64:$PATH"
blender_cmd="blender -b -P scripts_custom/blender_script_2.py"

# Function to render an item
function render_item {
    local render_options="--engine CYCLES --num_images 15 --camera_dist 2"
    if [[ "$script_name" == *textures* ]]; then
        render_options="$render_options --textures"
    fi
    # Check if "ambient" or "shadows" is in the script name
    if [[ "$script_name" == *ambient* || "$script_name" == *shadows* ]]; then
        # Include --bake_ao option when either "ambient" or "shadows" is in the script name
        render_options="$render_options --bake_ao"
    fi
    CUDA_VISIBLE_DEVICES="$chosen_gpu" srun /home/atuin/b112dc/b112dc10/blender-3.3.1-linux-x64/blender -b -P scripts_custom/blender_script_2.py --    --object_path "$item" --output_dir /home/janus/iwi9-datasets/objaverse-rendering/balanced_classes_textures $render_options
    echo CUDA_VISIBLE_DEVICES="$chosen_gpu" srun /home/atuin/b112dc/b112dc10/blender-3.3.1-linux-x64/blender -b -P scripts_custom/blender_script_2.py --    --object_path "$item" --output_dir "$output_dir" $render_options
}

# Use only one GPU for rendering
# Iterate through the remaining items and render them one by one

for item in "${items[@]}"; do
    # Render the current item
    echo "Rendering $item"
    render_item "$item"
    # Wait for the rendering process to complete before moving on to the next item
    wait
done 
while true; do
    # Check if the file is empty (zero size)
    if [ -s $output_filename ]; then
        # The file is not empty, so submit the job
        sbatch slurm_files/rendering_balanced_classes_textures.slurm
    else
        # The file is empty, so exit the loop
        echo "File is empty. Exiting."
        break
    fi

    # Wait for some time before checking again (e.g., 5 minutes)
    sleep 300
done
