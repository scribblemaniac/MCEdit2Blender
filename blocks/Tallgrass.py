import bpy
import mathutils
from Plant import Plant

class Tallgrass(Plant):
    """Tallgrass blocks"""
    
    def applyMaterial(self, obj, metadata):
        try:
            mat = bpy.data.materials[self._unlocalizedName]
        except KeyError:
            mat = bpy.data.materials.new(self._unlocalizedName)
            mat.preview_render_type = "CUBE"
            mat.use_nodes = True
            mat.node_tree.nodes["Material Output"].location = [400, 0]
            mat.node_tree.nodes["Diffuse BSDF"].location = [0, -75]
            mat.node_tree.links.remove(mat.node_tree.links[0])
            
            #Mix Shader
            mat.node_tree.nodes.new(type="ShaderNodeMixShader")
            mat.node_tree.nodes["Mix Shader"].location = [200, 0]
            mat.node_tree.links.new(mat.node_tree.nodes["Diffuse BSDF"].outputs[0], mat.node_tree.nodes["Mix Shader"].inputs[2])
            mat.node_tree.links.new(mat.node_tree.nodes["Mix Shader"].outputs[0], mat.node_tree.nodes["Material Output"].inputs[0])
            
            #Transparent Shader
            mat.node_tree.nodes.new(type="ShaderNodeBsdfTransparent")
            mat.node_tree.nodes["Transparent BSDF"].location = [0, 100]
            mat.node_tree.links.new(mat.node_tree.nodes["Transparent BSDF"].outputs[0], mat.node_tree.nodes["Mix Shader"].inputs[1])
            
            #Initialize Texture
            try:
                tex = bpy.data.images[self._unlocalizedName]
            except KeyError:
                tex = bpy.data.images.load(self.getBlockTexturePath(self._textureName))
                tex.name = self._unlocalizedName
            
            #Mix RGB (Multiply)
            mat.node_tree.nodes.new(type="ShaderNodeMixRGB")
            mat.node_tree.nodes["Mix"].location = [-100, -200]
            mat.node_tree.nodes["Mix"].blend_type = "MULTIPLY"
            mat.node_tree.nodes["Mix"].inputs[0].default_value = 1
            mat.node_tree.nodes["Mix"].inputs[2].default_value = (0, 1, 0, 1)
            mat.node_tree.links.new(mat.node_tree.nodes["Mix"].outputs[0], mat.node_tree.nodes["Diffuse BSDF"].inputs[0])
            
            #First Image Texture
            mat.node_tree.nodes.new(type="ShaderNodeTexImage")
            mat.node_tree.nodes["Image Texture"].location = [-400, 75]
            mat.node_tree.nodes["Image Texture"].image = tex
            mat.node_tree.nodes["Image Texture"].interpolation = "Closest"
            mat.node_tree.nodes["Image Texture"].projection = "FLAT"
            mat.node_tree.links.new(mat.node_tree.nodes["Image Texture"].outputs[0], mat.node_tree.nodes["Mix"].inputs[1])
            mat.node_tree.links.new(mat.node_tree.nodes["Image Texture"].outputs[1], mat.node_tree.nodes["Mix Shader"].inputs[0])
            
            #UV Map
            mat.node_tree.nodes.new(type="ShaderNodeUVMap")
            mat.node_tree.nodes["UV Map"].location = [-600, 0]
            mat.node_tree.nodes["UV Map"].uv_map = "UVMap"
            mat.node_tree.links.new(mat.node_tree.nodes["UV Map"].outputs[0], mat.node_tree.nodes["Image Texture"].inputs[0])
        
        obj.data.materials.append(mat)