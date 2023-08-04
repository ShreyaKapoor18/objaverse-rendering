import json
import glob
from os.path import join
import fnmatch
import os, re, os.path
import multiprocessing
from multiprocessing import Pool, freeze_support
from functools import partial
import concurrent.futures
import itertools


def ends_with_pattern(teststring, pattern):
    matching_strings = [] 
    if re.search(re.escape(pattern) + "$", teststring):
        matching_strings.append(teststring)
        print(teststring)
    
    return matching_strings


num_cores = int(os.getenv("SLURM_CPUS_PER_TASK"))# reptetitively giving one object, why???
print('Number of cores', num_cores) 


directory = []
file = open('results/test_5.txt', 'r')
objaverse_dir = '/home/janus/iwi9-datasets/objaverse-objects/hf-objaverse-v1/glbs/*'
object_id_paths = list(glob.glob(join(objaverse_dir, '*')))
#print(object_id_paths)
for object_name in file.readlines():
    object_name = object_name.strip('\n')
    pattern = object_name + '.glb'
    with Pool(num_cores) as p:
        object_path = p.starmap(ends_with_pattern, zip(object_id_paths, itertools.repeat(pattern)))
    directory.append(object_path)
    
json_string = json.dumps(directory)

with open('input_models_path.json', 'w') as f:
    json.dump(json_string, f) 