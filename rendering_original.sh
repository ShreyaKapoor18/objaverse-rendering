#!/bin/bash -l

#SBATCH --gres=gpu:rtx3080:1
#SBATCH --time=24:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --export=NONE
#SBATCH -o ./slurm_files/output/rendering_original.out
#SBATCH -e ./slurm_files/errors/rendering_original.err
unset SLURM_EXPORT_ENV
export SSL_CERT_DIR=/etc/ssl/certs
export SSL_CERT_FILE=/etc/ssl/cert.pem
input_file=/Users/shreya/Documents/GitHub/objaverse-rendering/hdf5/Hdf5files/uids_not_found_combined_original.txt
items=()  # Initialize the items array
while IFS= read -r -u 3 line && [ ${#items[@]} -lt 22500 ]; do
    items+=("$line")
done 3< "/Users/shreya/Documents/GitHub/objaverse-rendering/hdf5/Hdf5files/uids_not_found_combined_original.txt"
export PATH="/Applications/Blender.app/Contents/MacOS:$PATH"
# Print the contents of the array
for item in "${items[@]}"; do
    echo "$item"
done
script_name=f"rendering_original.sh"
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

    echo "blender -b -P scripts_custom/blender_script_2.py -- --object_path "$item" --output_dir /Users/shreya/Documents/GitHub/objaverse-rendering/original_2023-12-07_20-30-44 $render_options"
    blender -b -P scripts_custom/blender_script_2.py -- --object_path "$item" --output_dir /Users/shreya/Documents/GitHub/objaverse-rendering/original_2023-12-07_20-30-44 $render_options
}
iteration_count=0
for item in "${items[@]}"; do
        render_item "$item"
        # Additional commands related to rendering can be added here
        ((iteration_count++))
done

