import bpy
import mathutils
from Block import Block

class Log(Block):
    """A log block"""

    def __init__(self, id, unlocalizedName, topTexture, sideTexture):
        self._id = id
        self._unlocalizedName = unlocalizedName
        self._topTexture = topTexture
        self._sideTexture = self._textureName = sideTexture
    
    def applyMaterial(self, obj, metadata):
        if metadata & 0xC == 0xC:
            Block.applyMaterial(self, obj, metadata)
            return;
        tempUnlocalizedName = self._unlocalizedName
        self._unlocalizedName += " Side"
        Block.applyMaterial(self, obj, metadata) #Side texture material
        self._textureName = self._topTexture
        self._unlocalizedName = tempUnlocalizedName + " Top"
        Block.applyMaterial(self, obj, metadata) #Top texture material
        self._textureName = self._sideTexture
        self._unlocalizedName = tempUnlocalizedName
        if metadata & 0x8:
            isTop = [False, False, True, False, True, False]
        elif metadata & 0x4:
            isTop = [False, False, False, True, False, True]
        else:
            isTop = [True, True, False, False, False, False]
        for i in range(0,6):
            obj.data.polygons[i].material_index = int(isTop[i])
