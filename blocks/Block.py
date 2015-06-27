import bpy
import mathutils

class Block:
    """A basic block with a single texture
    
    This class should be inherited by every other block class
    """

    def __init__(self, id, unlocalizedName, textureName):
        self._id = id
        self._unlocalizedName = unlocalizedName
        self._textureName = textureName
    
    def getBlockTexturePath(self, textureName):
        return bpy.path.abspath("//textures/blocks/" + textureName + ".png")

    def make(self, x, y, z, metadata):
        obj = self.makeObject(x, y, z, metadata)
        self.makeUVMap(obj, metadata)
        self.applyMaterial(obj, metadata)
    
    def makeObject(self, x, y, z, metadata):
        mesh = bpy.data.meshes.new(name="Block")
        mesh.from_pydata([[-0.5,-0.5,-0.5],[0.5,-0.5,-0.5],[-0.5,0.5,-0.5],[0.5,0.5,-0.5],[-0.5,-0.5,0.5],[0.5,-0.5,0.5],[-0.5,0.5,0.5],[0.5,0.5,0.5]],[],[[0,1,3,2],[4,5,7,6],[0,1,5,4],[0,2,6,4],[2,3,7,6],[1,3,7,5]])
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
        obj.data.uv_layers[0].data.foreach_set("uv", [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1])
    
    def applyMaterial(self, obj, metadata):
        try:
            mat = bpy.data.materials[self._unlocalizedName]
        except KeyError:
            mat = bpy.data.materials.new(self._unlocalizedName)
            mat.use_nodes = True
            mat.node_tree.nodes["Material Output"].location = [300, 0]
            mat.node_tree.nodes["Diffuse BSDF"].location = [100, 0]
            
            #Initialize Texture
            try:
                tex = bpy.data.images[self._unlocalizedName]
            except KeyError:
                tex = bpy.data.images.load(self.getBlockTexturePath(self._textureName))
                tex.name = self._unlocalizedName

            #First Image Texture
            mat.node_tree.nodes.new(type="ShaderNodeTexImage")
            mat.node_tree.nodes["Image Texture"].location = [-100, 75]
            mat.node_tree.nodes["Image Texture"].image = tex
            mat.node_tree.nodes["Image Texture"].interpolation = "Closest"
            mat.node_tree.nodes["Image Texture"].projection = "BOX"
            mat.node_tree.links.new(mat.node_tree.nodes["Image Texture"].outputs[0], mat.node_tree.nodes["Diffuse BSDF"].inputs[0])
            
            #UV Map
            mat.node_tree.nodes.new(type="ShaderNodeUVMap")
            mat.node_tree.nodes["UV Map"].location = [-300, 0]
            mat.node_tree.nodes["UV Map"].uv_map = "UVMap"
            mat.node_tree.links.new(mat.node_tree.nodes["UV Map"].outputs[0], mat.node_tree.nodes["Image Texture"].inputs[0])
        
        obj.data.materials.append(mat)
