import numpy as np
import argparse
import math
import os
import random
import sys
import time
import urllib.request
from typing import Tuple
from os.path import join
import bpy
from mathutils import Vector
import glob
import mathutils
import itertools

parser = argparse.ArgumentParser()
parser.add_argument(
    "--object_path",
    type=str,
    required=True,
    help="Path to the object file",
)
parser.add_argument("--output_dir", type=str, default="./views")
parser.add_argument(
    "--engine", type=str, default="BLENDER_EEVEE", choices=["CYCLES", "BLENDER_EEVEE"]
)
parser.add_argument("--textures", action='store_true')
parser.add_argument("--num_images", type=int, default=12)
parser.add_argument("--camera_dist", type=float, default=1.2)
parser.add_argument("--shadows", action='store_true')
parser.add_argument("--bake_ao", action='store_true')
parser.add_argument("--no_specular", action='store_true')
parser.add_argument("--no_shadows", action='store_true')
parser.add_argument("--no_shading", action='store_true')
parser.add_argument("--device_type", type=str)
argv = sys.argv[sys.argv.index("--") + 1 :]
args = parser.parse_args(argv)

context = bpy.context
scene = context.scene
render = scene.render

render.engine = args.engine
render.image_settings.file_format = "JPEG"
render.image_settings.color_mode = "RGB" # hence there are 4 channels, I could just put them as 3 channels then it could be compatible with RESNET
render.resolution_x = 256
render.resolution_y = 256
render.image_settings.compression = 15
render.resolution_percentage = 100
scene.cycles.samples = 32
scene.cycles.filter_width = 0.01
scene.cycles.diffuse_bounces = 1
scene.cycles.glossy_bounces = 1
scene.cycles.transparent_max_bounces = 3
scene.cycles.transmission_bounces = 3
scene.cycles.use_denoising = True
scene.render.film_transparent = True
bpy.ops.object.mode_set(mode='OBJECT')
# Set the render device to GPU
bpy.context.scene.cycles.device = 'GPU'
# Set the compute device type to METAL
bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'METAL'
# Enable all available devices
for device in bpy.context.preferences.addons['cycles'].preferences.devices:
    if device.name == 'Apple M1 Max (GPU)':
            device.use = True

# Print information about available devices
for i, device in enumerate(bpy.context.preferences.addons['cycles'].preferences.devices):
    print(f"Device {i + 1}: {device.name}")

env_maps_dir = 'environment_maps/RENI_HDR/Train/*'
list_env_maps = list(glob.glob(env_maps_dir))

textures_dir = 'textures/dtd/images/*/*.jpg'
list_textures_dir = list(glob.glob(textures_dir)) #maybe this list is too big to iterate

def change_textures_in_scene(list_textures_dir):
    # To do: also include cases where there are no textures on the material
    i = np.random.randint(0, len(list_textures_dir), size=1)[0]
    texture_file = list_textures_dir[i]
    for obj in bpy.context.scene.objects.values():
        if isinstance(obj.data, (bpy.types.Mesh)):
            mat = bpy.data.materials.new(name='newtexture')
            mat.use_nodes = True
            bsdf = mat.node_tree.nodes['Principled BSDF']
            texImage = mat.node_tree.nodes.new('ShaderNodeTexImage')
            texImage.image = bpy.data.images.load(texture_file)
            mat.node_tree.links.new(bsdf.inputs['Base Color'], texImage.outputs['Color'])
            ob = context.view_layer.objects.active
            obj.data.materials[0] = mat
            
def calculate_bounding_box_corners(obj):
    # Get the object's world matrix
    world_matrix = obj.matrix_world
    
    # Initialize a list to store the transformed bounding box corners
    bounding_box_corners_world = []
    
    # Iterate through each bounding box corner vector
    for vector in obj.bound_box:
        # Transform the vector to world space
        world_corner = world_matrix @ vector.to_4d().to_3d()
        bounding_box_corners_world.append(world_corner)
    
    return bounding_box_corners_world

def add_background_image(list_env_maps, i):
    print('Add background image')
    image_path = list_env_maps[i]
    print(image_path)
    c = bpy.context
    world = c.scene.world
    world.use_nodes = True
    nodes = world.node_tree.nodes
    links = world.node_tree.links
    backNode = nodes['Background']
    print(backNode)
    if nodes.find('Environment Texture') == -1:
        envNode = nodes.new('ShaderNodeTexEnvironment')
    else:
        envNode = nodes['Environment Texture']
        
    envNode.location.x = backNode.location.x - 300
    envNode.location.y = backNode.location.y
    envNodeColorOut = envNode.outputs['Color']
    backColIn = backNode.inputs['Color']
    links.new(envNodeColorOut, backColIn)
    bpy.context.scene.render.film_transparent = False
    envNode.image = bpy.data.images.load(image_path)
    
    bpy.context.scene.world.cycles_visibility.diffuse = False
    bpy.context.scene.world.cycles_visibility.glossy = False
    bpy.context.scene.world.cycles_visibility.transmission = False
    bpy.context.scene.world.cycles_visibility.scatter = False
    bpy.ops.object.select_all(action='DESELECT')

    # Select all objects in the current scene
    for obj in bpy.context.scene.objects:
        obj.select_set(True)
    # Loop through selected objects
    for obj in bpy.context.selected_objects:
        # Calculate bounding box center
        bounding_box_corners_world = calculate_bounding_box_corners(obj)
        for corner in bounding_box_corners_world:
            print(corner)
            for corner in bounding_box_corners_world:
                bpy.ops.object.light_add(type='HEMI', location=corner)
                light = bpy.context.object
                light.data.energy = 100  # Adjust intensity as needed
        
        
        
            
        
    

