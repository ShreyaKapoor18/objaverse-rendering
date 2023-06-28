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
import pyshtools

def load_data(file_path)-> None:
    """
    Load the data from a particular file path
    """
    mesh = pv.read(file_path)
    return mesh
#%%
def load_background(mesh, background_file: str) -> None:
    """
    Add a background image to a particular plotting session
    """
    plotter = pv.Plotter()
    plotter.add_mesh(mesh)
    plotter.add_background_image(background_file)
    return plotter
#%%

def add_texture(mesh):
    """
    Add texture map to the mesh of the object
    """
    mesh.texture_map_to_plane(inplace=True)
    mesh.plot(texture=tex)


def change_lighting_on_object(mesh, light_direction=(1, 1, 1), light_color='white', light_intensity=1.0):
    plotter = pv.Plotter()
    plotter.add_mesh(mesh)
    plotter.add_directional_light(direction=light_direction, color=light_color, intensity=light_intensity)
    plotter.camera_position = 'xy'
    plotter.background_color = 'white'

def change_transparency(mesh, opacity=1.0):
    mesh.opacity = opacity
    plotter = pv.Plotter()
    plotter.add_mesh(mesh)
    plotter.camera_position = 'xy'
    plotter.background_color = 'white'
    plotter.show()


def change_shading_on_object(mesh, shading='phong'):
    plotter = pv.Plotter()
    plotter.add_mesh(mesh)
    plotter.set_shading(shading)
    plotter.camera_position = 'xy'
    plotter.background_color = 'white'
    plotter.show()
    

def add_lighting(lighting: str) -> None:
    """
    Lighting types are here:
    render objects with different types
    of lighting. All types of lighting 
    should be used
    """
    plotter= pv.Plotter(lighting="none", window_size=(1000, 1000))
    light = pv.Light()
    plotter.add_mesh(mesh, color='white', smooth_shading=True)
    light = pv.Light()
    light.set_direction_angle(30, -20)
    plotter.add_light(light)
    plotter.show()

def plot_mesh(mesh):
    """
    Plot the particular mesh you have
    """
    plotter.add_mesh(mesh)
    plotter.camera_position = 'xy'
    plotter.background_color = 'white'
    plotter.show()

def save_plot(mesh, file_name):
    plotter.add_mesh(mesh)
    plotter.camera_position = 'xy'
    plotter.background_color = 'white'
    plotter.save_image(file_name)


def spherical_harmonics():
    # Step 1: Compute or obtain spherical harmonic coefficients
    # Example: Generate random coefficients for demonstration
    coeffs = np.random.randn(9)

    # Step 2: Generate a spherical mesh
    sphere = pv.Sphere(radius=1, theta_resolution=100, phi_resolution=100)

    # Step 3: Apply lighting to the mesh vertices
    # Example: Compute lighting values based on spherical harmonics
    lighting_values = shtools.SHExpandDH(coeffs, sampling=2)

    # Step 4: Visualize the mesh with lighting
    sphere['Lighting'] = lighting_values
    sphere.plot(smooth_shading=True, lighting='Lighting')

