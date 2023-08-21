#!/Applications/Blender.app/Contents/Resources/3.4/python/bin/python3.10
import os 
import glob
import numpy as np
import multiprocessing
from operator import is_not
from functools import partial
import gc
from os.path import join
from multiprocessing import Pool
import argparse
import sys
import bpy
import pickle
import json
import subprocess
#%

"""
This program counts the number of meshes in the 
scene. It imports each scene and then checks the number of
meshes in the scene. Then we get the names of the objects in the folder
which has n = 5 meshes, n=20 meshes, n= 20 and n=100 meshes accordingly
"""
parser = argparse.ArgumentParser(description='take filename so that you are able to distributedly parse the file \
                                 and dont have to compute all at once, ensure it is in extras directory')
parser.add_argument('--filename', type=str, help='input filename')
parser.add_argument('--output_filename', type=str, help='name of the numpy array in which the counts will be stored')

argv = sys.argv[sys.argv.index("--") + 1 :]
args = parser.parse_args(argv)

                
def clear_render_cache():
    print('clear render cache is actually being executed')
    bpy.context.scene.use_nodes = False  # Disable compositing nodes

def reset_scene() -> None:
    """Resets the scene to a clean state."""
    print('Scene reset is actually being executed')
    # delete everything that isn't part of a camera or a light
    for obj in bpy.data.objects:
        if obj.type not in {"CAMERA", "LIGHT"}:
            #print('Removing data objects')
            bpy.data.objects.remove(obj, do_unlink=True)
            
    for obj in bpy.context.scene.objects.values():
        if isinstance(obj.data, (bpy.types.Mesh)):
           #print('Removing mesh objects')
           bpy.data.objects.remove(obj, do_unlink=True)
    # delete all the materials
    for material in bpy.data.materials:
        #print('Removing material objects')
        bpy.data.materials.remove(material, do_unlink=True)
    # delete all the textures
    for texture in bpy.data.textures:
        #print('Removing texture objects')
        bpy.data.textures.remove(texture, do_unlink=True)
    # delete all the images
    for image in bpy.data.images:
        #print('Removing Image objects')
        bpy.data.images.remove(image, do_unlink=True)
    gc.collect()

def count_meshes(objs):
    # reset the scene before every import so that there is no object in the scene
    # this will prevent the ram from being overloaded and lead to a better functioning program
    # still not able to iterate through the whole list. 
    # Maybe create three files and use ntasks=3
    count = 0
    object_name = objs.split('/glbs')[1].split('/')[-1][:-4]
    if object_name in list_lvis and object_name not in dict_counts.keys():
        if objs.endswith(".glb"):
            subprocess_obj = subprocess.Popen([blender_executable]) # probably don't need this code right now.
            return_code = subprocess_obj.wait() # there is no need for code since there is a return code
            
            if return_code == 0:
                print('Blender opened successfully')     # objects end with glb
            else:
                print(f"Blender has not been opened with: {return_code}")  

            bpy.ops.import_scene.gltf(filepath=objs) # why is this giving an error? loading the file should be easy
            for obj in bpy.context.scene.objects.values():
                if isinstance(obj.data, (bpy.types.Mesh)):
                    count+=1
            reset_scene()
            clear_render_cache()               
            bpy.context.scene.use_nodes = False  # Disable compositing nodes 
            dict_counts[object_name] = count
            print(object_name, ':', count)  
            if bpy.ops.wm.quit_blender.poll():
                bpy.ops.wm.quit_blender()
                print('Quitting blender')
            else:
                print('Cannot quit blender at the moment!')
            gc.collect()
            return count
    return None



if __name__ == '__main__':
    num_cores = int(os.getenv("SLURM_CPUS_PER_TASK")) - 5
    objaverse_dir = '/home/janus/iwi9-datasets/objaverse-objects' \
                    '/hf-objaverse-v1/glbs/*/*'
    print(os.getcwd())
    object_dir = list(glob.glob(objaverse_dir))
    base_dir = '../objaverse-rendering/'
    f = open(join(base_dir, 'extras', args.filename), 'r')
    list_lvis = []
    for line in f.readlines():
        line = line.strip('\n')
        list_lvis.append(line)
    
    global dict_counts
    global blender_executable
    blender_executable = bpy.app.binary_path

    
    if os.path.exists('results/counts.json'):
        with open('results/counts.json', 'r') as f:
            dict_counts = json.load(f)
    else:
        dict_counts = {'test': 0}
        with open('results/counts.json', 'w') as f:
            dict_counts = json.dump(dict_counts, f, indent=4)

    with Pool(num_cores) as p:
        list_counts = p.map(count_meshes, object_dir) # we need only the lvis annotated objects,
        # which is defined in function above
    
    with open('results/counts.json', 'w') as f:
                json.dump(dict_counts, f, indent=4)

    list_counts = list(filter(partial(is_not, None), list_counts))
    with open(join('results', args.output_filename)) as f:
        np.save(f, list_counts)


