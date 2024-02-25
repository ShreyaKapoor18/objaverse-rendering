#!/bin/bash -l
python scripts_custom/write_new_file_check_paths.py --output_dir ~/git/objaverse-rendering/meshes_lt_100_shadows_textures --input_file $WORK/objaverse-rendering/jsons/input_models_path_lt_100.txt --num_images 15  --output_file $WORK/objaverse-rendering/jsons/input_models_path_lt_100_remaining_meshes_lt_100_shadows_textures.txt
blender_cmd="blender -b -P scripts_custom/blender_script_2.py"
gpu_indices=(0)
mapfile -t -n 50 items < "$WORK/objaverse-rendering/jsons/input_models_path_lt_100_remaining_meshes_lt_100_shadows_textures.txt"
chosen_gpu="${gpu_indices[0]}"
num_items=${#items[@]}
blender_cmd="blender -b -P scripts_custom/blender_script_2.py"

# Function to render an item
function render_item {
    local render_options="--engine CYCLES --num_images 15 --camera_dist 2"
    if [[ "$script_name" == *textures* ]]; then
        render_options="$render_options --textures"
    fi
    if [[ "$script_name" == *ambient* || "$script_name" == *shadows* ]]; then
        render_options="$render_options --bake_ao"
    fi
    blender -b -P scripts_custom/blender_script_2.py --\
    --object_path "$item" --output_dir ~/git/objaverse-rendering/meshes_lt_100_shadows_textures $render_options
}
for item in "${items[@]}"; do
    render_item "$item"
done
