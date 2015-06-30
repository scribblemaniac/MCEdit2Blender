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
        
        obj = Slab.makeObject(self, x, y, z, metadata)
        Slab.makeUVMap(self, obj, metadata)
        Multitextured.applyMaterial(self, obj, metadata)
        
        self._unlocalizedName = tempUnlocalizedName
