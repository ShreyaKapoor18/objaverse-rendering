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

def count_objects(object):
    object_name = object.split('/glbs')[1].split('/')[-1][:-4]
    if object_name in list_lvis:
            print(object_name)
            scene = trimesh.load(object)
            #print(dir(scene))
            #print(scene.geometry)
            print(len(scene.geometry))
            #print(len(scene))
            return len(scene.geometry)
    return None
objaverse_dir = '/home/janus/iwi9-datasets/objaverse-objects/hf-objaverse-v1/glbs/*/*'

annotations = objaverse.load_annotations()
lvis_annotations = objaverse.load_lvis_annotations()

list_lvis = []
for values in lvis_annotations.values():
    list_lvis.extend(values)

object_dir = list(glob.glob(objaverse_dir))

list_counts=Parallel(n_jobs=-1)(delayed(count_objects)(object) for object in object_dir)
list_counts = list(filter(partial(is_not, None), list_counts))

with open('results/count_objects.npy', 'w') as f:
    a = np.save(f, list_counts)

fig, ax = plt.figure()
plt.hist(count_objects)
plt.title('Distribution over the objects')


print('The total Number of objects with less than 50 objects', count_objects)
print('The total Number of objects with less than 50 objects', count_objects, file='output.txt')