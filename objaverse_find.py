import objaverse
from os.path import join

uids = ['a800eb049d5f4ccaa85649d23ccd117f', 'd4ba24895a324321ab7438e8d1d87a39', '69de7b6bd3004eba8c6aa41d37858d86', 'e3edad5c3f1a4fc7bfc8e3ee1bc0e521', 
        'f957820ce0c645f5a36d0e89350964ef']

object_paths = objaverse._load_object_paths()
for uid in uids:
    print(join('https://huggingface.co/datasets/allenai/objaverse/resolve/main', object_paths[uid]))
#print(uids)
print('***'*20)

    