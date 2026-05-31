import numpy as np
import os
import json
import argparse
from os.path import join 

parser = argparse.ArgumentParser()
parser.add_argument("--output_dir", type=str, default="./views", help="the directory where the renderings are being written")
parser.add_argument("--input_file", type=str)
parser.add_argument("--output_file", type=str, help="the output json file which stores the objects remaining to be rendered")
parser.add_argument("--num_images", type=int, help="the number of images remaining to be rendered")

args = parser.parse_args()
last_name = args.output_dir.split('/')[-1]
print(args.num_images, 'Number of images')

data_list = []
with open(args.input_file, 'r') as file:
    for object_path in file.readlines():
        object_uid = object_path.split(".")[0].split("/")[-1]
        print('Uid', object_uid)
        obj = object_path.strip("\n").strip("/").strip(",").strip("_")
        uid_dir = join(args.output_dir, object_uid)
        if os.path.exists(uid_dir):
            print(os.listdir(uid_dir))
            print(len(os.listdir(uid_dir)))
            if len(os.listdir(uid_dir)) == args.num_images:
                print('Path already exists for uid', object_uid)
            else:
                if obj:
                    print(obj)
                    data_list.append(obj)
        else:
            if obj:
                print(obj)
                data_list.append(obj)
        
        
json_file_path = args.output_file
with open(json_file_path, 'w') as json_file:
    json_file.write(",\n".join(data_list))
        
            