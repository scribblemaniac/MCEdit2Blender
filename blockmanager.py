import bpy
import sys
sys.path.append("/Users/connor/git/MCEdit2Blender/")
import importlib
import blocks
import blocks.Block
importlib.reload(blocks.Block)
from blocks.Block import Block
import blocks.Unknown
importlib.reload(blocks.Unknown)
from blocks.Unknown import Unknown
import blocks.DataValues
importlib.reload(blocks.DataValues)
from blocks.DataValues import DataValues
import blocks.Log
importlib.reload(blocks.Log)
from blocks.Log import Log
import blocks.Multitextured
importlib.reload(blocks.Multitextured)
from blocks.Multitextured import Multitextured
import blocks.Slab
importlib.reload(blocks.Slab)
from blocks.Slab import Slab
import blocks.MultitexturedSlab
importlib.reload(blocks.MultitexturedSlab)
from blocks.MultitexturedSlab import MultitexturedSlab
import blocks.Stairs
importlib.reload(blocks.Stairs)
from blocks.Stairs import Stairs
import blocks.MultitexturedStairs
importlib.reload(blocks.MultitexturedStairs)
from blocks.MultitexturedStairs import MultitexturedStairs
import blocks.Transparent
importlib.reload(blocks.Transparent)
from blocks.Transparent import Transparent
import blocks.Farmland
importlib.reload(blocks.Farmland)
from blocks.Farmland import Farmland
import blocks.Plant
importlib.reload(blocks.Plant)
from blocks.Plant import Plant

