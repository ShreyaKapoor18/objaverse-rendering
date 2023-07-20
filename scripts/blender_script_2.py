import blenderproc as bproc
"""Blender script to render images of 3D models.

This script is used to render images of 3D models. It takes in a list of paths
to .glb files and renders images of each model. The images are from rotating the
object around the origin. The images are saved to the output directory.

Example usage:
    blender -b -P blender_script.py -- \
        --object_path my_object.glb \
        --output_dir ./views \
        --engine CYCLES \
        --scale 0.8 \
        --num_images 12 \
        --camera_dist 1.2

Here, input_model_paths.json is a json file containing a list of paths to .glb.
"""
import numpy as np
import argparse
import math
import os
import random
import sys
import time
import urllib.request
from typing import Tuple

import bpy
from mathutils import Vector
import glob


context = bpy.context
scene = context.scene
render = scene.render

render.engine = "CYCLES"
render.image_settings.file_format = "PNG"
render.image_settings.color_mode = "RGBA" # hence there are 4 channels, I could just put them as 3 channels then it could be compatible with RESNET
render.resolution_x = 512
render.resolution_y = 512
render.resolution_percentage = 100

scene.cycles.device = "GPU"
scene.cycles.samples = 32
scene.cycles.filter_width = 0.01
scene.cycles.use_denoising = True
scene.render.film_transparent = True

env_maps_dir = 'RENI_HDR/Train/*'
list_env_maps = list(glob.glob(env_maps_dir))
print(list_env_maps)

textures_dir = 'textures/*'
list_textures_dir = list(glob.glob(textures_dir))

def change_textures_in_scene(textures_dir):
    # To do: also include cases where there are no textures on the material
    i = np.random.randint(len(textures_dir))
    texture_file = textures_dir[i]
    for obj in bpy.context.scene.objects.values():
        if isinstance(obj.data, (bpy.types.Mesh)):
            mat = bpy.data.materials.new(name='newtexture')
            mat.use_nodes = True
            bsdf = mat.node_tree.nodes['Principled BSDF']
            texImage = mat.node_tree.nodes.new('ShaderNodeTexImage')
            texImage.image = bpy.data.images.load(texture_file)
            mat.node_tree.links.new(bsdf.inputs['Base Color'], texImage.outputs['Color'])

            ob = context.view_layer.objects.active
            if ob.data.materials:
                ob.data.materials[0] = mat
            else:
                ob.data.materials.append(mat)


# Change the ViewPort Shading to RENDERED    
for area in bpy.context.screen.areas: 
    if area.type == 'VIEW_3D':
        for space in area.spaces: 
            if space.type == 'VIEW_3D':
                space.shading.type = 'RENDERED'


def rotate_meshes_in_scene():
    # Select the mesh object you want to rotate
     for obj in bpy.context.scene.objects.values():
        # some error in this function
        if isinstance(obj.data, (bpy.types.Mesh)):
            print("reached here")
            rotation_angle = np.random.uniform(0, 360)
            axeses = ['X', 'Y', 'Z']
            i = np.random.randint(3)
            #bpy.data.objects[mesh].select_set(True)
            # Set the rotation values
            rotation_angle = math.radians(rotation_angle) # Replace with the desired rotation angle in degrees
            rotation_axis = axeses[i] # Replace with the desired rotation axis (X, Y, Z)
            print('also here')
            # Get the active object and enter Edit Mode
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='EDIT')
            print('error here')
            # Rotate the mesh in Edit Mode
            bpy.ops.transform.rotate(value=45, orient_axis=axeses[i])

             # Exit Edit Mode and update the scene
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.context.view_layer.update()

def add_environment_map(list_env_maps):
    # Create or retrieve the world
    i = np.random.randint(len(list_env_maps))
    image_path = list_env_maps[i]
    print(image_path)

    c = bpy.context
    world = c.scene.world
    world.use_nodes = True
    
    nodes = world.node_tree.nodes
    links = world.node_tree.links


    backNode = nodes['Background']

    if nodes.find('Environment Texture') == -1:
        envNode = nodes.new("ShaderNodeTexEnvironment")
    else:
        envNode = nodes['Environment Texture']

    envNode.location.x = backNode.location.x-300
    envNode.location.y = backNode.location.y

    envNodeColorOut = envNode.outputs['Color']
    backColIn = backNode.inputs['Color']
    links.new(envNodeColorOut, backColIn)
    bpy.context.scene.render.film_transparent = False
    envNode.image = bpy.data.images.load(image_path)
    image = bpy.data.images.load(image_path)


def sample_point_on_sphere(radius: float) -> Tuple[float, float, float]:
    theta = random.random() * 2 * math.pi
    phi = math.acos(2 * random.random() - 1)
    return (
        radius * math.sin(phi) * math.cos(theta),
        radius * math.sin(phi) * math.sin(theta),
        radius * math.cos(phi),
    )

