import bpy
import mathutils
from Multitextured import Multitextured

class Grass(Multitextured):
    """A grass block"""
    
    def __init__(self, id, unlocalizedName, textureBottom, textureTop, textureSide, textureSideOverlay):
        self._overlayTexture = textureSideOverlay
        Multitextured.__init__(self, id, unlocalizedName, textureBottom, textureTop, textureSide)
    
    def applyMaterial(self, obj, metadata):
        try:
            mat = bpy.data.materials[self._unlocalizedName + " Bottom"]
        except KeyError:
            mat = bpy.data.materials.new(self._unlocalizedName + " Bottom")
            mat.preview_render_type = "CUBE"
            mat.use_nodes = True
            mat.node_tree.nodes["Material Output"].location = [300, 0]
            mat.node_tree.nodes["Diffuse BSDF"].location = [100, 0]
        
            #Initialize Texture
            try:
                tex = bpy.data.images[self._unlocalizedName + " Bottom"]
            except KeyError:
                tex = bpy.data.images.load(self.getBlockTexturePath(self._textureNames[0]))
                tex.name = self._unlocalizedName + " Bottom"
            
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
         
        try:
            mat = bpy.data.materials[self._unlocalizedName + " Top"]
        except KeyError:
            mat = bpy.data.materials.new(self._unlocalizedName + " Top")
            mat.preview_render_type = "CUBE"
            mat.use_nodes = True
            mat.node_tree.nodes["Material Output"].location = [300, 0]
            mat.node_tree.nodes["Diffuse BSDF"].location = [100, 0]
        
            #Initialize Texture
            try:
                tex = bpy.data.images[self._unlocalizedName + " Top"]
            except KeyError:
                tex = bpy.data.images.load(self.getBlockTexturePath(self._textureNames[1]))
                tex.name = self._unlocalizedName + " Top"
            
            # Mix RGB (Multiply)
            mat.node_tree.nodes.new(type="ShaderNodeMixRGB")
            mat.node_tree.nodes["Mix"].location = [-100, 25]
            mat.node_tree.nodes["Mix"].blend_type = "MULTIPLY"
            mat.node_tree.nodes["Mix"].inputs[0].default_value = 1
            mat.node_tree.nodes["Mix"].inputs[2].default_value = (0, 1, 0, 1)
            mat.node_tree.links.new(mat.node_tree.nodes["Mix"].outputs[0], mat.node_tree.nodes["Diffuse BSDF"].inputs[0])
            
            #First Image Texture
            mat.node_tree.nodes.new(type="ShaderNodeTexImage")
            mat.node_tree.nodes["Image Texture"].location = [-300, 75]
            mat.node_tree.nodes["Image Texture"].image = tex
            mat.node_tree.nodes["Image Texture"].interpolation = "Closest"
            mat.node_tree.nodes["Image Texture"].projection = "FLAT"
            mat.node_tree.links.new(mat.node_tree.nodes["Image Texture"].outputs[0], mat.node_tree.nodes["Mix"].inputs[1])
            
            #UV Map
            mat.node_tree.nodes.new(type="ShaderNodeUVMap")
            mat.node_tree.nodes["UV Map"].location = [-300, 0]
            mat.node_tree.nodes["UV Map"].uv_map = "UVMap"
            mat.node_tree.links.new(mat.node_tree.nodes["UV Map"].outputs[0], mat.node_tree.nodes["Image Texture"].inputs[0])
            
        obj.data.materials.append(mat)
            
        try:
            mat = bpy.data.materials[self._unlocalizedName + " Side"]
        except KeyError:
            mat = bpy.data.materials.new(self._unlocalizedName + " Side")
            mat.preview_render_type = "CUBE"
            mat.use_nodes = True
            mat.node_tree.nodes["Material Output"].location = [500, 0]
            mat.node_tree.nodes["Diffuse BSDF"].location = [100, -200]
            
            #UV Map
            mat.node_tree.nodes.new(type="ShaderNodeUVMap")
            mat.node_tree.nodes["UV Map"].location = [-500, 0]
            mat.node_tree.nodes["UV Map"].uv_map = "UVMap"
            
            #Initialize Side Texture
            try:
                tex = bpy.data.images[self._unlocalizedName + " Side Overlay"]
            except KeyError:
                tex = bpy.data.images.load(self.getBlockTexturePath(self._textureNames[self._overlayTexture]))
                tex.name = self._unlocalizedName + " Side Overlay"
            
            #First Image Texture
            mat.node_tree.nodes.new(type="ShaderNodeTexImage")
            mat.node_tree.nodes["Image Texture"].location = [-300, -125]
            mat.node_tree.nodes["Image Texture"].image = tex
            mat.node_tree.nodes["Image Texture"].interpolation = "Closest"
            mat.node_tree.nodes["Image Texture"].projection = "FLAT"
            mat.node_tree.links.new(mat.node_tree.nodes["UV Map"].outputs[0], mat.node_tree.nodes["Image Texture"].inputs[0])
            
            #Initialize Side Texture
            try:
                tex = bpy.data.images[self._unlocalizedName + " Side"]
            except KeyError:
                tex = bpy.data.images.load(self.getBlockTexturePath(self._textureNames[2]))
                tex.name = self._unlocalizedName + " Side"
            
            #Second Image Texture
            mat.node_tree.nodes.new(type="ShaderNodeTexImage")
            mat.node_tree.nodes["Image Texture.001"].location = [-300, 225]
            mat.node_tree.nodes["Image Texture.001"].image = tex
            mat.node_tree.nodes["Image Texture.001"].interpolation = "Closest"
            mat.node_tree.nodes["Image Texture.001"].projection = "FLAT"
            mat.node_tree.links.new(mat.node_tree.nodes["UV Map"].outputs[0], mat.node_tree.nodes["Image Texture.001"].inputs[0])
            
            # Mix RGB (Multiply)
            mat.node_tree.nodes.new(type="ShaderNodeMixRGB")
            mat.node_tree.nodes["Mix"].location = [-100, -175]
            mat.node_tree.nodes["Mix"].blend_type = "MULTIPLY"
            mat.node_tree.nodes["Mix"].inputs[0].default_value = 1
            mat.node_tree.nodes["Mix"].inputs[2].default_value = (0, 1, 0, 1)
            mat.node_tree.links.new(mat.node_tree.nodes["Image Texture"].outputs[0], mat.node_tree.nodes["Mix"].inputs[1])
            mat.node_tree.links.new(mat.node_tree.nodes["Mix"].outputs[0], mat.node_tree.nodes["Diffuse BSDF"].inputs[0])
            
            #Second Diffuse BSDF
            mat.node_tree.nodes.new(type="ShaderNodeBsdfDiffuse")
            mat.node_tree.nodes["Diffuse BSDF.001"].location = [100, 200]
            mat.node_tree.links.new(mat.node_tree.nodes["Image Texture.001"].outputs[0], mat.node_tree.nodes["Diffuse BSDF.001"].inputs[0])
            
            #Mix Shader
            mat.node_tree.nodes.new(type="ShaderNodeMixShader")
            mat.node_tree.nodes["Mix Shader"].location = [300, 0]
            mat.node_tree.links.new(mat.node_tree.nodes["Image Texture"].outputs[1], mat.node_tree.nodes["Mix Shader"].inputs[0])
            mat.node_tree.links.new(mat.node_tree.nodes["Diffuse BSDF.001"].outputs[0], mat.node_tree.nodes["Mix Shader"].inputs[1])
            mat.node_tree.links.new(mat.node_tree.nodes["Diffuse BSDF"].outputs[0], mat.node_tree.nodes["Mix Shader"].inputs[2])
            mat.node_tree.links.new(mat.node_tree.nodes["Mix Shader"].outputs[0], mat.node_tree.nodes["Material Output"].inputs[0])
        
        obj.data.materials.append(mat)
        
        
        for i in range(0,6):
            obj.data.polygons[i].material_index = min(2, i)