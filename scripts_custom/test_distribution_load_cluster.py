#!/Applications/Blender.app/Contents/Resources/3.4/python/bin/python3.10

import bpy
import os 
import glob
import numpy as np
import multiprocessing
from operator import is_not
from functools import partial
import gc
import os
from os.path import join
from multiprocessing import Pool
#%

"""
This program counts the number of meshes in the 
scene. It imports each scene and then checks the number of
meshes in the scene. Then we get the names of the objects in the folder
which has n = 5 meshes, n=20 meshes, n= 20 and n=100 meshes accordingly
"""

def reset_scene() -> None:
    """Resets the scene to a clean state."""
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
    reset_scene()
    print(objs)
    if objs.endswith(".glb"):
        bpy.ops.import_scene.gltf(filepath=objs) # why is this giving an error? loading the file should be easy
    count = 0
    object_name = objs.split('/glbs')[1].split('/')[-1][:-4]
    if object_name in list_lvis:
        for obj in bpy.context.scene.objects.values():
            if isinstance(obj.data, (bpy.types.Mesh)):
                count+=1
        f1 = open('results/object_names_5.txt', 'a')
        f2 = open('results/object_names_10.txt', 'a')
        f2 = open('results/object_names_1.txt', 'a')
        f3 = open('results/object_names_2.txt', 'a')
        f4 = open('results/object_names_20.txt', 'a')
        f5 = open('results/object_names_100.txt', 'a')
        if count == 5: 
                    print(object_name, file=f1)
        if count == 10:
                    print(object_name, file=f1)
        if count == 1:
                    print(object_name, file=f2)
        if count == 2:
                    print(object_name, file=f3)
        if count == 20:
                    print(object_name, file=f4)
        if count == 100:
                    print(object_name, file=f5)
        return count
    return None



if __name__ == '__main__':
    num_cores = int(os.getenv("SLURM_CPUS_PER_TASK"))# reptetitively giving one object, why???
    objaverse_dir = '/home/janus/iwi9-datasets/objaverse-objects/hf-objaverse-v1/glbs/*/*'
    print(os.getcwd())
    object_dir = list(glob.glob(objaverse_dir))
    base_dir = '../objaverse-rendering/'
    f = open(join(base_dir,'extras/list_lvis.txt'), 'r')
    list_lvis = []
    for line in f.readlines():
        line = line.strip('\n')
        list_lvis.append(line)
        
    list_lvis = list_lvis[:len(list_lvis/2)]
    
    print(list_lvis)
    with Pool(num_cores) as p:
        list_counts = p.map(count_meshes, object_dir) # we need only the lvis annotated objects, which is defined in function above

    list_counts = list(filter(partial(is_not, None), list_counts))
    with open('results/count_objects.npy', 'wb') as f:
        a = np.save(f, list_counts)


