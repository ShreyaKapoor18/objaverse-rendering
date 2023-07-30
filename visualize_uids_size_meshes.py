import blenderproc as bproc
import glob
import numpy as np
import bpy
import math
from MathUtils import Vector

bproc.init()

def normalize_scene(scene):
    bbox_min, bbox_max = scene_bbox()
    scale = 1 / max(bbox_max - bbox_min)
    for obj in scene_root_objects():
        obj.scale = obj.scale * scale
    # Apply scale to matrix_world.
    bpy.context.view_layer.update()
    bbox_min, bbox_max = scene_bbox(scene)
    offset = -(bbox_min + bbox_max) / 2
    for obj in scene_root_objects(scene):
        obj.matrix_world.translation += offset
    bpy.ops.object.select_all(action="DESELECT")
    return obj

def scene_bbox(scene, single_obj=None, ignore_matrix=False):
    bbox_min = (math.inf,) * 3
    bbox_max = (-math.inf,) * 3
    found = False
    for obj in scene_meshes(scene) if single_obj is None else [single_obj]:
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


def scene_root_objects(scene):
    for obj in scene:
        if not obj.parent:
            yield obj

def scene_meshes(scene):
    for obj in scene:
        if isinstance(obj.data, (bpy.types.Mesh)):
            yield obj

for object in glob.glob('objects/glbs/*/*'):
    object_name = object.split('/')[-1][:-4]
    print(object_name)
    print(object)

    scene = bproc.loader.load_obj(object)
    light = bproc.types.Light()
    light.set_location([2, -2, 0])
    light.set_energy(300)
    normalize_scene(scene)
    # Set the camera to be in front of the object
    cam_pose = bproc.math.build_transformation_mat([0, -5, 0], [np.pi / 2, 0, 0])
    bproc.camera.add_camera_pose(cam_pose)
    bproc.camera.set_resolution(512, 512)

    # Render the scene
    data = bproc.renderer.render()
    # Write the rendering into an hdf5 file
    bproc.writer.write_gif_animation(f"output/{object_name}", data)
    bproc.writer.write_hdf5(f"output/{object_name}", data)



