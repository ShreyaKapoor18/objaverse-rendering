#%%
import objaverse
import matplotlib.pyplot as plt
from matplotlib.widgets import RangeSlider
import numpy as np
import glob
import os
import json
import multiprocessing
import shutil
import subprocess
import time
from dataclasses import dataclass
from typing import Optional

import boto3
import tyro
import wandb


lvis_annotations = objaverse.load_lvis_annotations()
count_keys = [len(lvis_annotations[l]) for l in lvis_annotations.keys()]
count_keys.sort(reverse=True)
print(count_keys)
#%%
fig, ax = plt.subplots()
plt.plot(range(1156), count_keys)
slider_ax = fig.add_axes([0.20, 0.1, 0.60, 0.03])
slider = RangeSlider(slider_ax, "Threshold", min(count_keys), max(count_keys))

plt.xlabel('Category Number')
plt.ylabel('Number of objects in the category')
plt.show()

#%%
count_20 = 0
count_40 = 0
count_60 = 0
count_80 = 0
count_100 = 0
count_500 = 0
count_500p = 0
#%%
for key in lvis_annotations.keys():
    num = len(count_keys)
    if num<=20:
            count_20+=1
    if num>=20 and num<=40:
            count_40+=1
    if num>=40 and num<=60:
            count_60+=1
    if num>=60 and num<=80:
            count_80+=1
    if num>=80 and num<=100:
            count_100+=1
    if num>=100 and num<=500:
            count_500+=1
    if num>=500:
            count_500p+=1
#%%
l_count = [count_20, count_40, count_60, count_80, count_100, count_500, count_500p]
import matplotlib.pyplot as plt

#%%
#import matplotlib.pyplot as plt
#plt.hist(range(num), lvis_annotations[key])
plt.plot(l_count, range(7))
plt.yticks(range(7), ['<20', '<40', '<60', '<80', '<100', "<500", ">500"])
plt.show()

## select only those categories which have more than 100 objects
select = [k for k in lvis_annotations.keys() if len(lvis_annotations[k])>=10]
select.sort(reverse=True)
annotations = [len(lvis_annotations[l]) for l in select]
annotations.sort(reverse=True)

plt.plot(range(len(select)), annotations)
plt.show()
print(len(select), ': the number of categories which have more than 10 objects')


#%%
''' It might be a good idea to focus on these categories
out of these categories there are some which have way 
too many objects and might cause a bias in the dataset. 
should we make a cutoff on which attributes we shall or shall not use '''
select = [k for k in lvis_annotations.keys() if len(lvis_annotations[k])>=100]

plt.plot(range(len(select)), [len(lvis_annotations[l]) for l in select])
plt.show()
print(len(select), ': the number of categories which have more than 100 objects and less than 300')
print(sum([len(lvis_annotations[l]) for l in select]), f': the total number of objects in {len(select)} categories')

# We can start rendering objects present in these 74 categories in order to form images
# %%

