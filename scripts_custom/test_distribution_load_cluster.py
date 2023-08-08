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
#%

"""
This program counts the number of meshes in the 
scene. It imports each scene and then checks the number of
meshes in the scene. Then we get the names of the objects in the folder
which has n = 5 meshes, n=20 meshes, n= 20 and n=100 meshes accordingly
"""
parser = argparse.ArgumentParser(description='take filename so that you are able to distributedly parse the file and dont have to compute all at once, ensure it is in extras directory')
parser.add_argument('--filename', type=str, help='input filename')
parser.add_argument('--output_filename', type=str, help='name of the numpy array in which the counts will be stored')

argv = sys.argv[sys.argv.index("--") + 1 :]
args = parser.parse_args(argv)

                
def clear_render_cache():
    print('clear render cache is actually being executed')
    bpy.context.scene.use_nodes = False  # Disable compositing nodes
    bpy.ops.wm.memorystate_statistics_reset()

def reset_scene() -> None:
    """Resets the scene to a clean state."""
    print('Scene reset is actually being executed')
    # delete everything that isn't part of a camera or a light
    for obj in bpy.data.objects:
        if obj.type not in {"CAMERA", "LIGHT"}:
            bpy.data.objects.remove(obj, do_unlink=True)
    # delete all the materials
    for material in bpy.data.materials:
        bpy.data.materials.remove(material, do_unlink=True)
    # delete all the textures
    for texture in bpy.data.textures:
        bpy.data.textures.remove(texture, do_unlink=True)
    # delete all the images
    for image in bpy.data.images:
        bpy.data.images.remove(image, do_unlink=True)

def count_meshes(objs):
    # reset the scene before every import so that there is no object in the scene
    # this will prevent the ram from being overloaded and lead to a better functioning program
    # still not able to iterate through the whole list. 
    with open('results/counts.json') as f:
        dict_counts = json.load(f)
    # Maybe create three files and use ntasks=3
    gc.collect() # call garbage collection to reduce memory collection and performance. 
    count = 0
    object_name = objs.split('/glbs')[1].split('/')[-1][:-4]
    if object_name in list_lvis and object_name not in dict_counts.keys():
        if objs.endswith(".glb"):
            bpy.ops.import_scene.gltf(filepath=objs) # why is this giving an error? loading the file should be easy
            for obj in bpy.context.scene.objects.values():
                if isinstance(obj.data, (bpy.types.Mesh)):
                    count+=1
            reset_scene()
            clear_render_cache()
            
            for obj in bpy.data.objects:
                if obj.type not in {"CAMERA", "LIGHT"}:
                    bpy.data.objects.remove(obj, do_unlink=True)
            # delete all the materials
            for material in bpy.data.materials:
                bpy.data.materials.remove(material, do_unlink=True)
            # delete all the textures
            for texture in bpy.data.textures:
                bpy.data.textures.remove(texture, do_unlink=True)
            # delete all the images
            for image in bpy.data.images:
                bpy.data.images.remove(image, do_unlink=True)
                
            bpy.context.scene.use_nodes = False  # Disable compositing nodes 
            dict_counts.append({objs : count_meshes})
            with open('results/counts.json') as f:
                json.dump(dict_counts)
            print(objs, ':', count)            
            return count
    return None



if __name__ == '__main__':
    num_cores = int(os.getenv("SLURM_CPUS_PER_TASK"))# reptetitively giving one object, why???
    

    objaverse_dir = '/home/janus/iwi9-datasets/objaverse-objects/hf-objaverse-v1/glbs/*/*'
    print(os.getcwd())
    object_dir = list(glob.glob(objaverse_dir))
    base_dir = '../objaverse-rendering/'
    f = open(join(base_dir, 'extras', args.filename), 'r')
    list_lvis = []
    for line in f.readlines():
        line = line.strip('\n')
        list_lvis.append(line)
        
    
    print(list_lvis)
    with Pool(num_cores) as p:
        list_counts = p.map(count_meshes, object_dir) # we need only the lvis annotated objects, which is defined in function above

    list_counts = list(filter(partial(is_not, None), list_counts))
    with open('results', args.output_filename, 'wb') as f:
        a = np.save(f, list_counts)


