import bpy
import mathutils
from Transparent import Transparent

class Fire(Transparent):
    """Fire block"""
    
    def makeObject(self, x, y, z, metadata):
        mesh = bpy.data.meshes.new(name="Block")
        mesh.from_pydata([[-0.5,-0.5,-0.7],[0.5,-0.5,-0.7],[-0.5,0.5,-0.7],[0.5,0.5,-0.7],[-0.5,-0.5,0.7],[0.5,-0.5,0.7],[-0.5,0.5,0.7],[0.5,0.5,0.7],[-0.2,-0.5,-0.7],[-0.2,0.5,-0.7],[0.3,0.5,0.7],[0.3,-0.5,0.7],[0.2,-0.5,-0.7],[0.2,0.5,-0.7],[-0.3,0.5,0.7],[-0.3,-0.5,0.7],[-0.5,-0.2,-0.7],[0.5,-0.2,-0.7],[0.5,0.3,0.7],[-0.5,0.3,0.7],[-0.5,0.2,-0.7],[0.5,0.2,-0.7],[0.5,-0.3,0.7],[-0.5,-0.3,0.7]],[],[[0,1,5,4],[0,2,6,4],[2,3,7,6],[1,3,7,5],[8,9,10,11],[12,13,14,15],[16,17,18,19],[20,21,22,23]])
        mesh.update()

        obj = bpy.data.objects.new("Block", mesh)
        obj.location.x = x + 0.5
        obj.location.y = y + 0.5
        obj.location.z = z + 0.7
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
            
            #First Image Texture
            mat.node_tree.nodes.new(type="ShaderNodeTexImage")
            mat.node_tree.nodes["Image Texture"].location = [-200, 75]
            mat.node_tree.nodes["Image Texture"].image = tex
            mat.node_tree.nodes["Image Texture"].interpolation = "Closest"
            mat.node_tree.nodes["Image Texture"].projection = "FLAT"
            mat.node_tree.links.new(mat.node_tree.nodes["Image Texture"].outputs[0], mat.node_tree.nodes["Diffuse BSDF"].inputs[0])
            mat.node_tree.links.new(mat.node_tree.nodes["Image Texture"].outputs[1], mat.node_tree.nodes["Mix Shader"].inputs[0])
            
            #Mapping
            mat.node_tree.nodes.new(type="ShaderNodeMapping")
            mat.node_tree.nodes["Mapping"].location = [-550, 0]
            animationFrames = [16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
            totalFrames = 32
            for animationFrameIndex, textureFrameIndex in enumerate(animationFrames):
                mat.node_tree.nodes["Mapping"].translation.y = 1 - textureFrameIndex / totalFrames
                mat.node_tree.nodes["Mapping"].keyframe_insert("translation", frame=animationFrameIndex+1)
            mat.node_tree.animation_data.action.fcurves[1].modifiers.new(type="CYCLES")
            mat.node_tree.links.new(mat.node_tree.nodes["Mapping"].outputs[0], mat.node_tree.nodes["Image Texture"].inputs[0])
            
            #UV Map
            mat.node_tree.nodes.new(type="ShaderNodeUVMap")
            mat.node_tree.nodes["UV Map"].location = [-750, 0]
            mat.node_tree.nodes["UV Map"].uv_map = "UVMap"
            mat.node_tree.links.new(mat.node_tree.nodes["UV Map"].outputs[0], mat.node_tree.nodes["Mapping"].inputs[0])
        
        obj.data.materials.append(mat)

    def makeUVMap(self, obj, metadata):
        obj.data.uv_textures.new();
        obj.data.uv_layers[0].data.foreach_set("uv", [0, 0, 1, 0, 1, 0.03125, 0, 0.03125, 1, 0, 1, 0.03125, 0, 0.03125, 0, 0, 1, 0, 1, 0.03125, 0, 0.03125, 0, 0, 0, 0, 1, 0, 1, 0.03125, 0, 0.03125, 0, 0, 1, 0, 1, 0.03125, 0, 0.03125, 0, 0, 1, 0, 1, 0.03125, 0, 0.03125, 0, 0, 1, 0, 1, 0.03125, 0, 0.03125, 0, 0, 1, 0, 1, 0.03125, 0, 0.03125])