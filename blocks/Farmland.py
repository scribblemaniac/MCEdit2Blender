import bpy
import mathutils
from Multitextured import Multitextured

class Farmland(Multitextured):
    """Wet and dry farmland blocks"""
    
    def makeObject(self, x, y, z, metadata):
        mesh = bpy.data.meshes.new(name="Block")
        mesh.from_pydata([[-0.5,-0.5,-0.5],[0.5,-0.5,-0.5],[-0.5,0.5,-0.5],[0.5,0.5,-0.5],[-0.5,-0.5,0.4375],[0.5,-0.5,0.4375],[-0.5,0.5,0.4375],[0.5,0.5,0.4375]],[],[[0,1,3,2],[4,5,7,6],[0,1,5,4],[0,2,6,4],[2,3,7,6],[1,3,7,5]])
        mesh.update()

        obj = bpy.data.objects.new("Block", mesh)
        obj.location.x = x + 0.5
        obj.location.y = y + 0.5
        obj.location.z = z + 0.5
        obj.blockId = self._id
        obj.blockMetadata = metadata
        bpy.context.scene.objects.link(obj)

        activeObject = bpy.context.scene.objects.active
        bpy.context.scene.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.object.editmode_toggle()
        bpy.context.scene.objects.active = activeObject
        
        return obj
    
    def makeUVMap(self, obj, metadata):
        obj.data.uv_textures.new();
        obj.data.uv_layers[0].data.foreach_set("uv", [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0.9375, 0, 0.9375, 1, 0, 1, 0.9375, 0, 0.9375, 0, 0, 0, 0, 0, 0.9375, 1, 0.9375, 1, 0, 1, 0, 0, 0, 0, 0.9375, 1, 0.9375])
