import argparse
import json
import multiprocessing
import random
from dataclasses import dataclass
import boto3
import tyro
from tqdm import tqdm
import objaverse


@dataclass
class Args:
    skip_completed: bool = False
    """whether to skip the files that have already been downloaded"""


def get_completed_uids():
    # get all the files in the objaverse-images bucket
    s3 = boto3.resource("s3")
    bucket = s3.Bucket("objaverse-images")
    bucket_files = [obj.key for obj in tqdm(bucket.objects.all())]

    dir_counts = {}
    for file in bucket_files:
        d = file.split("/")[0]
        dir_counts[d] = dir_counts.get(d, 0) + 1

    # get the directories with 12 files
    dirs = [d for d, c in dir_counts.items() if c == 12]
    return set(dirs)

def ten_per_cat(annotations, uids):
    categories = ['characters-creatures', 'cultural-heritage-history', 'furniture-home', 'art-abstract',
                  'science-technology', 'architecture', 'cars-vehicles', 'places-travel', 'people', 'food-drink',
                  'fashion-style', 'sports-fitness', 'music', 'news-politics', 'animals-pets', 'nature-plants', 
                  'electronics-gadgets', 'weapons-military']
    dict_cat = {}
    for category in categories:
        cnt = 0 
        category_uids = []
        for i in range(len(uids)):
            if annotations[uids[i]]['categories'] != []:
                if len(annotations[uids[i]]['categories']) == 1:
                    if annotations[uids[i]]['categories'][0]['name'] == category:
                        cnt +=1
                        category_uids.append(uids[i])
                elif len(annotations[uids[i]]['categories']) == 2:
                    if annotations[uids[i]]['categories'][1]['name'] == category:
                        cnt +=1
                        category_uids.append(uids[i])
            if cnt ==10:
                dict_cat[category] = category_uids
                break
    return dict_cat       

def lvis_cats():
    import itertools
    lvis_annotations = objaverse.load_lvis_annotations()
    #categories = lvis_annotations.keys()
    listkey = list(lvis_annotations.values())
    merged_uids = list(itertools.chain(*listkey))
    
    return merged_uids


            

# set the random seed to 42
if __name__ == "__main__":
    args = tyro.cli(Args)

    random.seed(42)

    #uids = objaverse.load_uids()
    annotations = objaverse.load_annotations()
    object_paths = objaverse._load_object_paths()
    print(len(object_paths))
    processes = multiprocessing.cpu_count()
    #uids = uids[args.start_i : args.end_i]
    #dict_cat = ten_per_cat(annotations, uids)
    #list_cat = []
    #for cat in dict_cat:
    #    list_cat.extend(dict_cat[cat])
    #print(list_cat)
    #uids = list_cat
    #print(len(uids))
    uids = lvis_cats()
    # values should be around 47k
    print(len(uids))
    # get the uids that have already been downloaded
    if args.skip_completed:
        completed_uids = get_completed_uids()
        uids = [uid for uid in uids if uid not in completed_uids]

    uid_object_paths = [
        f"https://huggingface.co/datasets/allenai/objaverse/resolve/main/{object_paths[uid]}"
        for uid in uids
    ]

    objects = objaverse.load_objects(uids=uids, download_processes=processes)
    print(len(uid_object_paths))
    with open("input_models_path.json", "w") as f:
        json.dump(uid_object_paths, f, indent=2)
