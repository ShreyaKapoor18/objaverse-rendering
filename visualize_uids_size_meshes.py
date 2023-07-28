import blenderproc as bproc
import glob
import numpy as np

bproc.init()
for object in glob.glob('objects/glbs/*/*'):
    object_name = object.split('/')[-1][:-4]
    print(object_name)
    print(object)

    obj = bproc.loader.load_obj(object)
    print(obj)
    light = bproc.types.Light()
    light.set_location([2, -2, 0])
    light.set_energy(300)

    # Set the camera to be in front of the object
    cam_pose = bproc.math.build_transformation_mat([0, -5, 0], [np.pi / 2, 0, 0])
    bproc.camera.add_camera_pose(cam_pose)
    bproc.camera.set_resolution(512, 512)

    # Render the scene
    data = bproc.renderer.render()

    # Write the rendering into an hdf5 file
    bproc.writer.write_gif_animation(f"output/{object_name}", data)
    bproc.writer.write_hdf5(f"output/{object_name}", data)