def sample_point_on_sphere(radius: float) -> Tuple[float, float, float]:
    theta = random.random() * 2 * math.pi
    phi = math.acos(2 * random.random() - 1)
    return (
        radius * math.sin(phi) * math.cos(theta),
        radius * math.sin(phi) * math.sin(theta),
        radius * math.cos(phi),
    )

def add_lighting() -> None:
    # delete the default light
    bpy.data.objects["Light"].select_set(True)
    bpy.ops.object.delete()
    # add a new light
    bpy.ops.object.light_add(type="AREA")
    # other options here are POINT, SUN, SPOT, AREA
    light2 = bpy.data.lights["Area"]
    light2.energy = 30000
    bpy.data.objects["Area"].location[2] = 0.3
    bpy.data.objects["Area"].scale[0] = 100
    bpy.data.objects["Area"].scale[1] = 100
    bpy.data.objects["Area"].scale[2] = 100

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

def add_shadows():
    print('Execute add shadows')
    for obj in bpy.context.scene.objects.values():
        if isinstance(obj.data, (bpy.types.Mesh)):
            bpy.context.view_layer.objects.active = obj
            obj.cycles.use_self_shadow = True
            obj.cycles.use_cast_shadows = True
            for material in obj.data.materials:
                material.use_cast_shadows = True
                material.use_cast_buffer_shadows = True  # Enable buffer shadows
                material.use_receive_shadows = True
            for slot in obj.material_slots:
                if slot.material:
                    slot.material.use_nodes = True
                    nodes = slot.material.node_tree.nodes
                    principled_bsdf = nodes.get("Principled BSDF")
                    if principled_bsdf:
                        principled_bsdf.inputs["Shadow"].default_value = 3.0
def remove_shadows():
    print('Executing shadow Removal')
    print('Remove the shadows from the environment texture')
    print('Remove the shadows from the object in the scene')
    c = bpy.context
    world = c.scene.world
    world.use_nodes = True
    nodes = world.node_tree.nodes
    env_texture = None
    if 'Environment Texture' in nodes:
        env_texture = nodes['Environment Texture']
    if env_texture and env_texture.type == 'IMAGE':
        # Disable shadows from the environment texture
        env_texture.use_map_ray_shadow = False
    else:
        print("This script is intended for environment textures.")
        bpy.context.object.visible_shadow = False

    for obj in bpy.context.scene.objects.values():
        if obj.type == 'MESH' and not obj.hide_render:
            obj.visible_shadow = False
            obj.display.show_shadows = False
            obj.active_material.shadow_method = 'NONE'
    # Disable object casting shadows in the 3D viewport

def remove_shading():
    # Don't do the unlinking if there is an image texture node
    # How to do if there is no image texture node
    for material in bpy.data.materials:
        print(material)
        if material and material.use_nodes:
            node_tree = material.node_tree
            material_output_node = None
            image_texture_node = None
            for node in node_tree.nodes:
                if node.type == 'TEX_IMAGE':
                    image_texture_node = node
                    break
            if not image_texture_node:
                continue # Only do this whole operation if there is an image texture node somewhere otherwise don't do it for this material
            
            for node in node_tree.nodes:
                print(node)
                if node.type == 'OUTPUT_MATERIAL':
                    material_output_node = node
                    break
            # Find the Principled BSDF node
            principled_bsdf_node = None
            for node in node_tree.nodes:
                if node.type == 'BSDF_PRINCIPLED':
                    principled_bsdf_node = node
                    break
            # Remove the link between the Principled BSDF node and the Material Output node
            if principled_bsdf_node and material_output_node:
                links = node_tree.links
                for link in links:
                    if link.to_node == material_output_node and link.from_node == principled_bsdf_node:
                        links.remove(link)
            # Add a link between the Image Texture node and the Material Output node
            if image_texture_node and material_output_node:
                    links = node_tree.links
                    link = links.new(image_texture_node.outputs['Color'], material_output_node.inputs['Surface'])