def reset_scene() -> None:
    """Resets the scene to a clean state."""
    # delete everything that isn't part of a camera or a light
    for obj in bpy.data.objects:
        if obj.type not in {"CAMERA", "LIGHT"}:
            bpy.data.objects.remove(obj, do_unlink=True)
    # delete all the materials
    for material in bpy.data.materials:
        bpy.data.materials.remove(material, do_unlink=True)
    # delete all the textures
    for texture in bpy.data.textures:
        bpy.data.textures.remove(texture, do_unlink=True)
    # delete all the images
    for image in bpy.data.images:
        bpy.data.images.remove(image, do_unlink=True)


# load the glb model
def load_object(object_path: str) -> None:
    """Loads a glb model into the scene."""
    if object_path.endswith(".glb"):
        bpy.ops.import_scene.gltf(filepath=object_path, merge_vertices=True)
    elif object_path.endswith(".fbx"):
        bpy.ops.import_scene.fbx(filepath=object_path)
    else:
        raise ValueError(f"Unsupported file type: {object_path}")


def scene_bbox(single_obj=None, ignore_matrix=False):
    bbox_min = (math.inf,) * 3
    bbox_max = (-math.inf,) * 3
    found = False
    for obj in scene_meshes() if single_obj is None else [single_obj]:
        found = True
        for coord in obj.bound_box:
            coord = Vector(coord)
            if not ignore_matrix:
                coord = obj.matrix_world @ coord
            bbox_min = tuple(min(x, y) for x, y in zip(bbox_min, coord))
            bbox_max = tuple(max(x, y) for x, y in zip(bbox_max, coord))
    if not found:
        raise RuntimeError("no objects in scene to compute bounding box for")
    return Vector(bbox_min), Vector(bbox_max)


def scene_root_objects():
    for obj in bpy.context.scene.objects.values():
        if not obj.parent:
            yield obj


def scene_meshes():
    for obj in bpy.context.scene.objects.values():
        if isinstance(obj.data, (bpy.types.Mesh)):
            yield obj


def normalize_scene():
    bbox_min, bbox_max = scene_bbox()
    scale = 1 / max(bbox_max - bbox_min)
    for obj in scene_root_objects():
        obj.scale = obj.scale * scale
    # Apply scale to matrix_world.
    bpy.context.view_layer.update()
    bbox_min, bbox_max = scene_bbox()
    offset = -(bbox_min + bbox_max) / 2
    for obj in scene_root_objects():
        obj.matrix_world.translation += offset
    bpy.ops.object.select_all(action="DESELECT")


def setup_camera():
    cam = scene.objects["Camera"]
    cam.location = (0, 1.2, 0)
    cam.data.lens = 35
    cam.data.sensor_width = 32
    cam_constraint = cam.constraints.new(type="TRACK_TO")
    cam_constraint.track_axis = "TRACK_NEGATIVE_Z"
    cam_constraint.up_axis = "UP_Y"
    return cam, cam_constraint


def save_images(object_file: str) -> None:
    """Saves rendered images of the object in the scene."""
    os.makedirs("./views", exist_ok=True)
    reset_scene()
    # load the object
    load_object(object_file)
    object_uid = os.path.basename(object_file).split(".")[0]
    normalize_scene()
    # dont need to add lighting due to env maps
    cam, cam_constraint = setup_camera()
    # create an empty object to track
    empty = bpy.data.objects.new("Empty", None)
    scene.collection.objects.link(empty)
    cam_constraint.target = empty
    camera_dist = 2
    num_images = 12
    for i in range(num_images):
        # set the camera position
        scene.cycles.diffuse_bounces = np.random.randint(1,4)
        scene.cycles.glossy_bounces = np.random.randint(1,4)
        scene.cycles.transparent_max_bounces = np.random.randint(1,4)
        scene.cycles.transmission_bounces = np.random.randint(1,3)
        theta = (i / num_images) * math.pi * 2
        rotate_meshes_in_scene()
        add_environment_map(list_env_maps)
        if i!=0:
            change_textures_in_scene(list_textures_dir)
        phi = math.radians(60)
        point = (
            camera_dist * math.sin(phi) * math.cos(theta),
            camera_dist * math.sin(phi) * math.sin(theta),
            camera_dist * math.cos(phi),
        )
        cam.location = point
        # render the image
        render_path = os.path.join('./views', object_uid, f"{i:03d}.png")
        scene.render.filepath = render_path
        bpy.ops.render.render(write_still=True)


def download_object(object_url: str) -> str:
    """Download the object and return the path."""
    # uid = uuid.uuid4()
    uid = object_url.split("/")[-1].split(".")[0]
    tmp_local_path = os.path.join("tmp-objects", f"{uid}.glb" + ".tmp")
    local_path = os.path.join("tmp-objects", f"{uid}.glb")
    # wget the file and put it in local_path
    os.makedirs(os.path.dirname(tmp_local_path), exist_ok=True)
    urllib.request.urlretrieve(object_url, tmp_local_path)
    os.rename(tmp_local_path, local_path)
    # get the absolute path
    local_path = os.path.abspath(local_path)
    return local_path


if __name__ == "__main__":
    try:
        start_i = time.time()
        local_path = "objects/flowerpot.glb"
        save_images(local_path)
        end_i = time.time()
        print("Finished", local_path, "in", end_i - start_i, "seconds")
        # delete the object if it was downloaded
    except Exception as e:
        print("Failed to render", local_path)
        print(e)