import objaverse
import trimesh
import glob
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing
from joblib import Parallel, delayed
from operator import is_not
from functools import partial
import bpy
#%%
# store the ids of the objects with less than 50 geometries
def count_objects(object):
    f1 = open('results/object_names_5.txt', 'a')
    f2 = open('results/object_names_10.txt', 'a')
    f2 = open('results/object_names_1.txt', 'a')
    f3 = open('results/object_names_2.txt', 'a')
    f4 = open('results/object_names_20.txt', 'a')
    object_name = object.split('/glbs')[1].split('/')[-1][:-4]
    print(object_name)
    #if object_name in list_lvis:
            
    scene = trimesh.load(object)
    '''        print(scene.geometry)
            if len(scene.geometry) == 5: 
                print(object_name, file=f1)
            if len(scene.geometry) == 10:
                print(object_name, file=f1)
            if len(scene.geometry) == 1:
                print(object_name, file=f2)
            if len(scene.geometry) == 2:
                print(object_name, file=f3)
            if len(scene.geometry) == 20:
                print(object_name, file= f4)'''
    return scene.geometry
    #return None


def count_meshes(objs):
    print(objs)
    bpy.ops.import_scene.gltf(filepath=objs, merge_vertices=True)
    count = 0
    print(bpy.data)
    #print(bpy.data.objects)
    try:
        for obj in bpy.data.objects:
            if isinstance(obj.data, (bpy.types.Mesh)):
                count+=1
        return count
    except:
        print('could not load scene')
        return None


objaverse_dir = '/home/janus/iwi9-datasets/objaverse-objects/hf-objaverse-v1/glbs/*/*'

#annotations = objaverse.load_annotations()
#lvis_annotations = objaverse.load_lvis_annotations()

#list_lvis = []
#for values in lvis_annotations.values():
#    list_lvis.extend(values)

object_dir = list(glob.glob(objaverse_dir))

list_counts = Parallel(n_jobs=-1)(delayed(count_meshes)(object) for object in object_dir[:5])
list_counts = list(filter(partial(is_not, None), list_counts))

with open('results/count_objects.npy', 'wb') as f:
    a = np.save(f, list_counts)

fig = plt.figure()
plt.hist(list_counts)
plt.title('Distribution over the objects')
plt.xlabel('Number of meshes')
plt.ylabel('Number of objects')
plt.savefig('results/distribution.png')
#%%




