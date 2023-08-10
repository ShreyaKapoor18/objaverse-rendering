import json
import glob
import objaverse
from os.path import join
import os
from multiprocessing import Pool
import itertools
import concurrent.futures


def find(pattern, string):
    if pattern in string:
        print(join(objaverse_dir, string))
        list_paths.append(join(objaverse_dir, name))
        return join(objaverse_dir, string)
    return None


directory = []
base_dir = '~/git/objaverse-rendering/'

file = open(join('results', 'test_5.txt'), 'r')
objaverse_dir = '/home/janus/iwi9-datasets/objaverse-objects/hf-objaverse-v1'
object_paths = list(objaverse._load_object_paths().values())
print(object_paths[:10])

global list_paths
list_paths = []

num_cores = int(os.getenv("SLURM_CPUS_PER_TASK")) - 1
for name in file.read():
    name = name.strip('\n') + '.glb'   
    p = Pool(num_cores)
    list_paths = p.map(find, itertools.repeat(name), object_paths)
    p.close()
    p.join()
    gc.collect()
    
with open(join('input_models_path_5.txt'), 'w') as f:
    for line in list_paths:
        f.write(line)  
        
        