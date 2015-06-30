import bpy
import mathutils
from Block import Block

class Log(Block):
    """A log block"""

    def __init__(self, id, unlocalizedName, topTexture, sideTexture):
        self._id = id
        self._unlocalizedName = unlocalizedName
        self._topTexture = topTexture
        self._sideTexture = self._textureName = sideTexture
    
    def make(self, x, y, z, metadata):
        if metadata & 0xC == 0xC:
            self._unlocalizedName += " Side"
            obj = Block.makeObject(self, x, y, z, metadata)
            Block.makeUVMap(self, obj, metadata)
            Block.applyMaterial(self, obj, metadata)
        else:
            obj = Block.makeObject(self, x, y, z, metadata)
            self.makeUVMap(obj, metadata)
            self.applyMaterial(obj, metadata)
    
    def makeUVMap(self, obj, metadata):
        obj.data.uv_textures.new();
        if metadata & 0x4:
            obj.data.uv_layers[0].data.foreach_set("uv", [0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1])
        elif metadata & 0x8:
            obj.data.uv_layers[0].data.foreach_set("uv", [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0])
        else:
            obj.data.uv_layers[0].data.foreach_set("uv", [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1])
    
    def applyMaterial(self, obj, metadata):
        nameMap = [("Side", self._sideTexture), ("Top", self._topTexture)]
        for name, textureName in nameMap:
            try:
                mat = bpy.data.materials[self._unlocalizedName + " " + name]
            except KeyError:
                mat = bpy.data.materials.new(self._unlocalizedName + " " + name)
                mat.preview_render_type = "CUBE"
                mat.use_nodes = True
                mat.node_tree.nodes["Material Output"].location = [300, 0]
                mat.node_tree.nodes["Diffuse BSDF"].location = [100, 0]
                
                #Initialize Texture
                try:
                    tex = bpy.data.images[self._unlocalizedName + " " + name]
                except KeyError:
                    tex = bpy.data.images.load(self.getBlockTexturePath(textureName))
                    tex.name = self._unlocalizedName + " " + name
    
                #First Image Texture
                mat.node_tree.nodes.new(type="ShaderNodeTexImage")
                mat.node_tree.nodes["Image Texture"].location = [-100, 75]
                mat.node_tree.nodes["Image Texture"].image = tex
                mat.node_tree.nodes["Image Texture"].interpolation = "Closest"
                mat.node_tree.nodes["Image Texture"].projection = "FLAT"
                mat.node_tree.links.new(mat.node_tree.nodes["Image Texture"].outputs[0], mat.node_tree.nodes["Diffuse BSDF"].inputs[0])
                
                #UV Map
                mat.node_tree.nodes.new(type="ShaderNodeUVMap")
                mat.node_tree.nodes["UV Map"].location = [-300, 0]
                mat.node_tree.nodes["UV Map"].uv_map = "UVMap"
                mat.node_tree.links.new(mat.node_tree.nodes["UV Map"].outputs[0], mat.node_tree.nodes["Image Texture"].inputs[0])
            
            obj.data.materials.append(mat)
        
        if metadata & 0xC != 0xC: # This function should not even be called if the metadata contains 0xC
            if metadata & 0x4:
                obj.data.polygons[3].material_index = obj.data.polygons[5].material_index = 1
            elif metadata & 0x8:
                obj.data.polygons[2].material_index = obj.data.polygons[4].material_index = 1
            else:
                obj.data.polygons[0].material_index = obj.data.polygons[1].material_index = 1