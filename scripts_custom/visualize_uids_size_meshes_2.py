import blenderproc as bproc
import glob
import numpy as np
import bpy
import math
from mathutils import Vector
from mathutils import Matrix
from mathutils import Vector
import mathutils

bproc.init()
def normalize_scene(scene):
    bbox_min, bbox_max = scene_bbox(scene)
    scale = 1 / max(bbox_max - bbox_min)
    for obj in scene_root_objects(scene):
        obj.blender_obj.scale = obj.blender_obj.scale * scale
    # Apply scale to matrix_world.
    bpy.context.view_layer.update()
    bbox_min, bbox_max = scene_bbox(scene)
    offset = -(bbox_min + bbox_max) / 2
    for obj in scene_root_objects(scene):
        obj.blender_obj.matrix_world.translation += offset
    bpy.ops.object.select_all(action="DESELECT")

def scene_bbox(scene, single_obj=None, ignore_matrix=False):
    bbox_min = (math.inf,) * 3
    bbox_max = (-math.inf,) * 3
    found = False
    for obj in scene_meshes(scene) if single_obj is None else [single_obj]:
        found = True
        for coord in obj.blender_obj.bound_box:
            coord = Vector(coord)
            if not ignore_matrix:
                coord = obj.blender_obj.matrix_world @ coord
            bbox_min = tuple(min(x, y) for x, y in zip(bbox_min, coord))
            bbox_max = tuple(max(x, y) for x, y in zip(bbox_max, coord))
    if not found:
        raise RuntimeError("no objects in scene to compute bounding box for")
    return Vector(bbox_min), Vector(bbox_max)


def scene_root_objects(scene):
    for obj in scene:
        if not obj.blender_obj.parent:
            yield obj
def scene_meshes(scene):
    for obj in scene:
        print(dir(obj))
        if isinstance(obj.blender_obj.data, (bpy.types.Mesh)):
            yield obj

import bpy
import mathutils

def set_camera_to_view_bounding_box(bbox_min, bbox_max):
    # Step 1: Calculate the bounding box center and size
    bounding_box_center = (bbox_min + bbox_max) / 2
    bounding_box_size = bbox_max - bbox_min
    
    # Step 2: Calculate the camera position and orientation based on the bounding box
    camera_distance = max(bounding_box_size) * 1.5  # Add some padding
    camera_position = bounding_box_center + mathutils.Vector((camera_distance, -camera_distance, camera_distance))
    camera_look_at = bounding_box_center
    
    # Step 3: Set the camera's location and rotation
    camera = bpy.data.objects.get("Camera")  # Assuming the camera's name is "Camera"
    if not camera:
        print("Camera not found.")
        return
    
    camera.location = camera_position
    camera.rotation_euler = (mathutils.Vector(camera_look_at) - mathutils.Vector(camera_position)).to_track_quat('Z', 'Y').to_euler()
    camera.rotation_euler.x += math.radians(90)  # Adjust camera orientation
    
    # Optional: Set camera focal length and sensor size
    camera.data.lens = 35  # Adjust the focal length as needed
    camera.data.sensor_width = 32  # Adjust the sensor size as needed (in millimeters)
    
    # Get camera properties
    focal_length_mm = camera.data.lens
    sensor_width_mm = camera.data.sensor_width
    sensor_height_mm = camera.data.sensor_height
    resolution_x = bpy.context.scene.render.resolution_x
    resolution_y = bpy.context.scene.render.resolution_y

    # Calculate the K matrix
    focal_length_pixels = focal_length_mm / sensor_width_mm * resolution_x
    aspect_ratio = resolution_x / resolution_y
    principal_point_x = resolution_x / 2
    principal_point_y = resolution_y / 2

    K_matrix = [
        [focal_length_pixels, 0, principal_point_x],
        [0, focal_length_pixels * aspect_ratio, principal_point_y],
        [0, 0, 1]
    ]

    camera_to_world_matrix = camera.matrix_world
    # Update the scene
    bpy.context.view_layer.update()
    
    return camera, camera_to_world_matrix, K_matrix




for object in glob.glob('objects/glbs/*/*'):
    bproc.utility.reset_keyframes()

    object_name = object.split('/')[-1][:-4]
    print(object_name)

    scene = bproc.loader.load_obj(object)
    vec1, vec2 = scene_bbox(scene)

    light = bproc.types.Light()
    light.set_location([2, -2, 0])
    light.set_energy(300)
    # Set the camera to be in front of the objet
    normalize_scene(scene)

    camera, camera_to_world_matrix, K_matrix = set_camera_to_view_bounding_box(vec1, vec2)
    #bproc.camera.set_intrinsics_from_K_matrix(K_matrix, 512, 512)
    # Set the camera to be in front of the object
    vecs = [[0, -2, 0], [-2, 0, 0], [0,0,-2]]
    vec2 = [[ np.pi/2, 0, 0], [0, np.pi/2, 0], [0, 0, np.pi/2]]
    for vec in vecs:
        cam_pose = bproc.math.build_transformation_mat(vec, [np.pi / 2, 0, 0])
        bproc.camera.add_camera_pose(cam_pose)

    # Render the scene
    data = bproc.renderer.render()
    # Write the rendering into an hdf5 file
    bproc.writer.write_gif_animation(f'output/{object_name}', data)
    bproc.writer.write_hdf5(f"output/{object_name}", data)
    bproc.clean_up()
    


