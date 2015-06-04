import bpy
from Block import Block
from Unknown import Unknown

class DataValues(Block):
    """A block that renders differently based on the its metadata
    
    The blockList can be one of two things:
        - a list of objects that are instances of blocks.Block. The Block object at index == metadata is the one that will be added to the scene.
        - a dict with values that are instances of blocks.Block and keys for the block's coresponding metadata.
    """

    def __init__(self, id, blockList):
        self._id = id
        self._blockList = blockList

    def make(self, x, y, z, metadata):
        try:
            if self._blockList[metadata] is None:
                unknownBlock = Unknown(self._id, metadata, "Unknown " + str(id))
                unknownBlock.make(x, y, z, metadata)
            else:
                self._blockList[metadata].make(x, y, z, metadata)
        except IndexError:
            unknownBlock = Unknown(self._id, metadata, "Unknown " + str(id))
            unknownBlock.make(x, y, z, metadata)
