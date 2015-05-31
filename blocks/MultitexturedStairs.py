import bpy
from Multitextured import Multitextured
from Stairs import Stairs

class Stairs(Multitextured, Stairs):
    """Stair block with a single texture"""

    def __init__(self, id, metadata, unlocalizedName, textureBottom="", textureTop="", textureFront="", textureLeft="", textureBack="", textureRight=""):
        """MultitexturedStairs constructor
        
        See blocks.Multitextured.Multitextured.__init__ for more details on the shorthand notation for this constructor
        """
        Multitextured.__init__(self, id, metadata, unlocalizedName, textureBottom, textureTop, textureFront, textureLeft, textureBack, textureRight)
    
    def make(self):
        obj = Stairs.makeObject(self)
        self.applyMaterial(obj)
    
    def applyMaterial(self, obj):
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
                    tex = bpy.data.images[self._unlocalizedname + " " + sideName]
                except KeyError:
                    tex = bpy.data.images.load(Blocks.getBlockTexturePath(self._textures[index]))
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
                    mat.node_tree.nodes["Mapping"].rotation = mathutils.Euler((0.0, 0.0, -1.5707963705062866), 'XYZ')
                    mat.node_tree.nodes["Mapping"].scale[0] = -1.0
                    mat.node_tree.links.new(mat.node_tree.nodes["Mapping"].outputs[0], mat.node_tree.nodes["Image Texture"].inputs[0])
                    mat.node_tree.nodes["Texture Coordinate"].location = [-600, 0]
                    mat.node_tree.links.new(mat.node_tree.nodes["Texture Coordinate"].outputs[0], mat.node_tree.nodes["Mapping"].inputs[0])
                elif index == 3 or index == 5:
                    mat.node_tree.nodes.new(type="ShaderNodeMapping")
                    mat.node_tree.nodes["Mapping"].location = [-400, 0]
                    mat.node_tree.nodes["Mapping"].scale[1] = -1.0
                    mat.node_tree.links.new(mat.node_tree.nodes["Mapping"].outputs[0], mat.node_tree.nodes["Image Texture"].inputs[0])
                    mat.node_tree.nodes["Texture Coordinate"].location = [-600, 0]
                    mat.node_tree.links.new(mat.node_tree.nodes["Texture Coordinate"].outputs[0], mat.node_tree.nodes["Mapping"].inputs[0])
                else:
                    mat.node_tree.links.new(mat.node_tree.nodes["Texture Coordinate"].outputs[0], mat.node_tree.nodes["Image Texture"].inputs[0])
                    mat.node_tree.nodes["Texture Coordinate"].location = [-200, 0]
