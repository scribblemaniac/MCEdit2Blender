import bpy
import mathutils
from Block import Block

class Stairs(Block):
    """Stair block with a single texture"""
    
    def make(self, x, y, z, metadata):
        obj = self.makeObject(x, y, z, metadata)
        self.applyMaterial(obj, metadata)
    
    def makeObject(self, x, y, z, metadata):
        mesh = bpy.data.meshes.new(name="Block")
        mesh.from_pydata([[0.5, 0.5, 0.5], [0.5, -0.5, 0.5], [0.5, 0.5, -0.5], [0.5, -0.5, -0.5], [0, 0.5, 0.5], [0, -0.5, 0.5], [0, 0.5, 0], [0, -0.5, 0], [-0.5, 0.5, 0], [-0.5, -0.5, 0], [-0.5, 0.5, -0.5], [-0.5, -0.5, -0.5]], [], [[0,1,3,2], [0,2,10,8,6,4], [1,3,11,9,7,5], [0,1,5,4], [4,5,7,6], [6,7,9,8], [8,9,11,10], [2,3,11,10]])
        mesh.update()
        
        obj = bpy.data.objects.new("Block", mesh)
        obj.location.x = x + 0.5
        obj.location.y = y + 0.5
        obj.location.z = z + 0.5
        bpy.context.scene.objects.link(obj)

        activeObject = bpy.context.scene.objects.active
        bpy.context.scene.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.object.editmode_toggle()
        bpy.context.scene.objects.active = activeObject
        
        self.makeUVMap(obj, metadata)
        
        obj.rotation_euler.y = 3.1415927410125732 * (metadata >> 2 & 1)
        obj.rotation_euler.z = 3.1415927410125732 * ((metadata & 1) + (metadata >> 2 & 1)) - 1.5707963705062866 * (metadata >> 1 & 1)
        bpy.ops.object.select_pattern(pattern=obj.name, extend=False)
        bpy.ops.object.transform_apply(rotation=True)
        obj.select = False
        
        return obj
    
    def makeUVMap(self, obj, metadata):
        maps = [[0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0.5, 0.5, 0.5, 0.5, 1, 1, 1, 0.5, 1, 0.5, 0.5, 0, 0.5, 0, 0, 1, 0, 1, 1, 0.5, 1, 0.5, 0, 1, 0, 0, 1, 0, 0.5, 1, 0.5, 1, 1, 0.5, 1, 0, 1, 0, 0, 0.5, 0, 0, 0.5, 0, 0, 1, 0, 1, 0.5, 1, 1, 1, 0, 0, 0, 0, 1], [1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0.5, 0.5, 0.5, 0.5, 1, 0, 1, 0.5, 1, 0.5, 0.5, 1, 0.5, 1, 0, 0, 0, 0, 0, 0.5, 0, 0.5, 1, 0, 1, 1, 1, 1, 0.5, 0, 0.5, 0, 1, 0.5, 0, 1, 0, 1, 1, 0.5, 1, 1, 0.5, 1, 0, 0, 0, 0, 0.5, 0, 0, 0, 1, 1, 1, 1, 0], [1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0.5, 0.5, 0.5, 0.5, 1, 1, 1, 0.5, 1, 0.5, 0.5, 0, 0.5, 0, 0, 1, 0, 1, 0, 1, 0.5, 0, 0.5, 0, 0, 1, 1, 1, 0.5, 0, 0.5, 0, 1, 1, 0.5, 1, 1, 0, 1, 0, 0.5, 1, 0.5, 1, 0, 0, 0, 0, 0.5, 1, 0, 0, 0, 0, 1, 1, 1], [0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0.5, 0.5, 0.5, 0.5, 1, 0, 1, 0.5, 1, 0.5, 0.5, 1, 0.5, 1, 0, 0, 0, 0, 1, 0, 0.5, 1, 0.5, 1, 1, 0, 1, 0, 0.5, 1, 0.5, 1, 1, 0, 0.5, 0, 0, 1, 0, 1, 0.5, 0, 0.5, 0, 0, 1, 0, 1, 0.5, 0, 1, 1, 1, 1, 0, 0, 0], [1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0.5, 0.5, 0.5, 0.5, 0, 1, 0, 0.5, 0, 0.5, 0.5, 0, 0.5, 0, 1, 1, 1, 1, 0, 0.5, 0, 0.5, 1, 1, 1, 1, 0, 1, 0.5, 0, 0.5, 0, 0, 0.5, 0, 0, 0, 0, 1, 0.5, 1, 1, 0.5, 1, 1, 0, 1, 0, 0.5, 1, 0, 1, 1, 0, 1, 0, 0], [0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0.5, 0.5, 0.5, 0.5, 0, 0, 0, 0.5, 0, 0.5, 0.5, 1, 0.5, 1, 1, 0, 1, 0, 1, 0.5, 1, 0.5, 0, 0, 0, 0, 0, 0, 0.5, 1, 0.5, 1, 0, 0.5, 1, 1, 1, 1, 0, 0.5, 0, 0, 0.5, 0, 1, 1, 1, 1, 0.5, 0, 1, 0, 0, 1, 0, 1, 1], [0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0.5, 0.5, 0.5, 0.5, 0, 1, 0, 0.5, 0, 0.5, 0.5, 0, 0.5, 0, 1, 1, 1, 0, 0, 0, 0.5, 1, 0.5, 1, 0, 0, 0, 0, 0.5, 1, 0.5, 1, 0, 0, 0.5, 0, 1, 1, 1, 1, 0.5, 0, 0.5, 0, 1, 1, 1, 1, 0.5, 0, 0, 1, 0, 1, 1, 0, 1], [1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0.5, 0.5, 0.5, 0.5, 0, 0, 0, 0.5, 0, 0.5, 0.5, 1, 0.5, 1, 1, 0, 1, 1, 1, 1, 0.5, 0, 0.5, 0, 1, 1, 0, 1, 0.5, 0, 0.5, 0, 0, 1, 0.5, 1, 0, 0, 0, 0, 0.5, 1, 0.5, 1, 1, 0, 1, 0, 0.5, 1, 1, 0, 1, 0, 0, 1, 0]];
        obj.data.uv_textures.new();
        obj.data.uv_layers[0].data.foreach_set("uv", maps[metadata])
