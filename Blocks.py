import math
import bpy
import mathutils
from bpy.props import (StringProperty)
from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator
import nbt
import os.path

class Blocks() :
    def getDisplayName(id):
        return Blocks.BlockDict[id][1]
    #end getDisplayName

    # TODO Define deal with data values
    def getBlockTexturePath(textureName):
        return bpy.path.abspath("//textures/blocks/" + textureName + ".png")
    #end getTexturePath

    #deprecated
    #use args value passed to draw function
    def getBlockArg(id, index):
        return Blocks.BlockDict[id][2][index]
    #end getBlockArg

    def draw(context, x, y, z, id, metadata):
        if id != 0:
            Blocks.BlockDict[id][0](context, x, y, z, id, metadata, Blocks.getDisplayName(id), Blocks.BlockDict[id][2])
        #end if
    #end draw

    def drawRegularCube(context, x, y, z, id, metadata, displayName, args):
        mesh = bpy.data.meshes.new(name="Block")
        mesh.from_pydata([[-0.5,-0.5,-0.5],[0.5,-0.5,-0.5],[-0.5,0.5,-0.5],[0.5,0.5,-0.5],[-0.5,-0.5,0.5],[0.5,-0.5,0.5],[-0.5,0.5,0.5],[0.5,0.5,0.5]],[],[[0,1,3,2],[4,5,7,6],[0,1,5,4],[0,2,6,4],[2,3,7,6],[1,3,7,5]])
        mesh.update()

        obj = bpy.data.objects.new("Block", mesh)
        obj.location.x = x + 0.5
        obj.location.y = y + 0.5
        obj.location.z = z + 0.5
        context.scene.objects.link(obj)

        bpy.context.scene.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.object.editmode_toggle()

        try:
            mat = bpy.data.materials[displayName]
        #end try
        except KeyError:
            mat = bpy.data.materials.new(displayName)
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
                tex = bpy.data.images[displayName]
            #end try
            except KeyError:
                tex = bpy.data.images.load(Blocks.getBlockTexturePath(args[0]))
                tex.name = displayName
            #end KeyError

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
        #end KeyError

        obj.data.materials.append(mat)
    #end drawRegularCube

    def drawUnknown(context, x, y, z, id, metadata, displayName, args):
        mesh = bpy.data.meshes.new(name="Block")
        mesh.from_pydata([[-0.5,-0.5,-0.5],[0.5,-0.5,-0.5],[-0.5,0.5,-0.5],[0.5,0.5,-0.5],[-0.5,-0.5,0.5],[0.5,-0.5,0.5],[-0.5,0.5,0.5],[0.5,0.5,0.5]],[],[[0,1,3,2],[4,5,7,6],[0,1,5,4],[0,2,6,4],[2,3,7,6],[1,3,7,5]])
        mesh.update()

        obj = bpy.data.objects.new("Block", mesh)
        obj.location.x = x + 0.5
        obj.location.y = y + 0.5
        obj.location.z = z + 0.5
        context.scene.objects.link(obj)

        bpy.context.scene.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.object.editmode_toggle()

        try:
            mat = bpy.data.materials[displayName]
        #end try
        except KeyError:
            mat = bpy.data.materials.new(displayName)
        #end KeyError
        mat.use_nodes = True
        mat.node_tree.nodes["Diffuse BSDF"].inputs[0].default_value = (1, 0, 1, 1)

        obj.data.materials.append(mat)
    #end drawUnknown

    def drawMultitextured(context, x, y, z, id, metadata, displayName, args):
        mesh = bpy.data.meshes.new(name="Block")
        mesh.from_pydata([[-0.5,-0.5,-0.5],[0.5,-0.5,-0.5],[-0.5,0.5,-0.5],[0.5,0.5,-0.5],[-0.5,-0.5,0.5],[0.5,-0.5,0.5],[-0.5,0.5,0.5],[0.5,0.5,0.5]],[],[[0,1,3,2],[4,5,7,6],[0,1,5,4],[0,2,6,4],[2,3,7,6],[1,3,7,5]])
        mesh.update()

        obj = bpy.data.objects.new("Block", mesh)
        obj.location.x = x + 0.5
        obj.location.y = y + 0.5
        obj.location.z = z + 0.5
        context.scene.objects.link(obj)

        bpy.context.scene.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.object.editmode_toggle()

        sideMapping = ["Bottom", "Top", "Front", "Left", "Back", "Right"]
        for index, sideName in enumerate(sideMapping):
            try:
                mat = bpy.data.materials[displayName + " " + sideName]
            #end try
            except KeyError:
                mat = bpy.data.materials.new(displayName + " " + sideName)
                mat.use_nodes = True
                mat.node_tree.nodes["Material Output"].location = [400, 0]
                mat.node_tree.nodes["Diffuse BSDF"].location = [200, 0]

                try:
                    tex = bpy.data.images[displayName + " " + sideName]
                #end try
                except KeyError:
                    tex = bpy.data.images.load(Blocks.getBlockTexturePath(args[index]))
                    tex.name = displayName + " " + sideName
                #end KeyError
                mat.node_tree.nodes.new(type="ShaderNodeTexImage")
                mat.node_tree.nodes["Image Texture"].location = [0, 0]
                mat.node_tree.nodes["Image Texture"].image = tex
                mat.node_tree.nodes["Image Texture"].interpolation = "Closest"
                mat.node_tree.nodes["Image Texture"].projection = "BOX"
                mat.node_tree.links.new(mat.node_tree.nodes["Image Texture"].outputs[0], mat.node_tree.nodes["Diffuse BSDF"].inputs[0])

                mat.node_tree.nodes.new(type="ShaderNodeTexCoord")

                if index < 2:
                    mat.node_tree.nodes.new(type="ShaderNodeMapping")
                    mat.node_tree.nodes["Mapping"].location = [-400, 0]
                    mat.node_tree.nodes["Mapping"].rotation = mathutils.Euler((0.0, 0.0, -1.5707963705062866), 'XYZ')
                    mat.node_tree.nodes["Mapping"].scale[0] = -1.0
                    mat.node_tree.links.new(mat.node_tree.nodes["Mapping"].outputs[0], mat.node_tree.nodes["Image Texture"].inputs[0])
                    mat.node_tree.nodes["Texture Coordinate"].location = [-600, 0]
                    mat.node_tree.links.new(mat.node_tree.nodes["Texture Coordinate"].outputs[0], mat.node_tree.nodes["Mapping"].inputs[0])
                elif index == 3 or index == 5:
                    mat.node_tree.nodes.new(type="ShaderNodeMapping")
                    mat.node_tree.nodes["Mapping"].location = [-400, 0]
                    mat.node_tree.nodes["Mapping"].scale[1] = -1.0
                    mat.node_tree.links.new(mat.node_tree.nodes["Mapping"].outputs[0], mat.node_tree.nodes["Image Texture"].inputs[0])
                    mat.node_tree.nodes["Texture Coordinate"].location = [-600, 0]
                    mat.node_tree.links.new(mat.node_tree.nodes["Texture Coordinate"].outputs[0], mat.node_tree.nodes["Mapping"].inputs[0])
                else:
                    mat.node_tree.links.new(mat.node_tree.nodes["Texture Coordinate"].outputs[0], mat.node_tree.nodes["Image Texture"].inputs[0])
                    mat.node_tree.nodes["Texture Coordinate"].location = [-200, 0]
                #end else
            #end KeyError

            obj.data.materials.append(mat)
        #end sideMapping loop

        i = 0
        while i < 6:
            obj.data.polygons[i].material_index = i
            i += 1
    #end drawMultitextured

    def drawDataValues(context, x, y, z, id, metadata, displayName, args):
        args[metadata][0](context, x, y, z, id, metadata, args[metadata][1], args[metadata][2])
    #end drawDataValues

    def drawLog(context, x, y, z, id, metadata, displayName, args):
        if metadata & 0xC == 0xC:
            Blocks.drawRegularCube(context, x, y, z, id, metadata, displayName, [args[1]])
        elif metadata & 0x4:
            Blocks.drawMultitextured(context, x, y, z, id, metadata, displayName + "(EW)", [args[1], args[1], args[1], args[0], args[1], args[0]])
        elif metadata & 0x8:
            Blocks.drawMultitextured(context, x, y, z, id, metadata, displayName + "(NS)", [args[1], args[1], args[0], args[1], args[0], args[1]])
        else:
            Blocks.drawMultitextured(context, x, y, z, id, metadata, displayName + "(UD)", [args[0], args[0], args[1], args[1], args[1], args[1]])
        #end else
    #end drawLog

    def drawLogDataValues(context, x, y, z, id, metadata, displayName, args):
        args[metadata & 3][0](context, x, y, z, id, metadata, args[metadata & 3][1], args[metadata & 3][2])
    #end drawLogDataValues

    def drawCloth(context, x, y, z, id, metadata, displayName, args):
        colorMapping = ["White", "Orange", "Magenta", "Light Blue", "Yellow", "Lime", "Pink", "Gray", "Light Gray", "Cyan", "Purple", "Blue", "Brown", "Green", "Red", "Black"]
        Blocks.drawRegularCube(context, x, y, z, id, metadata, colorMapping[metadata] + " " + displayName, ["cloth_" + str(metadata)])
    #end drawCloth

    def drawStairs(context, x, y, z, id, metadata, displayName, args):
        mesh = bpy.data.meshes.new(name="Block")
        mesh.from_pydata([[0.5, 0.5, 0.5], [0.5, -0.5, 0.5], [0.5, 0.5, -0.5], [0.5, -0.5, -0.5], [0, 0.5, 0.5], [0, -0.5, 0.5], [0, 0.5, 0], [0, -0.5, 0], [-0.5, 0.5, 0], [-0.5, -0.5, 0], [-0.5, 0.5, -0.5], [-0.5, -0.5, -0.5]], [], [[0,1,3,2], [0,2,10,8,6,4], [1,3,11,9,7,5], [0,1,5,4], [4,5,7,6], [6,7,9,8], [8,9,11,10], [2,3,11,10]])
        mesh.update()

        obj = bpy.data.objects.new("Block", mesh)
        obj.location.x = x + 0.5
        obj.location.y = y + 0.5
        obj.location.z = z + 0.5
        obj.rotation_euler.y = 3.1415927410125732 * (metadata >> 2 & 1)
        obj.rotation_euler.z = 3.1415927410125732 * ((metadata & 1) + (metadata >> 2 & 1)) + 1.5707963705062866 * (metadata >> 1 & 1)
        context.scene.objects.link(obj)
        bpy.ops.object.select_pattern(pattern=obj.name, extend=False)
        bpy.ops.object.transform_apply(rotation=True)
        obj.select = False

        bpy.context.scene.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.object.editmode_toggle()

        try:
            mat = bpy.data.materials[displayName]
        #end try
        except KeyError:
            mat = bpy.data.materials.new(displayName)
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
                tex = bpy.data.images[displayName]
            #end try
            except KeyError:
                tex = bpy.data.images.load(Blocks.getBlockTexturePath(args[0]))
                tex.name = displayName
            #end KeyError

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
        #end KeyError

        obj.data.materials.append(mat)
    #end drawStairs

    def drawMultitexturedStairs(context, x, y, z, id, metadata, displayName, args):
        mesh = bpy.data.meshes.new(name="Block")
        mesh.from_pydata([[0.5, 0.5, 0.5], [0.5, -0.5, 0.5], [0.5, 0.5, -0.5], [0.5, -0.5, -0.5], [0, 0.5, 0.5], [0, -0.5, 0.5], [0, 0.5, 0], [0, -0.5, 0], [-0.5, 0.5, 0], [-0.5, -0.5, 0], [-0.5, 0.5, -0.5], [-0.5, -0.5, -0.5]], [], [[0,1,3,2], [0,2,10,8,6,4], [1,3,11,9,7,5], [0,1,5,4], [4,5,7,6], [6,7,9,8], [8,9,11,10], [2,3,11,10]])
        mesh.update()

        obj = bpy.data.objects.new("Block", mesh)
        obj.location.x = x + 0.5
        obj.location.y = y + 0.5
        obj.location.z = z + 0.5
        obj.rotation_euler.y = 3.1415927410125732 * (metadata >> 2 & 1)
        obj.rotation_euler.z = 3.1415927410125732 * ((metadata & 1) + (metadata >> 2 & 1)) + 1.5707963705062866 * (metadata >> 1 & 1)
        context.scene.objects.link(obj)
        bpy.ops.object.select_pattern(pattern=obj.name, extend=False)
        bpy.ops.object.transform_apply(rotation=True)
        obj.select = False

        bpy.context.scene.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.object.editmode_toggle()

        sideMapping = ["Bottom", "Top", "Front", "Left", "Back", "Right"]
        for index, sideName in enumerate(sideMapping):
            try:
                mat = bpy.data.materials[displayName + " " + sideName]
            #end try
            except KeyError:
                mat = bpy.data.materials.new(displayName + " " + sideName)
                mat.use_nodes = True
                mat.node_tree.nodes["Material Output"].location = [400, 0]
                mat.node_tree.nodes["Diffuse BSDF"].location = [200, 0]

                try:
                    tex = bpy.data.images[displayName + " " + sideName]
                #end try
                except KeyError:
                    tex = bpy.data.images.load(Blocks.getBlockTexturePath(args[index]))
                    tex.name = displayName + " " + sideName
                #end KeyError
                mat.node_tree.nodes.new(type="ShaderNodeTexImage")
                mat.node_tree.nodes["Image Texture"].location = [0, 0]
                mat.node_tree.nodes["Image Texture"].image = tex
                mat.node_tree.nodes["Image Texture"].interpolation = "Closest"
                mat.node_tree.nodes["Image Texture"].projection = "BOX"
                mat.node_tree.links.new(mat.node_tree.nodes["Image Texture"].outputs[0], mat.node_tree.nodes["Diffuse BSDF"].inputs[0])

                mat.node_tree.nodes.new(type="ShaderNodeTexCoord")

                if index < 2:
                    mat.node_tree.nodes.new(type="ShaderNodeMapping")
                    mat.node_tree.nodes["Mapping"].location = [-400, 0]
                    mat.node_tree.nodes["Mapping"].rotation = mathutils.Euler((0.0, 0.0, -1.5707963705062866), 'XYZ')
                    mat.node_tree.nodes["Mapping"].scale[0] = -1.0
                    mat.node_tree.links.new(mat.node_tree.nodes["Mapping"].outputs[0], mat.node_tree.nodes["Image Texture"].inputs[0])
                    mat.node_tree.nodes["Texture Coordinate"].location = [-600, 0]
                    mat.node_tree.links.new(mat.node_tree.nodes["Texture Coordinate"].outputs[0], mat.node_tree.nodes["Mapping"].inputs[0])
                elif index == 3 or index == 5:
                    mat.node_tree.nodes.new(type="ShaderNodeMapping")
                    mat.node_tree.nodes["Mapping"].location = [-400, 0]
                    mat.node_tree.nodes["Mapping"].scale[1] = -1.0
                    mat.node_tree.links.new(mat.node_tree.nodes["Mapping"].outputs[0], mat.node_tree.nodes["Image Texture"].inputs[0])
                    mat.node_tree.nodes["Texture Coordinate"].location = [-600, 0]
                    mat.node_tree.links.new(mat.node_tree.nodes["Texture Coordinate"].outputs[0], mat.node_tree.nodes["Mapping"].inputs[0])
                else:
                    mat.node_tree.links.new(mat.node_tree.nodes["Texture Coordinate"].outputs[0], mat.node_tree.nodes["Image Texture"].inputs[0])
                    mat.node_tree.nodes["Texture Coordinate"].location = [-200, 0]
                #end else
            #end KeyError

            obj.data.materials.append(mat)
        #end sideMapping loop

        if metadata & 0x4:
            materialIndexMap = [5, 4, 2, 0, 3, 0, 3, 1]
        else:
            materialIndexMap = [5, 4, 2, 1, 3, 1, 3, 0]
        #end else
        for polygonIndex, materialIndex in enumerate(materialIndexMap):
            obj.data.polygons[polygonIndex].material_index = materialIndex
        #end for
    #end drawMultitexturedStairs

    def drawSlab(context, x, y, z, id, metadata, displayName, args):
        mesh = bpy.data.meshes.new(name="Block")
        mesh.from_pydata([[-0.5,-0.5,-0.25],[0.5,-0.5,-0.25],[-0.5,0.5,-0.25],[0.5,0.5,-0.25],[-0.5,-0.5,0.25],[0.5,-0.5,0.25],[-0.5,0.5,0.25],[0.5,0.5,0.25]],[],[[0,1,3,2],[4,5,7,6],[0,1,5,4],[0,2,6,4],[2,3,7,6],[1,3,7,5]])
        mesh.update()

        obj = bpy.data.objects.new("Block", mesh)
        obj.location.x = x + 0.5
        obj.location.y = y + 0.5
        obj.location.z = z + 0.25 + 0.5 * (metadata >> 3 & 1)
        context.scene.objects.link(obj)

        bpy.context.scene.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.object.editmode_toggle()
        
        if metadata & 8:
            displayName += " High"
        else:
            displayName += " Low"
        #end else

        try:
            mat = bpy.data.materials[displayName]
        #end try
        except KeyError:
            mat = bpy.data.materials.new(displayName)
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
                tex = bpy.data.images[displayName]
            #end try
            except KeyError:
                tex = bpy.data.images.load(Blocks.getBlockTexturePath(args[0]))
                tex.name = displayName
            #end KeyError

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
        #end KeyError

        obj.data.materials.append(mat)
    #end drawSlab

    def drawMultitexturedSlab(context, x, y, z, id, metadata, displayName, args):
        mesh = bpy.data.meshes.new(name="Block")
        mesh.from_pydata([[-0.5,-0.5,-0.25],[0.5,-0.5,-0.25],[-0.5,0.5,-0.25],[0.5,0.5,-0.25],[-0.5,-0.5,0.25],[0.5,-0.5,0.25],[-0.5,0.5,0.25],[0.5,0.5,0.25]],[],[[0,1,3,2],[4,5,7,6],[0,1,5,4],[0,2,6,4],[2,3,7,6],[1,3,7,5]])
        mesh.update()

        obj = bpy.data.objects.new("Block", mesh)
        obj.location.x = x + 0.5
        obj.location.y = y + 0.5
        obj.location.z = z + 0.25 + 0.5 * (metadata >> 3 & 1)
        context.scene.objects.link(obj)

        bpy.context.scene.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.object.editmode_toggle()

        if metadata & 8:
            displayName += " High"
        else:
            displayName += " Low"
        #end else

        sideMapping = ["Bottom", "Top", "Front", "Left", "Back", "Right"]
        for index, sideName in enumerate(sideMapping):
            try:
                mat = bpy.data.materials[displayName + " " + sideName]
            #end try
            except KeyError:
                mat = bpy.data.materials.new(displayName + " " + sideName)
                mat.use_nodes = True
                mat.node_tree.nodes["Material Output"].location = [400, 0]
                mat.node_tree.nodes["Diffuse BSDF"].location = [200, 0]

                try:
                    tex = bpy.data.images[displayName + " " + sideName]
                #end try
                except KeyError:
                    tex = bpy.data.images.load(Blocks.getBlockTexturePath(args[index]))
                    tex.name = displayName + " " + sideName
                #end KeyError
                mat.node_tree.nodes.new(type="ShaderNodeTexImage")
                mat.node_tree.nodes["Image Texture"].location = [0, 0]
                mat.node_tree.nodes["Image Texture"].image = tex
                mat.node_tree.nodes["Image Texture"].interpolation = "Closest"
                mat.node_tree.nodes["Image Texture"].projection = "BOX"
                mat.node_tree.links.new(mat.node_tree.nodes["Image Texture"].outputs[0], mat.node_tree.nodes["Diffuse BSDF"].inputs[0])

                mat.node_tree.nodes.new(type="ShaderNodeTexCoord")

                if index < 2:
                    mat.node_tree.nodes.new(type="ShaderNodeMapping")
                    mat.node_tree.nodes["Mapping"].location = [-400, 0]
                    mat.node_tree.nodes["Mapping"].rotation = mathutils.Euler((0.0, 0.0, -1.5707963705062866), 'XYZ')
                    mat.node_tree.nodes["Mapping"].scale[0] = -1.0
                    mat.node_tree.links.new(mat.node_tree.nodes["Mapping"].outputs[0], mat.node_tree.nodes["Image Texture"].inputs[0])
                    mat.node_tree.nodes["Texture Coordinate"].location = [-600, 0]
                    mat.node_tree.links.new(mat.node_tree.nodes["Texture Coordinate"].outputs[0], mat.node_tree.nodes["Mapping"].inputs[0])
                else:
                    mat.node_tree.nodes.new(type="ShaderNodeMapping")
                    mat.node_tree.nodes["Mapping"].location = [-400, 0]
                    if index == 3 or index == 5:
                        mat.node_tree.nodes["Mapping"].scale[1] = -1.0
                    #end if
                    mat.node_tree.nodes["Mapping"].scale[2] = 0.5
                    mat.node_tree.nodes["Mapping"].translation.z = 0.5 * (metadata >> 3 & 1)
                    mat.node_tree.links.new(mat.node_tree.nodes["Mapping"].outputs[0], mat.node_tree.nodes["Image Texture"].inputs[0])
                    mat.node_tree.nodes["Texture Coordinate"].location = [-600, 0]
                    mat.node_tree.links.new(mat.node_tree.nodes["Texture Coordinate"].outputs[0], mat.node_tree.nodes["Mapping"].inputs[0])
                #end else
            #end KeyError

            obj.data.materials.append(mat)
        #end sideMapping loop

        i = 0
        while i < 6:
            obj.data.polygons[i].material_index = i
            i += 1
    #end drawMultitexturedSlab
    
    def drawSlabDataValues(context, x, y, z, id, metadata, displayName, args):
        args[metadata & 7][0](context, x, y, z, id, metadata, args[metadata & 7][1], args[metadata & 7][2])
    #end drawSlabDataValues

    BlockDict = {0: (drawRegularCube, "Air", []), 1: (drawRegularCube, "Stone", ["stone"]), 2: (drawUnknown, "Grass", []), 3: (drawRegularCube, "Dirt", ["dirt"]), 4: (drawRegularCube, "Cobblestone", ["stonebrick"]), 5: (drawDataValues, "Wooden Plank", [(drawRegularCube, "Oak Wood Planks", ["wood"]), (drawRegularCube, "Spruce Wood Planks", ["wood_spruce"]), (drawRegularCube, "Birch Wood Planks", ["wood_birch"]), (drawRegularCube, "Jungle Wood Planks", ["wood_jungle"])]), 6: (drawUnknown, "Sapling", []), 7: (drawRegularCube, "Bedrock", ["bedrock"]), 8: (drawUnknown, "Water", ["water"]), 9: (drawUnknown, "Stationary Water", ["water"]), 10: (drawUnknown, "Lava", ["lava"]), 11: (drawUnknown, "Stationary Lava", ["lava"]), 12: (drawRegularCube, "Sand", ["sand"]), 13: (drawRegularCube, "Gravel", ["gravel"]), 14: (drawRegularCube, "Gold Ore", ["oreGold"]), 15: (drawRegularCube, "Iron Ore", ["ore_iron"]), 16: (drawRegularCube, "Coal Ore", ["oreCoal"]), 17: (drawLogDataValues, "Wood", [(drawLog, "Oak Wood", ["tree_top", "tree_side"]), (drawLog, "Spruce Wood", ["tree_top", "tree_spruce"]), (drawLog, "Birch Wood", ["tree_top", "tree_birch"]), (drawLog, "Jungle Wood", ["tree_top", "tree_jungle"])]), 18: (drawUnknown, "Leaves", []), 19: (drawRegularCube, "Sponge", ["sponge"]), 20: (drawRegularCube, "Glass", ["glass"]), 21: (drawRegularCube, "Lapis Lazuli Ore", ["oreLapis"]), 22: (drawRegularCube, "Lapis Lazuli Block", ["blockLapis"]), 23: (drawUnknown, "Dispenser", []), 24: (drawDataValues, "Sandstone", [(drawMultitextured, "Sandstone(0)", ["sandstone_bottom", "sandstone_top", "sandstone_side", "sandstone_side", "sandstone_side", "sandstone_side"]), (drawMultitextured, "Sandstone(1)", ["sandstone_top", "sandstone_top", "sandstone_carved", "sandstone_carved", "sandstone_carved", "sandstone_carved"]), (drawMultitextured, "Sandstone(2)", ["sandstone_top", "sandstone_top", "sandstone_smooth", "sandstone_smooth", "sandstone_smooth", "sandstone_smooth"])]), 25: (drawRegularCube, "Note Block", ["musicBlock"]), 26: (drawUnknown, "Bed", []), 27: (drawUnknown, "Powered Rail", []), 28: (drawUnknown, "Detector Rail", []), 29: (drawUnknown, "Sticky Piston", []), 30: (drawUnknown, "Cobweb", []), 31: (drawUnknown, "Tall Grass", []), 32: (drawUnknown, "Dead Shrubs", []), 33: (drawUnknown, "Piston", []), 34: (drawUnknown, "Piston Extension", []), 35: (drawCloth, "Wool", []), 36: (drawUnknown, "Piston Moved Block", []), 37: (drawUnknown, "Yellow Flower", []), 38: (drawUnknown, "Red Rose", []), 39: (drawUnknown, "Brown Mushroom", []), 40: (drawUnknown, "Red Mushroom", []), 41: (drawRegularCube, "Gold Block", ["blockGold"]), 42: (drawRegularCube, "Iron Block", ["blockIron"]), 43: (drawDataValues, "Double Slab", [(drawMultitextured, "Double Stone Slab", ["stoneslab_top", "stoneslab_top", "stoneslab_side", "stoneslab_side", "stoneslab_side", "stoneslab_side"]), (drawMultitextured, "Double Sandstone Slab", ["sandstone_bottom", "sandstone_top", "sandstone_side", "sandstone_side", "sandstone_side", "sandstone_side"]), (drawRegularCube, "Double Wooden Slab (Stone)", ["wood"]), (drawRegularCube, "Double Cobblestone Slab", ["stonebrick"]), (drawRegularCube, "Double Brick Slab", ["brick"]), (drawRegularCube, "Double Stone Brick Slab", ["stonebricksmooth"]), (drawRegularCube, "Double Nether Brick Slab", ["netherBrick"]), (drawMultitextured, "Double Quartz Slab", ["quartz_bottom", "quartz_top", "quartz_side", "quartz_side", "quartz_side", "quartz_side"]), (drawRegularCube, "Double Smooth Stone Slab", ["stoneslab_top"]), (drawRegularCube, "Double Smooth Sandstone Slab", ["sandstone_top"])]), 44: (drawSlabDataValues, "Slab", [(drawMultitexturedSlab, "Stone Slab", ["stoneslab_top", "stoneslab_top", "stoneslab_side", "stoneslab_side", "stoneslab_side", "stoneslab_side"]), (drawMultitexturedSlab, "Sandstone Slab", ["sandstone_bottom", "sandstone_top", "sandstone_side", "sandstone_side", "sandstone_side", "sandstone_side"]), (drawSlab, "Wooden Slab (Stone)", ["wood"]), (drawSlab, "Cobblestone Slab", ["stonebrick"]), (drawSlab, "Brick Slab", ["brick"]), (drawSlab, "Stone Brick Slab", ["stonebricksmooth"]), (drawSlab, "Nether Brick Slab", ["netherBrick"]), (drawMultitexturedSlab, "Quartz Slab", ["quartzblock_bottom", "quartzblock_top", "quartzblock_side", "quartzblock_side", "quartzblock_side", "quartzblock_side"])]), 45: (drawRegularCube, "Brick Block", ["brick"]), 46: (drawMultitextured, "TNT", ["tnt_bottom", "tnt_top", "tnt_side", "tnt_side", "tnt_side", "tnt_side"]), 47: (drawMultitextured, "Bookshelf", ["wood", "wood", "bookshelf", "bookshelf", "bookshelf", "bookshelf"]), 48: (drawRegularCube, "Moss Stone", ["stoneMoss"]), 49: (drawRegularCube, "Obsidian", ["obsidian"]), 50: (drawUnknown, "Torch", []), 51: (drawUnknown, "Fire", []), 52: (drawUnknown, "Monster Spawner", []), 53: (drawStairs, "Oak Wood Stairs", ["wood"]), 54: (drawUnknown, "Chest", []), 55: (drawUnknown, "Redstone Wire", []), 56: (drawRegularCube, "Diamond Ore", ["oreDiamond"]), 57: (drawRegularCube, "Diamond Block", ["blockDiamond"]), 58: (drawMultitextured, "Crafting Table", ["wood", "workbench_top", "workbench_front", "workbench_front", "workbench_side", "workbench_side"]), 59: (drawUnknown, "Crops", []), 60: (drawUnknown, "Farmland", []), 61: (drawUnknown, "Furnace", []), 62: (drawUnknown, "Burning Furnace", []), 63: (drawUnknown, "Sign Post", []), 64: (drawUnknown, "Wooden Door", []), 65: (drawUnknown, "Ladder", []), 66: (drawUnknown, "Rails", []), 67: (drawStairs, "Cobblestone Stairs", ["stonebrick"]), 68: (drawUnknown, "Wall Sign", []), 69: (drawUnknown, "Lever", []), 70: (drawUnknown, "Stone Pressure Plate", []), 71: (drawUnknown, "Iron Door", []), 72: (drawUnknown, "Wooden Pressure Plate", []), 73: (drawRegularCube, "Redstone Ore", ["oreRedstone"]), 74: (drawRegularCube, "Glowing Redstone Ore", ["oreRedstone"]), 75: (drawUnknown, "Redstone Torch (OFF)", []), 76: (drawUnknown, "Redstone Torch (ON)", []), 77: (drawUnknown, "Stone Button", []), 78: (drawUnknown, "Snow", []), 79: (drawRegularCube, "Ice", ["ice"]), 80: (drawRegularCube, "Snow Block", ["blockSnow"]), 81: (drawUnknown, "Cactus", []), 82: (drawRegularCube, "Clay Block", ["clay"]), 83: (drawUnknown, "Sugar Cane", []), 84: (drawMultitextured, "Jukebox", ["musicBlock", "jukebox_top", "musicBlock", "musicBlock", "musicBlock", "musicBlock"]), 85: (drawUnknown, "Fence", []), 86: (drawDataValues, "Pumpkin", [(drawMultitextured, "Pumpkin(0)", ["pumpkin_top", "pumpkin_top", "pumpkin_side", "pumpkin_side", "pumpkin_face", "pumpkin_side"]), (drawMultitextured, "Pumpkin(1)", ["pumpkin_top", "pumpkin_top", "pumpkin_side", "pumpkin_face", "pumpkin_side", "pumpkin_side"]), (drawMultitextured, "Pumpkin(2)", ["pumpkin_top", "pumpkin_top", "pumpkin_face", "pumpkin_side", "pumpkin_side", "pumpkin_side"]), (drawMultitextured, "Pumpkin(3)", ["pumpkin_top", "pumpkin_top", "pumpkin_side", "pumpkin_side", "pumpkin_side", "pumpkin_face"]), (drawMultitextured, "Pumpkin(4)", ["pumpkin_top", "pumpkin_top", "pumpkin_side", "pumpkin_side", "pumpkin_side", "pumpkin_side"])]), 87: (drawRegularCube, "Netherrack", ["hellrock"]), 88: (drawRegularCube, "Soul Sand", ["hellsand"]), 89: (drawRegularCube, "Glowstone Block", ["lightgem"]), 90: (drawUnknown, "Portal", []), 91: (drawDataValues, "Jack-O-Lantern", [(drawMultitextured, "Jack-O-Lantern(0)", ["pumpkin_top", "pumpkin_top", "pumpkin_side", "pumpkin_side", "pumpkin_jack", "pumpkin_side"]), (drawMultitextured, "Jack-O-Lantern(1)", ["pumpkin_top", "pumpkin_top", "pumpkin_side", "pumpkin_jack", "pumpkin_side", "pumpkin_side"]), (drawMultitextured, "Jack-O-Lantern(2)", ["pumpkin_top", "pumpkin_top", "pumpkin_jack", "pumpkin_side", "pumpkin_side", "pumpkin_side"]), (drawMultitextured, "Jack-O-Lantern(3)", ["pumpkin_top", "pumpkin_top", "pumpkin_side", "pumpkin_side", "pumpkin_side", "pumpkin_jack"]), (drawMultitextured, "Jack-O-Lantern(4)", ["pumpkin_top", "pumpkin_top", "pumpkin_side", "pumpkin_side", "pumpkin_side", "pumpkin_side"])]), 92: (drawUnknown, "Cake Block", []), 93: (drawUnknown, "Redstone Repeater (OFF)", []), 94: (drawUnknown, "Redstone Repeater (ON)", []), 95: (drawUnknown, "Stained Glass", []), 96: (drawUnknown, "Trapdoor", []), 97: (drawRegularCube, "Silverfish Stone", ["stone"]), 98: (drawRegularCube, "Stone Brick", ["stonebricksmooth"]), 99: (drawRegularCube, "Brown Mushroom Cap", ["mushroom_skin_brown"]), 100: (drawRegularCube, "Red Mushroom Cap", ["mushroom_skin_red"]), 101: (drawUnknown, "Iron Bars", []), 102: (drawUnknown, "Glass Pane", []), 103: (drawUnknown, "Melon", []), 104: (drawUnknown, "Pumpkin Stem", []), 105: (drawUnknown, "Melon Stem", []), 106: (drawUnknown, "Vines", []), 107: (drawUnknown, "Fence Gate", []), 108: (drawStairs, "Brick Stairs", ["brick"]), 109: (drawStairs, "Stone Brick Stairs", ["stonebricksmooth"]), 110: (drawUnknown, "Mycelium", []), 111: (drawUnknown, "Lily Pad", []), 112: (drawRegularCube, "Nether Brick", ["netherBrick"]), 113: (drawUnknown, "Nether Brick Fence", []), 114: (drawStairs, "Nether Brick Stairs", ["netherBrick"]), 115: (drawUnknown, "Nether Wart", []), 116: (drawUnknown, "Enchantment Table", []), 117: (drawUnknown, "Brewing Stand", []), 118: (drawUnknown, "Cauldron", []), 119: (drawUnknown, "End Portal", []), 120: (drawUnknown, "End Portal Frame", []), 121: (drawRegularCube, "End Stone", ["whiteStone.png"]), 122: (drawUnknown, "Dragon Egg", []), 123: (drawRegularCube, "Redstone Lamp (Inactive)", ["redstoneLight"]), 124: (drawRegularCube, "Redstone Lamp (Active)", ["redstoneLight_lit"]), 125: (drawDataValues, "Double Wooden Slab", [(drawRegularCube, "Double Oak Wood Slab", ["wood"]), (drawRegularCube, "Double Spruce Wood Slab", ["wood_spruce"]), (drawRegularCube, "Double Birch Wood Slab", ["wood_birch"]), (drawRegularCube, "Double Jungle Wood Slab", ["wood_jungle"])]), 126: (drawSlabDataValues, "Wooden Slab", [(drawSlab, "Oak Wood Slab", ["wood"]), (drawSlab, "Spruce Wood Slab", ["wood_spruce"]), (drawSlab, "Birch Wood Slab", ["wood_birch"]), (drawSlab, "Jungle Wood Slab", ["wood_jungle"])]), 127: (drawUnknown, "Cocoa Plant", []), 128: (drawMultitexturedStairs, "Sandstone Stairs", ["sandstone_bottom", "sandstone_top", "sandstone_side", "sandstone_side", "sandstone_side", "sandstone_side"]), 129: (drawRegularCube, "Emerald Ore", ["oreEmerald"]), 130: (drawUnknown, "Ender Chest", []), 131: (drawUnknown, "Tripwire Hook", []), 132: (drawUnknown, "Tripwire", []), 133: (drawRegularCube, "Block of Emerald", ["blockEmerald"]), 134: (drawStairs, "Spruce Wood Stairs", ["wood_spruce"]), 135: (drawStairs, "Birch Wood Stairs", ["wood_birch"]), 136: (drawStairs, "Jungle Wood Stairs", ["wood_jungle"]), 137: (drawRegularCube, "Command Block", ["commandBlock"]), 138: (drawUnknown, "Beacon", []), 139: (drawUnknown, "Cobblestone Wall", []), 140: (drawUnknown, "Flower Pot", []), 141: (drawUnknown, "Carrots", []), 142: (drawUnknown, "Potatoes", []), 143: (drawUnknown, "Wooden Button", []), 144: (drawUnknown, "Mob Head", []), 145: (drawUnknown, "Anvil", []), 146: (drawUnknown, "Trapped Chest", []), 147: (drawUnknown, "Weighted Pressure Plate", []), 148: (drawUnknown, "Weighted Pressure Plate", []), 149: (drawUnknown, "Redstone Comparator", []), 150: (drawUnknown, "Redstone Comparator (Active)", []), 151: (drawUnknown, "Daylight Sensor", []), 152: (drawRegularCube, "Block of Redstone", ["blockRedstone"]), 153: (drawRegularCube, "Nether Quartz Ore", ["netherquartz"]), 154: (drawUnknown, "Hopper", []), 155: (drawUnknown, "Block of Quartz", []), 156: (drawMultitexturedStairs, "Quartz Stairs", ["quartzblock_bottom", "quartzblock_top", "quartzblock_side", "quartzblock_side", "quartzblock_side", "quartzblock_side"]), 157: (drawUnknown, "Activator Rail", []), 158: (drawUnknown, "Dropper", []), 159: (drawUnknown, "Stained Clay", []), 160: (drawUnknown, "Stained Glass Pane", [])}
