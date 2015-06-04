import bpy
import mathutils
from Block import Block

class Slab(Block):
    """Slab block with a single texture"""
    
    def make(self, x, y, z, metadata):
        tempUnlocalizedName = self._unlocalizedName
        if metadata & 8:
            self._unlocalizedName += " High"
        else:
            self._unlocalizedName += " Low"
        
        obj = self.makeObject(x, y, z, metadata)
        self.applyMaterial(obj, metadata)
        
        self._unlocalizedName = tempUnlocalizedName
    
    def makeObject(self, x, y, z, metadata):
        """
        py:function:: makeObject(self)
        
        Make a new block and returns its object.
        
        Return type: <class 'bpy_types.Object'>
        """
        mesh = bpy.data.meshes.new(name="Block")
        mesh.from_pydata([[-0.5,-0.5,-0.25],[0.5,-0.5,-0.25],[-0.5,0.5,-0.25],[0.5,0.5,-0.25],[-0.5,-0.5,0.25],[0.5,-0.5,0.25],[-0.5,0.5,0.25],[0.5,0.5,0.25]],[],[[0,1,3,2],[4,5,7,6],[0,1,5,4],[0,2,6,4],[2,3,7,6],[1,3,7,5]])
        mesh.update()
        
        obj = bpy.data.objects.new("Block", mesh)
        obj.location.x = x + 0.5
        obj.location.y = y + 0.5
        obj.location.z = z + 0.25 + 0.5 * (metadata >> 3 & 1)
        bpy.context.scene.objects.link(obj)
        
        bpy.context.scene.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.object.editmode_toggle()
        
        return obj
    
    def applyMaterial(self, obj, metadata):
        try:
            mat = bpy.data.materials[self._unlocalizedName]
        except KeyError:
            mat = bpy.data.materials.new(self._unlocalizedName)
            mat.use_nodes = True
            mat.node_tree.links.remove(mat.node_tree.links[0])
            mat.node_tree.nodes["Material Output"].location = [600, 0]
            
            #Mix Shader
            mat.node_tree.nodes.new(type="ShaderNodeMixShader")
            mat.node_tree.nodes["Mix Shader"].location = [400,0]
            mat.node_tree.links.new(mat.node_tree.nodes["Mix Shader"].outputs[0], mat.node_tree.nodes["Material Output"].inputs[0])
            
            #Multiply
            mat.node_tree.nodes.new(type="ShaderNodeMath")
            mat.node_tree.nodes["Math"].location = [200,200]
            mat.node_tree.nodes["Math"].operation = "MULTIPLY"
            mat.node_tree.nodes["Math"].use_clamp = True
            mat.node_tree.links.new(mat.node_tree.nodes["Math"].outputs[0], mat.node_tree.nodes["Mix Shader"].inputs[0])
            
            #First Diffuse Shader (already exists from default use_node setup)
            mat.node_tree.nodes["Diffuse BSDF"].location = [200, 0]
            mat.node_tree.links.new(mat.node_tree.nodes["Diffuse BSDF"].outputs[0], mat.node_tree.nodes["Mix Shader"].inputs[1])
            
            #Second Diffuse Shader
            mat.node_tree.nodes.new(type="ShaderNodeBsdfDiffuse")
            mat.node_tree.nodes["Diffuse BSDF.001"].location = [200,-150]
            mat.node_tree.links.new(mat.node_tree.nodes["Diffuse BSDF.001"].outputs[0], mat.node_tree.nodes["Mix Shader"].inputs[2])
            
            #Initialize Texture
            try:
                tex = bpy.data.images[self._unlocalizedName]
            except KeyError:
                tex = bpy.data.images.load(self.getBlockTexturePath(self._textureName))
                tex.name = self._unlocalizedName
            
            #First Image Texture
            mat.node_tree.nodes.new(type="ShaderNodeTexImage")
            mat.node_tree.nodes["Image Texture"].location = [0, 50]
            mat.node_tree.nodes["Image Texture"].image = tex
            mat.node_tree.nodes["Image Texture"].interpolation = "Closest"
            mat.node_tree.nodes["Image Texture"].projection = "BOX"
            mat.node_tree.links.new(mat.node_tree.nodes["Image Texture"].outputs[0], mat.node_tree.nodes["Diffuse BSDF"].inputs[0])
            
            #Second Image Texture
            mat.node_tree.nodes.new(type="ShaderNodeTexImage")
            mat.node_tree.nodes["Image Texture.001"].location = [0, -250]
            mat.node_tree.nodes["Image Texture.001"].image = tex
            mat.node_tree.nodes["Image Texture.001"].interpolation = "Closest"
            mat.node_tree.nodes["Image Texture.001"].projection = "BOX"
            mat.node_tree.links.new(mat.node_tree.nodes["Image Texture.001"].outputs[0], mat.node_tree.nodes["Diffuse BSDF.001"].inputs[0])
            
            #Separate XYZ
            mat.node_tree.nodes.new(type="ShaderNodeSeparateXYZ")
            mat.node_tree.nodes["Separate XYZ"].location = [-300,200]
            mat.node_tree.links.new(mat.node_tree.nodes["Separate XYZ"].outputs[2], mat.node_tree.nodes["Math"].inputs[0])
            mat.node_tree.links.new(mat.node_tree.nodes["Separate XYZ"].outputs[2], mat.node_tree.nodes["Math"].inputs[1])
            
            #First Mapping
            mat.node_tree.nodes.new(type="ShaderNodeMapping")
            mat.node_tree.nodes["Mapping"].location = [-400, 0]
            mat.node_tree.nodes["Mapping"].scale[1] = -1.0
            mat.node_tree.nodes["Mapping"].scale[2] = 0.5
            mat.node_tree.nodes["Mapping"].translation.z = 0.5 * (metadata >> 3 & 1)
            mat.node_tree.links.new(mat.node_tree.nodes["Mapping"].outputs[0], mat.node_tree.nodes["Image Texture"].inputs[0])
            
            #Second Mapping
            mat.node_tree.nodes.new(type="ShaderNodeMapping")
            mat.node_tree.nodes["Mapping.001"].location = [-400,-300]
            mat.node_tree.nodes["Mapping.001"].rotation = mathutils.Euler((0.0, 0.0, -1.5707963705062866), 'XYZ')
            mat.node_tree.nodes["Mapping.001"].scale[0] = -1.0
            mat.node_tree.links.new(mat.node_tree.nodes["Mapping.001"].outputs[0], mat.node_tree.nodes["Image Texture.001"].inputs[0])
            
            #Texture Coordinate
            mat.node_tree.nodes.new(type="ShaderNodeTexCoord")
            mat.node_tree.nodes["Texture Coordinate"].location = [-600,0]
            mat.node_tree.links.new(mat.node_tree.nodes["Texture Coordinate"].outputs[0], mat.node_tree.nodes["Mapping"].inputs[0])
            mat.node_tree.links.new(mat.node_tree.nodes["Texture Coordinate"].outputs[0], mat.node_tree.nodes["Mapping.001"].inputs[0])
            mat.node_tree.links.new(mat.node_tree.nodes["Texture Coordinate"].outputs[1], mat.node_tree.nodes["Separate XYZ"].inputs[0])
        
        obj.data.materials.append(mat)