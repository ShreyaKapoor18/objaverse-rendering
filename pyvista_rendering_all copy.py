#%%
import glob
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
import pyvista as pv
from os.path import join
from pyvista import examples
import cv2
import meshio
from os.path import join
import os
#%%
"""

To do:
Add a loop for different rotations of the object/ different poses
Add another loop for textures applied to the object
Add reflectivity/ metalicness/ luminosity of the object
"""
file_path = '/Users/shreya/Documents/000-000/0a3dd21606a84a449bb22f597c34bab7.glb'
backgrounds = '/Users/shreya/Downloads/RENI_HDR/Test'
output_dir = './out'
os.environ["OPENCV_IO_ENABLE_OPENEXR"]="1"
if not os.path.exists(output_dir):
    os.mkdir(output_dir)

#%%
for background in glob.glob(join(backgrounds, '*.exr')):
    pl = pv.Plotter(lighting='none')
    mesh = pv.read(file_path)
    bg_image = cv2.imread(background, cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH | cv2.IMREAD_UNCHANGED) 
    fname = background.split('.exr')[0] + ".png"
    print(fname)
    cv2.imwrite(fname, cv2.cvtColor(255.0*bg_image, cv2.COLOR_RGB2BGR)) 
    pl.add_background_image(fname)
    for shading in ['smooth', 'flat']:
        if shading == 'smooth':
            actor = pl.add_mesh(mesh, smooth_shading=True)
        elif shading == 'flat':
            actor = pl.add_mesh(mesh)
        for lighting in ['head_light', 'camera-light', 'scene-light']:
            light = pv.Light()
            if lighting == 'head-light':
                light.set_headlight()
            elif lighting == 'camera-light':
                light.set_camera_light()
            elif lighting == 'scene-light':
                light.set_scene_light()
            pl.add_light(light)
            bgname = background.split(backgrounds + "/")[1][:-4]
            pl.show(screenshot=join(output_dir, f'{shading}_{bgname}_{lighting}.png'))
            pl=pv.Plotter()
        

# %%
