import objaverse
import os
from os.path import join
annotations = objaverse.load_annotations()
lvis_annotations = objaverse.load_lvis_annotations()

global list_lvis
list_lvis = []
for values in lvis_annotations.values():
    list_lvis.extend(values)
    
base_dir = '../objaverse-rendering/'
f = open(join(base_dir,'extras/list_lvis.txt'), 'w')
for line in list_lvis:
    f.write(line+'\n')
    
print('Done')