import bpy
import mathutils
from Block import Block

class Multitextured(Block):
    """A block with multiple textures"""

    def __init__(self, id, unlocalizedName, textureBottom="", textureTop="", textureFront="", textureLeft="", textureBack="", textureRight=""):
        """Multitextured constructor
        
        Some arguments may be left blank and will be determined according to the following rules:
            - If only one of textureTop and textureBottom is specified, they will both use that specified value
            - If only one of textureFront and textureBack is specified, they will both use that specified value 
            - If only one of textureLeft and textureRight is specified, they will both use that specified value
            - If only one of textureFront, textureLeft, textureBack, and textureRight is specified, they will all use that specified value
        The following situations are invalid. They may cause unexpected behaviours or errors:
            - no textures are specified
            - textureLeft and textureRight are specified but textureFront and textureBack are not specified
            - textureFront and textureBack are specified but textureLeft and textureRight are not specified
            - textureBottom and textureTop are not specified
        """
        self._id = id
        self._unlocalizedName = unlocalizedName
        self._textureNames = [None]*6
        
        # Bottom Texture
        if textureBottom == "":
            self._textureNames[0] = textureTop
        else:
            self._textureNames[0] = textureBottom
        
        # Top Texture
        if textureTop == "":
            self._textureNames[1] = textureBottom
        else:
            self._textureNames[1] = textureTop
        
        # Front Texture
        if textureFront == "":
            if textureBack == "":
                if textureLeft == "":
                    self._textureNames[2] = textureRight
                else:
                    self._textureNames[2] = textureLeft
            else:
                self._textureNames[2] = textureBack
        else:
            self._textureNames[2] = textureFront
        
        # Left Texture
        if textureLeft == "":
            if textureRight == "":
                self._textureNames[3] = self._textureNames[2]
            else:
                self._textureNames[3] = textureRight
        else:
            self._textureNames[3] = textureLeft
        
        # Back Texture
        if textureBack == "":
            self._textureNames[4] = self._textureNames[2]
        else:
            self._textureNames[4] = textureBack
        
        #Right Texture
        if textureRight == "":
            self._textureNames[5] = self._textureNames[3]
        else:
            self._textureNames[5] = textureRight
    
    def applyMaterial(self, obj, metadata):
        sideMapping = ["Bottom", "Top", "Front", "Left", "Back", "Right"]
        for index, sideName in enumerate(sideMapping):
            try:
                mat = bpy.data.materials[self._unlocalizedName + " " + sideName]
            #end try
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
                    mat.node_tree.links.new(mat.node_tree.nodes["Texture Coordinate"].outputs[0], mat.node_tree.nodes["Image Texture"].inputs[0])
                    mat.node_tree.nodes["Texture Coordinate"].location = [-200, 0]

            obj.data.materials.append(mat)
        #end sideMapping loop
        
        for i in range(0,6):
            obj.data.polygons[i].material_index = i
