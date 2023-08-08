import objaverse
import os
from os.path import join
annotations = objaverse.load_annotations()
lvis_annotations = objaverse.load_lvis_annotations()

"""
Get the lvis annotations and then split it into
n files according to the given program.

"""

n = 5
# Let us split the file into 5 so that we can process each one individually

global list_lvis
list_lvis = []
for values in lvis_annotations.values():
    list_lvis.extend(values)

def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

splitted_list = split(list_lvis, 5)
base_dir = '../objaverse-rendering/'

for i, spl in zip(range(5), splitted_list):
    with  open(join(base_dir,f'extras/list_lvis_{i}.txt'), 'w') as f:
        for line in spl:
            f.write(line+'\n')