def remove_specular():
    print("Executing Removal of specular")
    principled_bsdf = None
    #bpy.context.scene.world.cycles_visibility.diffuse = False
    #bpy.context.scene.world.cycles_visibility.transmission = False
    bpy.context.scene.world.cycles_visibility.glossy = False

    for mat in bpy.data.materials:
        if not mat.use_nodes:
            mat.specular_intensity = 0
            continue
        for n in mat.node_tree.nodes:
            print(n.type)
            if n.type == 'BSDF_PRINCIPLED':
                n.inputs[7].default_value = 0 # Specular to 0 
                n.inputs[8].default_value = 0 # Specular Tint to 0
                n.inputs[9].default_value = 1 # se the roughness to 1
                print('remove the specularity on the object with the specular tint')
                principled_bsdf = n
            if principled_bsdf:
            # Remove links to the Metallic input
                for link in mat.node_tree.links:
                        if link.to_node == principled_bsdf.inputs["Metallic"]:
                            mat.node_tree.links.remove(link)
                            principled_bsdf.inputs["Metallic"].default_value = 0
                # Remove links to the Roughness input
                for link in mat.node_tree.links:
                        if link.to_node == principled_bsdf.inputs["Roughness"]:
                            mat.node_tree.links.remove(link)
                            principled_bsdf.inputs["Roughness"].default_value = 1
                            
                        
    print('Remove the specularity as well as the specular tint on the material using the principled BSDF')
    
    # Do not these once they have been disabled in the world settings
    """bpy.context.scene.cycles.diffuse_bounces = 1
    bpy.context.scene.cycles.glossy_bounces = 1
    bpy.context.scene.cycles.transmission_bounces = 1
    bpy.context.scene.cycles.transparent_max_bounces = 1
    bpy.context.scene.cycles.max_bounces = 1"""


def save_images(object_file: str) -> None:
    """Saves rendered images of the object in the scene."""
    os.makedirs(args.output_dir, exist_ok=True)
    reset_scene()
    # load the object
    object_uid = os.path.basename(object_file).split(".")[0]
    print(object_file, 'path found')
    load_object(object_file)
    normalize_scene()
    # add_lighting()
    # if this uid has not already been rendered with 12 images
    cam, cam_constraint = setup_camera()
    # create an empty object to track
    empty = bpy.data.objects.new("Empty", None)
    scene.collection.objects.link(empty)
    cam_constraint.target = empty
    if args.bake_ao:
        print('Baking ambient occlusion')
        bpy.context.scene.cycles.ao_bounces = 2  # Number of ambient occlusion bounces
        # Strength of the ambient occlusion effect
        bpy.context.scene.cycles.ao_diffuse = 0.5
        bpy.context.scene.cycles.use_ao = True
        # You can adjust other Ambient Occlusion settings as needed
        # For example, you can set the samples:
        bpy.context.scene.cycles.ao_samples = 128
        # Render your scene with Ambient Occlusion
        bpy.ops.render.render(animation=False)
        os.makedirs(args.output_dir, exist_ok=True)

    cam, cam_constraint = setup_camera()
    # create an empty object to track
    empty = bpy.data.objects.new("Empty", None)
    scene.collection.objects.link(empty)
    cam_constraint.target = empty
    angles = np.random.uniform(0, 360, size=args.num_images-5) # just for visualization can I set the angles to be non random -- change this later on
    #angles = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270] # all angles should be the same for all the renderings
    print(len(angles)) # the length of the angles is 10
    for i in range(args.num_images):
        # set the camera position
        if args.textures == True:
            change_textures_in_scene(list_textures_dir)  # only
        # change the env maps for each image, but make sure the env maps are consistent for each dataset
        #add_environment_map(list_env_maps, i)
        add_background_image(list_env_maps,i)
        #add_background_map(list_env_maps, i)
        #add_area_light(intensity=0.5)
        #add_ambient_illumination(list_env_maps, i, intensity=0.5)
        if args.shadows:
            print('Adding shadows')
            add_shadows()
        if args.no_shadows:
            print('Removing shadows')
            remove_shadows()
        if args.no_shading:
            print('Removing shading')
            remove_shading()
        if args.no_specular:
            print('Removing specular')
            remove_specular()
            # if it set to false
        theta = (i / args.num_images) * math.pi * 2
        #theta = np.pi/4
        j = np.random.randint(0, len(angles), size=1)[0]
        phi = angles[j]
        #phi = np.pi/2
        point = (
            args.camera_dist * math.sin(phi) * math.cos(theta),
            args.camera_dist * math.sin(phi) * math.sin(theta),
            args.camera_dist * math.cos(phi),
        )
        cam.location = point
        # render the image
        render_path = os.path.join(args.output_dir, object_uid, f"{i:03d}.png")
        scene.render.filepath = render_path
        bpy.ops.render.render(write_still=True)

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

def download_object(object_url: str) -> str:
    """Download the object and return the path."""
    # uid = uuid.uuid4()
    print('downloading the object here')
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
        if args.object_path.startswith("http"):
            print('the object name starts with http')
            local_path = download_object(args.object_path)
        else:
            local_path = args.object_path    
        object_uid = os.path.basename(local_path)
        print(object_uid)
        path = join(args.output_dir, object_uid)
        if os.path.exists(path):
            print('rendering done already')
        if not os.path.exists(path):
            save_images(local_path)
        end_i = time.time()
        print("Finished", local_path, "in", end_i - start_i, "seconds")
        # delete the object if it was downloaded
        if args.object_path.startswith("http"):
            os.remove(local_path)
    except Exception as e:
        print("Failed to render", args.object_path)
        print(e)
