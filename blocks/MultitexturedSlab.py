import bpy
import mathutils
from Multitextured import Multitextured
from Slab import Slab

class MultitexturedSlab(Multitextured, Slab):
    """Slab block with a multiple textures"""
    
    def __init__(self, id, unlocalizedName, textureBottom="", textureTop="", textureFront="", textureLeft="", textureBack="", textureRight=""):
        """MultitexturedSlab constructor
        
        See blocks.Multitextured.Multitextured.__init__ for more details on the shorthand notation for this constructor
        """
        Multitextured.__init__(self, id, unlocalizedName, textureBottom, textureTop, textureFront, textureLeft, textureBack, textureRight)

    def make(self, x, y, z, metadata):
        tempUnlocalizedName = self._unlocalizedName
        if metadata & 8:
            self._unlocalizedName += " High"
        else:
            self._unlocalizedName += " Low"
        
        obj = Slab.makeObject(self, x, y, z, metadata)
        self.applyMaterial(obj, metadata)
        
        self._unlocalizedName = tempUnlocalizedName
    
    def applyMaterial(self, obj, metadata):
        sideMapping = ["Bottom", "Top", "Front", "Left", "Back", "Right"]
        for index, sideName in enumerate(sideMapping):
            try:
                mat = bpy.data.materials[self._unlocalizedName + " " + sideName]
            except KeyError:
                mat = bpy.data.materials.new(self._unlocalizedName + " " + sideName)
                mat.use_nodes = True
                mat.node_tree.nodes["Material Output"].location = [400, 0]
                mat.node_tree.nodes["Diffuse BSDF"].location = [200, 0]

                try:
                    tex = bpy.data.images[self._unlocalizedName + " " + sideName]
                except KeyError:
                    tex = bpy.data.images.load(self.getBlockTexturePath(self._textureNames[index]))
                    tex.name = self._unlocalizedName + " " + sideName
                mat.node_tree.nodes.new(type="ShaderNodeTexImage")
                mat.node_tree.nodes["Image Texture"].location = [0, 0]
                mat.node_tree.nodes["Image Texture"].image = tex
                mat.node_tree.nodes["Image Texture"].interpolation = "Closest"
                mat.node_tree.nodes["Image Texture"].projection = "BOX"
                mat.node_tree.links.new(mat.node_tree.nodes["Image Texture"].outputs[0], mat.node_tree.nodes["Diffuse BSDF"].inputs[0])

                mat.node_tree.nodes.new(type="ShaderNodeTexCoord")

                if index < 2:
                    mat.node_tree.nodes.new(type="ShaderNodeMapping")
                    mat.node_tree.nodes["Mapping"].location = [-400, 0]
                    mat.node_tree.nodes["Mapping"].rotation = mathutils.Euler((0.0, 0.0, 1.5707963705062866), 'XYZ')
                    mat.node_tree.nodes["Mapping"].scale[0] = -1.0
                    mat.node_tree.links.new(mat.node_tree.nodes["Mapping"].outputs[0], mat.node_tree.nodes["Image Texture"].inputs[0])
                    mat.node_tree.nodes["Texture Coordinate"].location = [-600, 0]
                    mat.node_tree.links.new(mat.node_tree.nodes["Texture Coordinate"].outputs[0], mat.node_tree.nodes["Mapping"].inputs[0])
                else:
                    mat.node_tree.nodes.new(type="ShaderNodeMapping")
                    mat.node_tree.nodes["Mapping"].location = [-400, 0]
                    mat.node_tree.nodes["Mapping"].scale[2] = 0.5
                    mat.node_tree.nodes["Mapping"].translation.z = 0.5 * (metadata >> 3 & 1)
                    mat.node_tree.links.new(mat.node_tree.nodes["Mapping"].outputs[0], mat.node_tree.nodes["Image Texture"].inputs[0])
                    mat.node_tree.nodes["Texture Coordinate"].location = [-600, 0]
                    mat.node_tree.links.new(mat.node_tree.nodes["Texture Coordinate"].outputs[0], mat.node_tree.nodes["Mapping"].inputs[0])

            obj.data.materials.append(mat)

        for i in range(0,6):
            obj.data.polygons[i].material_index = i