class BlockManager:
    _BlockDict = {}
    
    def draw(self, context, x, y, z, id, metadata):
        if id != 0:
            try:
                self._BlockDict[id].make(x, y, z, metadata)
            except KeyError:
                unknownBlock = Unknown(id, metadata, "Unknown " + str(id))
                unknownBlock.make(x, y, z, metadata)
    
    def addBlock(self, id, block):
        self._BlockDict[id] = block

    def __init__(self):
        self.addBlock(1, Block(1, "Stone", "stone"))
        self.addBlock(3, Block(3, "Dirt", "dirt"))
        self.addBlock(4, Block(4, "Cobblestone", "cobblestone"))
        self.addBlock(5, DataValues(5, [Block(5, "Oak Wood Planks", "planks_oak"), Block(5, "Spruce Wood Planks", "planks_spruce"), Block(5, "Birch Wood Planks", "planks_birch"), Block(5, "Jungle Wood Planks", "planks_jungle")]))
        self.addBlock(6, DataValues(6, [Plant(6, "Oak Sapling", "sapling_oak"), Plant(6, "Spruce Sapling", "sapling_spruce"), Plant(6, "Birch Sapling", "sapling_birch"), Plant(6, "Jungle Sapling", "sapling_jungle")]*4));
        self.addBlock(7, Block(7, "Block", "bedrock"))
        self.addBlock(12, Block(12, "Sand", "sand"))
        self.addBlock(13, Block(13, "Gravel", "gravel"))
        self.addBlock(14, Block(14, "Gold Ore", "oreGold"))
        self.addBlock(15, Block(15, "Iron Ore", "oreIron"))
        self.addBlock(16, Block(16, "Coal Ore", "oreCoal"))
        self.addBlock(17, DataValues(17, [Log(17, "Oak Log", "tree_top", "tree_side"), Log(17, "Spruce Wood", "tree_top", "tree_spruce"), None, None ]*4))
        self.addBlock(19, Block(19, "Sponge", "sponge"))
        self.addBlock(20, Transparent(20, "Glass", "glass"))
        self.addBlock(21, Block(21, "Lapis Lazuli Ore", "oreLapis"))
        self.addBlock(22, Block(22, "Lapis Lazuli Block", "blockLapis"))
        self.addBlock(24, DataValues(24, [Multitextured(24, "Sandstone(0)", "sandstone_bottom", "sandstone_top", "sandstone_side"), Multitextured(24, "Sandstone(1)", textureTop="sandstone_top", textureFront="sandstone_carved"), Multitextured(24, "Sandstone(2)", textureTop="sandstone_top", textureFront="sandstone_smooth")]))
        self.addBlock(25, Block(25, "Note Block", "musicBlock"))
        self.addBlock(35, DataValues(35, [Block(35, "White Wool", "cloth_0"), Block(35, "Orange Wool", "cloth_1"), Block(35, "Magenta Wool", "cloth_2"), Block(35, "Light Blue Wool", "cloth_3"), Block(35, "Yellow Wool", "cloth_4"), Block(35, "Lime Wool", "cloth_5"), Block(35, "Pink Wool", "cloth_6"), Block(35, "Gray Wool", "cloth_7"), Block(35, "Light Gray Wool", "cloth_8"), Block(35, "Cyan Wool", "cloth_9"), Block(35, "Purple Wool", "cloth_10"), Block(35, "Blue Wool", "cloth_11"), Block(35, "Brown Wool", "cloth_12"), Block(35, "Green Wool", "cloth_13"), Block(35, "Red Wool", "cloth_14"), Block(35, "Black Wool", "cloth_15")]))
        self.addBlock(39, Plant(39, "Brown Mushroom", "mushroom_brown"))
        self.addBlock(40, Plant(40, "Red Mushroom", "mushroom_red"))
        self.addBlock(41, Block(41, "Gold Block", "blockGold"))
        self.addBlock(42, Block(42, "Iron Block", "blockIron"))
        self.addBlock(43, DataValues(43, [Multitextured(43, "Double Stone Slab", textureTop="stoneslab_top", textureFront="stoneslab_side"), Multitextured(43, "Double Sandstone Slab", "sandstone_bottom", "sandstone_top", "sandstone_side"), Block(43, "Double Wooden Slab (Stone)", "planks_oak"), Block(43, "Double Cobblestone Slab", "cobblestone"), Block(43, "Double Brick Slab", "brick"), Block(43, "Double Stone Brick Slab", "stonebrick"), Block(43, "Double Nether Brick Slab", "netherBrick"), Multitextured(43, "Double Quartz Slab", "quartzblock_bottom", "quartzblock_top", "quartzblock_side"), Block(43, "Double Smooth Stone Slab", "stoneslab_top"), Block(43, "Double Smooth Sandstone Slab", "sandstone_top")]))
        self.addBlock(44, DataValues(44, [MultitexturedSlab(44, "Stone Slab", textureTop="stoneslab_top", textureFront="stoneslab_side"), MultitexturedSlab(44, "Sandstone Slab", "sandstone_bottom", "sandstone_top", "sandstone_side"), Slab(44, "Wooden Slab (Stone)", "planks_oak"), Slab(44, "Cobblestone Slab", "cobblestone"), Slab(44, "Brick Slab", "brick"), Slab(44, "Stone Brick Slab", "stonebrick"), Slab(44, "Nether Brick Slab", "netherBrick"), MultitexturedSlab(44, "Quartz Slab", "quartzblock_bottom", "quartzblock_top", "quartzblock_side")]*2))
        self.addBlock(45, Block(45, "Brick Block", "brick"))
        self.addBlock(46, Multitextured(46, "TNT", "tnt_bottom", "tnt_top", "tnt_side"))
        self.addBlock(47, Multitextured(47, "Bookshelf", textureTop="planks_oak", textureFront="bookshelf"))
        self.addBlock(48, Block(48, "Moss Stone", "stoneMoss"))
        self.addBlock(49, Block(49, "Obsidian", "obsidian"))
        self.addBlock(53, Stairs(53, "Oak Wood Stairs", "planks_oak"))
        self.addBlock(56, Block(56, "Diamond Ore", "oreDiamond"))
        self.addBlock(57, Block(57, "Diamond Block", "blockDiamond"))
        self.addBlock(58, Multitextured(58, "Crafting Table", "planks_oak", "workbench_top", "workbench_front", "workbench_front", "workbench_side", "workbench_side"))
        self.addBlock(60, DataValues(60, [Farmland(60, "Dry Farmland", "dirt", "farmland_dry", "dirt"), Farmland(60, "Wet Farmland", "dirt", "farmland_wet", "dirt"), Farmland(60, "Wet Farmland", "dirt", "farmland_wet", "dirt"), Farmland(60, "Wet Farmland", "dirt", "farmland_Wet", "dirt"), Farmland(60, "Wet Farmland", "dirt", "farmland_wet", "dirt"), Farmland(60, "Wet Farmland", "dirt", "farmland_wet", "dirt"), Farmland(60, "Wet Farmland", "dirt", "farmland_wet", "dirt"), Farmland(60, "Wet Farmland", "dirt", "farmland_wet", "dirt")]))
        self.addBlock(67, Stairs(67, "Cobblestone Stairs", "cobblestone"))
        self.addBlock(73, Block(73, "Redstone Ore", "oreRedstone"))
        self.addBlock(74, Block(74, "Glowing Redstone Ore", "oreRedstone"))
        self.addBlock(79, Block(79, "Ice", "ice"))
        self.addBlock(80, Block(80, "Snow Block", "blockSnow"))
        self.addBlock(82, Block(82, "Clay Block", "clay"))
        self.addBlock(84, Multitextured(84, "Jukebox", "musicBlock", "jukebox_top", "musicBlock"))
        self.addBlock(86, DataValues(86, [Multitextured(86, "Pumpkin (0)", "pumpkin_top", "pumpkin_top", "pumpkin_side", "pumpkin_side", "pumpkin_face", "pumpkin_side"), Multitextured(86, "Pumpkin (1)", "pumpkin_top", "pumpkin_top", "pumpkin_side", "pumpkin_face", "pumpkin_side", "pumpkin_side"), Multitextured(86, "Pumpkin (2)", "pumpkin_top", "pumpkin_top", "pumpkin_face", "pumpkin_side", "pumpkin_side", "pumpkin_side"), Multitextured(86, "Pumpkin (3)", "pumpkin_top", "pumpkin_top", "pumpkin_side", "pumpkin_side", "pumpkin_side", "pumpkin_face"), Multitextured(86, "Pumpkin (4)", textureTop="pumpkin_top", textureFront="texture_side")]))
        self.addBlock(87, Block(87, "Netherrack", "hellrock"))
        self.addBlock(88, Block(88, "Soul Sand", "hellsand"))
        self.addBlock(89, Block(89, "Glowstone Block", "lightgem"))
        self.addBlock(91, DataValues(86, [Multitextured(86, "Jack O'Lantern (0)", "pumpkin_top", "pumpkin_top", "pumpkin_side", "pumpkin_side", "pumpkin_jack", "pumpkin_side"), Multitextured(86, "Jack O'Lantern (1)", "pumpkin_top", "pumpkin_top", "pumpkin_side", "pumpkin_jack", "pumpkin_side", "pumpkin_side"), Multitextured(86, "Jack O'Lantern (2)", "pumpkin_top", "pumpkin_top", "pumpkin_jack", "pumpkin_side", "pumpkin_side", "pumpkin_side"), Multitextured(86, "Jack O'Lantern (3)", "pumpkin_top", "pumpkin_top", "pumpkin_side", "pumpkin_side", "pumpkin_side", "pumpkin_jack"), Multitextured(86, "Jack O'Lantern (4)", textureTop="pumpkin_top", textureFront="texture_side")]))
        self.addBlock(95, DataValues(95, [Transparent(95, "White Stained Glass", "glass_white"), Transparent(95, "Orange Stained Glass", "glass_orange"), Transparent(95, "Magenta Stained Glass", "glass_magenta"), Transparent(95, "Light Blue Stained Glass", "glass_light_blue"), Transparent(95, "Yellow Stained Glass", "glass_yellow"), Transparent(95, "Lime Stained Glass", "glass_lime"), Transparent(95, "Pink Stained Glass", "glass_pink"), Transparent(95, "Gray Stained Glass", "glass_gray"), Transparent(95, "Light Gray Stained Glass", "glass_silver"), Transparent(95, "Cyan Stained Glass", "glass_cyan"), Transparent(95, "Purple Stained Glass", "glass_purple"), Transparent(95, "Blue Stained Glass", "glass_blue"), Transparent(95, "Brown Stained Glass", "glass_brown"), Transparent(95, "Green Stained Glass", "glass_green"), Transparent(95, "Red Stained Glass", "glass_red"), Transparent(95, "Black Stained Glass", "glass_black")]))
        self.addBlock(97, Block(97, "Silverfish Stone", "stone"))
        self.addBlock(98, Block(98, "Stone Brick", "stonebrick"))
        self.addBlock(103, Multitextured(103, "Melon", textureTop="melon_top", textureFront="melon_side"))
        self.addBlock(108, Stairs(108, "Brick Stairs", "brick"))
        self.addBlock(109, Stairs(109, "Stone Brick Stairs", "stonebrick"))
        self.addBlock(110, Multitextured(110, "Mycelium", "dirt", "mycel_top", "mycel_side"))
        self.addBlock(112, Block(112, "Nether Brick", "netherBrick"))
        self.addBlock(114, Stairs(114, "Nether Brick Stairs", "netherBrick"))
        self.addBlock(121, Block(121, "End Stone", "whiteStone"))
        self.addBlock(123, Block(123, "Redstone Lamp (Inactive)", "redstoneLight"))
        self.addBlock(124, Block(124, "Redstone Lamp (Active)", "redstoneLight_lit"))
        self.addBlock(125, DataValues(125, [Block(125, "Double Oak Wood Slab", "planks_oak"), Block(125, "Double Spruce Wood Slab", "planks_spruce"), Block(125, "Double Birch Wood Slab", "planks_birch"), Block(125, "Double Jungle Wood Slab", "planks_jungle")]))
        self.addBlock(126, DataValues(126, [Slab(126, "Oak Wood Slab", "planks_oak"), Slab(126, "Spruce Wood Slab", "planks_spruce"), Slab(126, "Birch Wood Slab", "planks_birch"), Slab(126, "Jungle Wood Slab", "planks_jungle")]*2))
        self.addBlock(128, MultitexturedStairs(128, "Sandstone Stairs", "sandstone_bottom", "sandstone_top", "sandstone_side"))
        self.addBlock(129, Block(129, "Emerald Ore", "oreEmerald"))
        self.addBlock(133, Block(133, "Block of Emerald", "blockEmerald"))
        self.addBlock(134, Stairs(134, "Spruce Wood Stairs", "planks_spruce"))
        self.addBlock(135, Stairs(135, "Birch Wood Stairs", "planks_birch"))
        self.addBlock(136, Stairs(136, "Jungle Wood Stairs", "planks_jungle"))
        self.addBlock(137, Block(137, "Command Block", "commandBlock"))
        self.addBlock(152, Block(152, "Block of Redstone", "blockRedstone"))
        self.addBlock(153, Block(153, "Nether Quartz Ore", "netherquartz"))
        self.addBlock(155, DataValues(155, [Multitextured(155, "Block of Quartz", "quartzblock_bottom", "quartzblock_top", "quartzblock_side"), Multitextured(155, "Chiseled Quartz Block", textureTop="quartzblock_chiseled_top", textureFront="quartzblock_chiseled")]))
        self.addBlock(156, MultitexturedStairs(156, "Quartz Stairs", "quartzblock_bottom", "quartzblock_top", "quartzblock_side"))