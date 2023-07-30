import blenderproc as bproc
import glob
import numpy as np
import bpy
import math
from mathutils import Vector


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
    return obj

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

for object in glob.glob('objects/glbs/*/*'):
    bproc.utility.reset_keyframes()

    object_name = object.split('/')[-1][:-4]
    print(object_name)

    scene = bproc.loader.load_obj(object)
    light = bproc.types.Light()
    light.set_location([2, -2, 0])
    light.set_energy(300)
    normalize_scene(scene)
    # Set the camera to be in front of the object
    # Find point of interest, all cam poses should look towards it
    poi = bproc.object.compute_poi(scene)
    # Sample random camera location above objects
    # Find point of interest, all cam poses should look towards it
    # Sample five camera poses
    for i in range(5):
    # Sample random camera location above objects
        location = np.random.uniform([-5, -5, -5], [5, 5, 5])
        # Compute rotation based on vector going from location towards poi
        rotation_matrix = bproc.camera.rotation_from_forward_vec(poi - location, inplane_rot=np.random.uniform(-0.3, 0.3))
        # Add homog cam pose based on location an rotation
        cam2world_matrix = bproc.math.build_transformation_mat(location, rotation_matrix)
        bproc.camera.add_camera_pose(cam2world_matrix)

    # Render the scene
    data = bproc.renderer.render()
    # Write the rendering into an hdf5 file
    bproc.writer.write_hdf5(f'output/{object_name}', data)
    #bproc.writer.write_hdf5(f"output/{object_name}", data)
    bproc.clean_up()


