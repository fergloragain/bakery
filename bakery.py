bl_info = {
  "name" : "Bakes AO for all objects",
  "description" : "Bakes AO for all objects",
  "author" : "Ferglor",
  "version" : (1,0),
  "blender" : (2,7,1),
  "location" : "View3D > Object > AO Baker",
  "warning" : "",
  "wiki_url" : "",
  "tracker_url" : "",
  "category" : "Object" } 

import bpy  
from bpy.types import Operator
from bpy.props import FloatVectorProperty, FloatProperty, IntProperty
  
class MoveOperator(Operator):  
  """AO Baker"""
  bl_idname = "object.move_operator"  
  bl_label = "AO Baker"  
  bl_options = {'REGISTER', 'UNDO'}
  
  def execute(self, context):  
    for o in bpy.data.objects:
      bpy.ops.object.select_all(action='DESELECT')
      bpy.context.scene.objects.active = o
      o.select=True
      print ("#########################################")
      print(context.active_object.name)
      print (o.name)
      if (o.type != 'MESH'):
        continue

      # an object's mesh is its data property
      m = o.data

      print (m.name)

      # create a new uv map
      oldLayers = m.uv_layers
      oldLayers = oldLayers[:]
      print(oldLayers)
      bpy.ops.mesh.uv_texture_add()
      newLayers = m.uv_layers
      print(newLayers)

      oldNames = []
      newNames = []

      for l in newLayers:
        print("new {}".format(l.name))
        newNames.append(l.name)

      for l in oldLayers:
        print("old {}".format(l.name))
        oldNames.append(l.name)

      texName = "empty"

      print("newNames: {}".format(newNames))
      print("oldNames: {}".format(oldNames))

      #for l in oldNames:
        #print (l)
      for l in newNames:
        print (l)
        if l not in oldNames:
          print ("created new uv layer: {}".format(l))
          texName = l

      # get the last uv map assigned to the cube
      #numTex = len(m.uv_textures)
      #numTex = int(numTex)
      #print("numTex: {}".format(numTex))
      #texIndex = numTex -1
      #texIndex = int(texIndex)
      #print("texIndex: {}".format(texIndex))

      #if (texIndex < 0):
        #  texIndex = 0

      # rename the latest uv map to whatever we want
      m.uv_layers[texName].name = "bakery ao " + m.name + "UVMap"
      texName = "bakery ao " + m.name + "UVMap"

      #print ("renamed new uv layer to: "+"bakery ao " + m.name)
      # we need to read this name back, as blender might have appended .001
      #texName = m.uv_textures[texIndex].name
      print ("final uv layer name: " + texName)

      bpy.data.worlds['World'].light_settings.use_ambient_occlusion = True
      print ("using ao")

      bpy.ops.object.editmode_toggle()
      print ("in edit mode")

      bpy.ops.mesh.select_all(action='SELECT')
      print ("select all")
      bpy.ops.uv.smart_project()
      print ("smart project")
      orig = bpy.context.area.type

      # create a new uv image 
      bpy.context.area.type = 'IMAGE_EDITOR'
      bpy.ops.image.new(name=texName, width=1024, height=1024)
      print ("created new image called : " + texName)
      image = bpy.data.images[texName]
      bpy.ops.image.save_as(filepath="/tmp/"+texName)
      bpy.ops.image.open(filepath="/tmp/"+texName)

      bpy.data.screens['UV Editing'].areas[1].spaces[0].image = image

      bpy.data.scenes['Scene'].render.bake_type='AO'
      print ("activate ao")

      bpy.ops.object.bake_image()
      print ("baked")

      bpy.context.area.type = orig
      bpy.ops.object.editmode_toggle()
      print ("exited edit mode")

    return {'FINISHED'}  

def add_object_button(self, context):
  self.layout.operator(
    MoveOperator.bl_idname,
    text=MoveOperator.__doc__,
    icon='PLUGIN')

def register():  
  bpy.utils.register_class(MoveOperator)
  bpy.types.VIEW3D_MT_object.append(add_object_button)

if __name__ == "__main__":
  register()
