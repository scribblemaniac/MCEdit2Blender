# MCEdit2Blender
A Blender addon to quickly import Minecraft worlds using MCEdit .schematic files.

## Information
 Here are a few things we do (or plan to do) that help distinguish us from other similar projects:
- No additional setup is required after importing a schematic to achieve the look and feel of Minecraft
- We are designed with animators in mind. Individual objects for each block, animated particle systems, and custom configuration for blocks like pistons and doors all to make it easier to animate.
- We do not rely on [Mineways](http://www.realtimerendering.com/erich/minecraft/public/mineways/) or [jMc2Obj](https://github.com/jmc2obj/j-mc-2-obj) to generate objects but instead do it ourselves which gives us greater control over the entire process.
- MCEdit schematic files are used instead of direct importing from a minecraft world. This is one of the most popular and well supported formats for saving parts of a map and have the advantage of being able to use various different tools to generate them. WorldEdit and MCEdit are both easy tools that can be used to select 3d regions to render.
- It is relatively simple for mods to extend our plugin to add support for their own blocks.
- Easily swap texture packs within Blender.

This project is still in very early beta. We currently only have support for about 40% of all of the vanilla minecraft blocks and we are still missing some very important features. We will not be providing instructions for installation and usage until the project has been developed a little bit more. The source code is all here however so if you want to try it out you still theoretically could. The [NBT](https://github.com/twoolie/NBT) library by twoolie and the block textures from minecraft are currently the only two dependencies.

## Contributing
We welcome contributions, however since this project is so new we are still getting things set up. We ask that you wait a little bit or contact @scribblemaniac before attempted to do anything. There are currently plans for some major changes to the code and we just don't want you do have to more work that you need to. Keep checking back here for updates!
