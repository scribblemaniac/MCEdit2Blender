import bpy
from Block import Block

class DataValues(Block):
    """A block that renders differently based on the its metadata
    
    The blockList should be a list of tuples containing exactly three elements. This first is a metadata mask. The second is an integer that is compared to the masked metadata. If the comparison evaluates to true, make is called for the block third element. When make is called, the condition metadata & arg1 == arg2 is evaluated for each element starting from the beginning until a condition evaluates to true. This means that the elements in blockList are in order of decreasing precedence.
    
    If the first element of a tuple is None, it is assumed to be 0xFF.
    If the second element of a tuple is None, it is assumed to be equal to the index of the tuple in the list.
    """

    def __init__(self, id, metadata, blockList):
        self._id = id
        self._metadata = metadata
        self._unlocalizedName = unlocalizedName
        self._blockList = blockList
        for index, blockInfo in enumerate(self._blockList):
            if blockInfo[0] is None:
                blockInfo[0] = 0xFF
            if blockInfo[1] is None:
                blockInfo[1] = index

    def make(self):
        for blockInfo in self._blockList:
            if self._metadata & blockInfo[0] == blockInfo[1]:
                self._blockList[self._metadata].make()
