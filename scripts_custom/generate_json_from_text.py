import json
import glob
import objaverse
from os.path import join
import os
from multiprocessing import Pool
import itertools
import concurrent.futures
import re


directory = []
base_dir = '~/git/objaverse-rendering/'

file = open(join('results', 'test_5.txt'), 'r')
objaverse_dir = '/home/janus/iwi9-datasets/objaverse-objects/hf-objaverse-v1'
object_paths = list(objaverse._load_object_paths().values())

global list_paths
list_paths = []

num_cores = 2

for name in file.readlines():
    print(name)
    name_2 = name.strip('\n') + '.glb'  
    print(name_2)
    res = [join(objaverse_dir, x) for x in object_paths if x.split('/')[-1]==name_2]
    print(res)
    list_paths.extend(res)


with open(join('input_models_path_5.txt'), 'w') as f:
    for line in list_paths:
        f.write(line + '\n')  
        
        