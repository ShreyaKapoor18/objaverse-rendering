import os
import glob
from os.path import join
import objaverse
path1 = "/Users/shreya/Documents/GitHub/objaverse-rendering/jsons/input_models_path_lt_100.txt"

uids = set()
i = 0
with open(path1, 'r') as f:
    for line in f:
        #print('Line', line)
        uid = line.split('/')[-1].replace(".glb", "")
        uid = uid.strip('\n')
        uids.add(uid)
        #print(uids)
    
print('Total number of uids', len(uids))
count_uid = 0
count_found = 0

for files in glob.glob(join("/Users/shreya/Documents/GitHub/objaverse-rendering/hdf5/Hdf5files", "*_combined.txt")):
    #print(files.split('/')[-1].split('_combined.txt')[0])
    print('The file being read is', files)
    filename = files.split('/')[-1].split('_combined.txt')[0]
    with open(files, 'r') as f:
        uids_in_file = set()
        print('50bd4cc3a141400cb84ea66fd8dfb2a6' in uids)
        for line in f:
            uid_line = line.split('.glb')
            uid_line = uid_line[0].strip('\n')
            uid_line = uid_line.replace(" ", "")
            uids_in_file.add(uid_line)
        object_paths = objaverse._load_object_paths()
        uids_remaining = uids.difference(uids_in_file)
        print("number of uids remaining", len(uids_remaining))
        print("Number of uids in file", len(uids_in_file))
        uid_object_paths = [
        f"https://huggingface.co/datasets/allenai/objaverse/resolve/main/{object_paths[uid]}"
        for uid in uids_remaining
        ]
        with open(f"{os.getcwd()}/uids_not_found_{filename}.txt", "w") as f2:
            for path in uid_object_paths:
                #print(path)
                f2.write(path + "\n")
    
