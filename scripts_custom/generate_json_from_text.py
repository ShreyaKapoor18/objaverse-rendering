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
object_paths = objaverse._load_object_paths()

global list_paths
list_paths = []

for name in file.read():
    name = name.strip('\n') + '.glb'   
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # start processes
        futures = [executor.submit(name, string) for string in object_paths]
        # wait for all to finish
        concurrent.futures.wait(futures)
    
with open(join('input_models_path_5.txt'), 'w') as f:
    for line in list_paths:
        f.write(line)  
        