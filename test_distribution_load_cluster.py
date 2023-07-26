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
    f1 = open('results/object_names_50.txt', 'a')
    object_name = object.split('/glbs')[1].split('/')[-1][:-4]
    if object_name in list_lvis:
            
            scene = trimesh.load(object)
            if len(scene.geometry) < 50: 
                print(object_name, file=f1)

            return len(scene.geometry)
    return None


objaverse_dir = '/home/janus/iwi9-datasets/objaverse-objects/hf-objaverse-v1/glbs/*/*'


annotations = objaverse.load_annotations()
lvis_annotations = objaverse.load_lvis_annotations()

list_lvis = []
for values in lvis_annotations.values():
    list_lvis.extend(values)

object_dir = list(glob.glob(objaverse_dir))

list_counts = Parallel(n_jobs=-1)(delayed(count_objects)(object) for object in object_dir)
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
