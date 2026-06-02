import json
import objaverse
from os.path import join
from multiprocessing import Pool
import os
# ... (other imports and variable definitions)

def process_object(key):
    objaverse_dir = '/home/janus/iwi9-datasets/objaverse-objects/hf-objaverse-v1'
    if dict_json[key] <= 60:
        name = key + '.glb'
        res = [join(objaverse_dir, x) for x in object_paths if x.split('/')[-1] == name]
        return res
    return []

if __name__ == '__main__':
    
    num_cores = int(os.getenv("SLURM_CPUS_PER_TASK", "4")) - 2

    with open('results/counts.json') as f:
        dict_json = json.load(f)

    object_paths = list(objaverse._load_object_paths().values())

    list_paths = []

    with Pool(num_cores) as p:
        results = p.map(process_object, dict_json.keys())
        for res in results:
            list_paths.extend(res)

    with open(join('input_models_path_lt_100.txt'), 'w') as f:
        for line in list_paths:
            f.write(line + '\n')
