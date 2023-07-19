import bpy
import os

filename = os.path.join(os.path.dirname(bpy.data.filepath), "scripts/blender_script_2.py")
exec(compile(open(filename).read(), filename, 'exec'))
