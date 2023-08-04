conda activate pyobjaverse
filename=$(cat ~/Documents/GitHub/objaverse-rendering/input_models_path_2.txt)
export SSL_CERT_DIR=/etc/ssl/certs
export SSL_CERT_FILE=/etc/ssl/cert.pem
for item in $filename;
do  
    echo $item
    blender -b -P scripts_custom/blender_script_2.py -- \
        --object_path $item \
        --output_dir ./views \
        --engine CYCLES \
        --num_images 12 \
        --camera_dist 1.2 \
        --textures True
done