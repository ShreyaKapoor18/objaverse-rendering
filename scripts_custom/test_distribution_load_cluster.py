import blenderproc as bproc
import objaverse
import trimesh
import glob
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing
from operator import is_not
from functools import partial
import gc
#%%
# store the ids of the objects with less than 50 geometries
def count_objects(object):
    f1 = open('results/object_names_5.txt', 'a')
    f2 = open('results/object_names_10.txt', 'a')
    f2 = open('results/object_names_1.txt', 'a')
    f3 = open('results/object_names_2.txt', 'a')
    f4 = open('results/object_names_20.txt', 'a')
    object_name = object.split('/glbs')[1].split('/')[-1][:-4]           
            
    scene = trimesh.load(object)
    
    return scene.geometry


def count_meshes(objs):
    print(objs)
    scene = bproc.loader.load_obj(filepath=objs)
    count = 0
    object_name = objs.split('/glbs')[1].split('/')[-1][:-4]
    if object_name in list_lvis:
        for obj in scene:
                if isinstance(obj, (bproc.types.MeshObject)):
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
                    print(object_name, file= f4)
        if count == 100:
                    print(object_name, file=f5)
        return count
    bproc.clean_up()
    del scene
    gc.collect()
    return None


objaverse_dir = '/home/janus/iwi9-datasets/objaverse-objects/hf-objaverse-v1/glbs/*/*'

annotations = objaverse.load_annotations()
lvis_annotations = objaverse.load_lvis_annotations()

list_lvis = []
for values in lvis_annotations.values():
   list_lvis.extend(values)

object_dir = list(glob.glob(objaverse_dir))

list_counts = []
for object in glob.glob(objaverse_dir):
    list_counts.append(count_meshes(object))

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




