#!/bin/bash -l

#SBATCH --gres=gpu:rtx3080:1
#SBATCH --time=24:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --export=NONE
#SBATCH -o ./slurm_files/output/rendering_original_wo_shading.out
#SBATCH -e ./slurm_files/errors/rendering_original_wo_shading.err
unset SLURM_EXPORT_ENV
export SSL_CERT_DIR=/etc/ssl/certs
export SSL_CERT_FILE=/etc/ssl/cert.pem
input_file=jsons/input_models_path_lt_100.txt
items=()  # Initialize the items array
mapfile -t items < jsons/input_models_path_lt_100.txt

export CUDA_VISIBLE_DEVICES=0
# Print the contents of the array
for item in "${items[@]}"; do
    echo "$item"
done
script_name=f"rendering_original_wo_shading.sh"
num_items=${#items[@]}
blender_cmd="blender -b -P scripts_custom/blender_script_2.py"

# Function to render an item
function render_item {
    local render_options="--engine CYCLES --num_images 10 --camera_dist 2 --device_type METAL"
    if [[ "$script_name" == *textures* ]]; then
        echo "no textures"
        render_options="$render_options --textures"
    fi
    if [[ "$script_name" == *wo_shadows* ]]; then
        echo "without shadows"
        render_options="$render_options --no_shadows"
    fi
    if [[ "$script_name" == *wo_shading* ]]; then
        echo "no shading"
        render_options="$render_options --no_shading"
    fi
    if [[ "$script_name" == *no_spec* ]]; then
        echo "no specularity"
        render_options="$render_options --no_specular"
    fi
    if [[ "$script_name" == *original_wo_all* ]]; then
        echo "remove all"
        render_options="$render_options --no_shading --no_shadows --no_specular --textures"
    fi
    

    echo "blender -b -P scripts_custom/blender_script_2.py -- --object_path "$item" --output_dir jsons/original_wo_shading_2024-04-17_10-41-19 $render_options"
    blender -b -P scripts_custom/blender_script_2.py -- --object_path "$item" --output_dir jsons/original_wo_shading_2024-04-17_10-41-19 $render_options
}
iteration_count=0
for item in "${items[@]}"; do
    if [ "$iteration_count" -lt 20 ]; then
        render_item "$item"
        # Additional commands related to rendering can be added here
        ((iteration_count++))
    else
        break  # Exit the loop if the iteration count reaches 20
    fi
done

