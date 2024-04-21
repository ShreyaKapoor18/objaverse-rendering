import os
import datetime
import glob
from os.path import join
import re
import os
#folder_names = glob.glob('/Users/shreya/git/objaverse-rendering/*')
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
folder_names = ['original', 'textures', 'original_wo_shadows', 'original_wo_shading', 'original_no_spec', 'original_wo_all']
for folder in folder_names:
    pattern = r"_\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}$"
    print(pattern)
    stripped_name = re.sub(pattern, '', folder)
    print('Stripped name', stripped_name)
    name = stripped_name.split('/')[-1]
    print(name)
    num_images = 3 # around 3 images per object is fine
    script_name = f"rendering_{name}.sh"
    output_dir = f"~/Users/shreya/Documents/GitHub/jsons/{name}_{timestamp}"  # Use the full path to the output directory
    match_pattern = f"~/Users/shreya/Documents/GitHub/jsons/{name}"
    #for dir in glob.glob(join(match_pattern+"*")):
    #    print(f"rm -rf {dir}")
    #    os.system(f"rm -rf {dir}")
    os.makedirs(output_dir, exist_ok=True)
    filename_original = "~/Users/shreya/Documents/GitHub/jsons/input_models_path_lt_100.txt"
    output_filename = f"~/Users/shreya/Documents/GitHub/jsons/input_models_path_lt_100_remaining_{name}.txt"

    # Create the Bash script for the current folder
    script_content = f"""#!/bin/bash -l

#SBATCH --gres=gpu:rtx3080:1
#SBATCH --time=24:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --export=NONE
#SBATCH -o ./slurm_files/output/rendering_{name}.out
#SBATCH -e ./slurm_files/errors/rendering_{name}.err
export PATH='/home/atuin/b112dc/b112dc10/blender-3.3.1-linux-x64.$PATH'
unset SLURM_EXPORT_ENV
export SSL_CERT_DIR=/etc/ssl/certs
export SSL_CERT_FILE=/etc/ssl/cert.pem
python3 scripts_custom/write_new_file_check_paths.py --output_dir {output_dir} --input_file {filename_original} --num_images {num_images} --output_file {output_filename}
input_file=~/Users/shreya/Documents/GitHub/objvaerse-rendering/jsons/input_models_path_lt_100.txt
items=()  # Initialize the items array
mapfile -t items < ~/Users/shreya/Documents/GitHub/objvaerse-rendering/jsons/input_models_path_lt_100.txt

export CUDA_VISIBLE_DEVICES=0
# Print the contents of the array
for item in "${{items[@]}}"; do
    echo "$item"
done
script_name=f"rendering_{name}.sh"
num_items=${{#items[@]}}
blender_cmd="blender -b -P scripts_custom/blender_script_2.py"

# Function to render an item
function render_item {{
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
    

    echo "blender -b -P scripts_custom/blender_script_2.py -- --object_path "$item" --output_dir {output_dir} $render_options"
    blender -b -P scripts_custom/blender_script_2.py -- --object_path "$item" --output_dir {output_dir} $render_options
}}
iteration_count=0
for item in "${{items[@]}}"; do
    if [ "$iteration_count" -lt 20 ]; then
        render_item "$item"
        # Additional commands related to rendering can be added here
        ((iteration_count++))
    else
        break  # Exit the loop if the iteration count reaches 20
    fi
done

"""

    with open(script_name, "w") as script_file:
        print(os.getcwd())
        print("writing to here", script_name)
        script_file.write(script_content)
