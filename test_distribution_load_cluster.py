#%%
import objaverse
import trimesh
import glob
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing
from joblib import Parallel, delayed
from operator import is_not
from functools import partial
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


objaverse_dir = '/home/janus/iwi9-datasets/objaverse-objects/hf-objaverse-v1/glbs/*/*'

'''
In trimesh, the main class that represents a geometry is called Trimesh. It represents a single 3D mesh or a collection of connected triangles that form a surface.
'''
annotations = objaverse.load_annotations()
lvis_annotations = objaverse.load_lvis_annotations()

list_lvis = []
for values in lvis_annotations.values():
    list_lvis.extend(values)

object_dir = list(glob.glob(objaverse_dir))
print(object)
list_counts = Parallel(n_jobs=-1)(delayed(count_objects)(object) for object in object_dir)
#list_counts = list(filter(partial(is_not, None), list_counts))
print(list_counts)

with open('results/count_objects.npy', 'wb') as f:
    a = np.save(f, list_counts)

fig = plt.figure()
plt.hist(list_counts)
plt.title('Distribution over the objects')
plt.xlabel('Number of meshes')
plt.ylabel('Number of objects')
plt.savefig('results/distribution.png')


#%%
