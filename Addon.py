import math
import bpy
import mathutils
from bpy.props import (StringProperty)
from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator
import nbt
import importlib
import Blocks
importlib.reload(Blocks)
 
class SchematicImporter(Operator, ImportHelper) :
    bl_idname = "import.schematic"
    bl_label = "Import Schematic"
 
    def execute(self, context) :
        filename_ext = ".schematic"
        
        filter_glob = StringProperty(default="*.schematic", options={'HIDDEN'},)

        if self.filepath.split('\\')[-1].split('.')[1].lower() != 'schematic':
            print ("  Selected file = ", self.filepath)
            raise IOError("The selected input file is not a *.schematic file")
        #end if

        nbtfile = nbt.nbt.NBTFile(self.filepath,'rb')

        height = nbtfile["Height"].value
        width = nbtfile["Width"].value
        length = nbtfile["Length"].value

        bpy.data.scenes[0].render.engine = "CYCLES"
        for index, dataValue in enumerate(nbtfile["Blocks"].value):
            if dataValue != 0:
                Blocks.Blocks.draw(context, index % width - math.floor(width / 2), math.floor((index % (width * length)) / width) - math.floor(length / 2), math.floor(index / (width * length)), dataValue, nbtfile["Data"][index])
            #end if
        #end for

        return {"FINISHED"}
    #end invoke
#end SchematicImporter

# -----------------------------------------------------------------------------
# Register

def import_images_button(self, context):
    self.layout.operator(SchematicImporter.bl_idname, text="MCEdit Schematic (.schematic)")
#end import_images_button

def register() :
    bpy.utils.register_class(SchematicImporter)
    bpy.types.INFO_MT_file_import.append(import_images_button)
#end register
 
def unregister() :
    bpy.utils.unregister_class(SchematicImporter)
    bpy.types.INFO_MT_mesh_add.remove(import_images_button)
#end unregister
 
if __name__ == "__main__" :
    register()
#end if