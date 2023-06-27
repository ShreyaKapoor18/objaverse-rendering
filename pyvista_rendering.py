#%%
from pyvista import examples
import pyvista as pv
import cv2
import OpenEXR, array
import os
import cv2
#%%
pl = pv.Plotter()
filename = '/Users/shreya/Documents/000-000/78e7d5afe771428d958b1359c0b6e00b.glb'
os.environ["OPENCV_IO_ENABLE_OPENEXR"]="1"

background_file = cv2.imread('/Users/shreya/blender/objaverse-rendering/00002.exr', cv2.COLOR_BGR2RGB | cv2.IMREAD_ANYDEPTH)
cv2.imwrite('00002.png', background_file)
mesh = pv.read(filename)

#%%
actor = pl.add_mesh(mesh, smooth_shading=True)
pl.add_background_image('/Users/shreya/blender/objaverse-rendering/00002.png')
pl.show()

#%%
cubemap = examples.download_sky_box_cube_map()
p = pv.Plotter()
p.add_actor(cubemap.to_skybox())
p.set_environment_texture(cubemap)  # For reflecting the environment off the mesh
p.add_mesh(mesh, color='linen')

# Define a nice camera perspective
cpos = [(-323.40, 66.09, 1000.61), (0.0, 0.0, 0.0), (0.018, 0.99, -0.06)]

p.show(cpos=cpos)

# %%
cubemap

# %%
pl.save_graphic('00002.svg')
# %%
renderer = pl.renderer
renderer.add_light 
renderer.set_background
renderer.view_isometric
renderer.view_vector
renderer.add_light
renderer.add

# %%
from pyvista import demos
pl = demos.orientation_plotter()
pl.enable_3_lights()
pl.show()

pl = demos.orientation_plotter()
pl.show()

plotter = pv.Plotter()
light_types = [light.light_types for light in plotter.renderer.renderer.lights]
pv.plotting._ALL_PLOTTERS.clear()
light_types
#%%
mesh = examples.download_st_helens().warp_by_scalar()
plotter = pv.Plotter()
plotter.add_mesh(mesh, color='white')
plotter.show()
#%%
plotter = pv.Plotter(lighting='three lights')
plotter.add_mesh(mesh, color='white')
plotter.show()

# %%
pl.enable_depth_of_field()
pl.show()

# %%
# apply textures -- to the surfaace

tex = examples.download_masonry_texture()

surf = mesh
surf.texture_map_to_plane(inplace=True)

surf.plot(texture=tex)
# %%
# Volume rendering
vol = mesh
cpos = [(-381.74, -46.02, 216.54), (74.8305, 89.2905, 100.0), (0.23, 0.072, 0.97)]

vol.plot(volume=True, cmap="bone", cpos=cpos)
# %%
import pyvista as pv
from pyvista import examples

vol = examples.download_knee_full()
vol
# %%
import pyvista as pv
from pyvista import examples