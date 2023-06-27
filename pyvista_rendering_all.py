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



parser = argparse.ArgumentParser()
parser.add_argument(
    "--object_path",
    type=str,
    required=True,
    help="Path to the object file",
)
parser.add_argument("--output_dir", type=str, default="./views")
parser.add_argument("--lighting", type=str, default="none")

def load_data(file_path):
    mesh = pv.read(file_path)
    return mesh


def load_background(background_file: str) -> None:
    pl = pv.plotter()
    pv.add_background_image()

def add_texture():
    surf.texture_map_to_plane(inplace=True)
    surf.plot(texture=tex)

def add_file():

def add_lighting(lighting: str) -> None:
    """
    Lighting types are here:
    render objects with different types
    of lighting. All types of lighting 
    should be used

    light_type


    """
    plotter= pv.Plotter(lighting="none", window_size=(1000, 1000))
    light = pv.Light()
    plotter.add_mesh(mesh, color='white', smooth_shading=True)
    light = pv.Light()
    light.set_direction_angle(30, -20)
    plotter.add_light(light)
    plotter.show()

def add_shadows():
    mesh = examples.download_dragon()

def plot_mesh(mesh):
    plotter = pv.Plotter()
    plotter.add_mesh(mesh)
    plotter.camera_position = 'xy'
    plotter.background_color = 'white'
    plotter.show()



def save_plot(mesh, file_name):
    plotter = pv.Plotter()
    plotter.add_mesh(mesh)
    plotter.camera_position = 'xy'
    plotter.background_color = 'white'
    plotter.save_image(file_name)


def main():
    file_path = 'path/to/mesh.obj'
    output_file = 'output.png'

    mesh = load_data(file_path)
    plot_mesh(mesh)
    save_plot(mesh, output_file)

pv.global_theme.smooth_shading = True

if __name__ == '__main__':
    main()