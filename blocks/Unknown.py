import bpy

class Block:
    """A basic block with a single texture
    
    This class should be inherited by every other block class
    """

    def __init__(self, id, metadata, unlocalizedName):
        self._id = id
        self._metadata = metadata
        self._unlocalizedName = unlocalizedName
    
    def applyMaterial(self, obj):
        try:
            mat = bpy.data.materials[self._unlocalizedName]
        #end try
        except KeyError:
            mat = bpy.data.materials.new(self._unlocalizedName)
        #end KeyError
        mat.use_nodes = True
        mat.node_tree.nodes["Diffuse BSDF"].inputs[0].default_value = (1, 0, 1, 1)

        obj.data.materials.append(mat)