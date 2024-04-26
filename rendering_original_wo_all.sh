export SSL_CERT_DIR=/etc/ssl/certs
export SSL_CERT_FILE=/etc/ssl/cert.pem

mapfile -t items < "C:\Users\Shreya\objaverse-rendering\jsons\input_models_path_lt_100.txt"

export CUDA_VISIBLE_DEVICES=0
# Print the contents of the array
script_name=f"rendering_original_wo_all.sh"
num_items=${#items[@]}
blender_cmd="blender -b -P scripts_custom/blender_script_2_woall.py"

# Function to render an item
function render_item {
    local render_options="--engine CYCLES --num_images 10 --camera_dist 2 --device_type CUDA"
    echo "no textures"
    render_options="$render_options --textures"
    echo "without shadows"
    render_options="$render_options --no_shadows"
    echo "no shading"
    render_options="$render_options --no_shading"
    echo "no specularity"
    render_options="$render_options --no_specular"
    echo "blender -b -P scripts_custom/blender_script_2.py -- --object_path "$item" --output_dir original_wo_shading_2023-11-21_14-34-42 $render_options"
    blender -b -P objaverse-rendering/scripts_custom/blender_script_2_woall.py -- --object_path "$item" --output_dir original_wo_all_08_03_2024 $render_options
}
iteration_count=0
for item in "${items[@]}"; do
        render_item "$item"
        # Additional commands related to rendering can be added here
        ((iteration_count++))
done
