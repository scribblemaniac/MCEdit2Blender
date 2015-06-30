import bpy
import mathutils
from Multitextured import Multitextured
from Stairs import Stairs

class MultitexturedStairs(Multitextured, Stairs):
    """Stair block with a single texture"""

    def __init__(self, id, unlocalizedName, textureBottom="", textureTop="", textureFront="", textureLeft="", textureBack="", textureRight=""):
        """MultitexturedStairs constructor
        
        See blocks.Multitextured.Multitextured.__init__ for more details on the shorthand notation for this constructor
        """
        Multitextured.__init__(self, id, unlocalizedName, textureBottom, textureTop, textureFront, textureLeft, textureBack, textureRight)
    
    def make(self, x, y, z, metadata):
        obj = Stairs.makeObject(self, x, y, z, metadata)
        Stairs.makeUVMap(self, obj, metadata)
        self.applyMaterial(obj, metadata)
    
    def applyMaterial(self, obj, metadata):
        sideMapping = ["Bottom", "Top", "Front", "Left", "Back", "Right"]
        for index, sideName in enumerate(sideMapping):
            try:
                mat = bpy.data.materials[self._unlocalizedName + " " + sideName]
            except KeyError:
                mat = bpy.data.materials.new(self._unlocalizedName + " " + sideName)
                mat.preview_render_type = "CUBE"
                mat.use_nodes = True
                mat.node_tree.nodes["Material Output"].location = [300, 0]
                mat.node_tree.nodes["Diffuse BSDF"].location = [100, 0]
            
                #Initialize Texture
                try:
                    tex = bpy.data.images[self._unlocalizedName + " " + sideName]
                except KeyError:
                    tex = bpy.data.images.load(self.getBlockTexturePath(self._textureNames[index]))
                    tex.name = self._unlocalizedName + " " + sideName

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
        
        for i in range(0,8):
            obj.data.polygons[i].material_index = 2
        
        obj.data.polygons[3].material_index = obj.data.polygons[5].material_index = not metadata >> 2
        obj.data.polygons[7].material_index = metadata >> 2