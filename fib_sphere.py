bl_info = {
    "name": "Fibonacci Sphere",
    "author": "Ben Wendt",
    "version": (0, 0, 1),
    "blender": (2, 79, 0),
    "location": "VIEW3D > ADD > Mesh",
    "description": "Add a Fibonacci Sphere with an evenly distributed number of vertices",
    "warning": "",
    "wiki_url": "https://github.com/rbwendt/blender-add-mesh-fibonacci-sphere",
    "tracker_url": "",
    "category": "Add Mesh"}

from numpy import array, arange, pi, sin, cos, arccos
from math import sqrt
import bpy
import bmesh
from bpy import context
from bpy_extras import object_utils
from bpy.props import IntProperty

def fib_sphere(n):
    golden_ratio = (1 + 5**0.5)/2
    i = arange(0, n)
    theta = 2 *pi * i / golden_ratio
    phi = arccos(1 - 2*(i+0.5)/n)
    coords = array([cos(theta) * sin(phi), sin(theta) * sin(phi), cos(phi)])

    ob_name = 'Fibonacci_Sphere'
    me = bpy.data.meshes.new(ob_name + " Mesh")
    ob = bpy.data.objects.new(ob_name, me)

    me.from_pydata(coords.transpose(), [], [])

    bm = bmesh.new()
    bm.from_mesh(me)
    bmesh.ops.convex_hull(bm, input=bm.verts)
    bm.to_mesh(me)
    me.update()
    bpy.context.collection.objects.link(ob)

class FibonacciSphere(bpy.types.Operator, object_utils.AddObjectHelper):
    bl_idname = "mesh.fibonacci_sphere_add"
    bl_label = "Fibonacci Sphere"
    bl_description = "Add a Fibonacci Sphere with an evenly distributed number of vertices"
    bl_options = {'REGISTER', 'UNDO'}
    
    vertices: IntProperty(
        name="Number of vertices",
        default = 200,
        min = 4, max = 10000,
        description="Number of vertices"
    )
    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'vertices', expand=True)			 
        #if self.change == False:
    @classmethod
    def poll(cls, context):
        return context.scene is not None

    def execute(self, context):
        if context.selected_objects != [] and context.active_object and \
            ('Fibonacci' in context.active_object.data.keys()) and (self.change == True):
            obj = context.active_object
            bpy.context.collection.objects.unlink(obj)    
        fib_sphere(self.vertices)
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return self.execute(context)

        
def menu_func(self, context):
    self.layout.operator(FibonacciSphere.bl_idname, icon='MESH_ICOSPHERE')
def register():
    bpy.utils.register_class(FibonacciSphere)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)
def unregister():
    bpy.utils.unregister_class(FibonacciSphere)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)
    
    
if __name__ == '__main__':
    print('register it')
    register()
    #fib_sphere(222)