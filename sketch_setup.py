import bpy

from bpy.types import Operator, Panel

bl_info = {
         "name" : "Sketch",
         "author" : "Andrew Merizalde <andrewmerizalde@hotmail.com>",
         "version" : (1, 0, 0),
         "blender" : (2, 7, 8),
         "location" : "View 3D > Object Mode > Tool Shelf > Sketch",
         "description" :
             "Jump straight into a 2D texture workflow from any state.",
         "warning" : "",
         "wiki_url" : "https://github.com/amerizalde/sketch",
         "tracker_url" : "",
         "category" : "Paint"}

         
class SketchOperator(Operator):

    bl_idname = "alm.sketch"
    bl_label = "Create Blank Image"
    
    def execute(self, context):

        if 'sketch_object' in bpy.data.objects.keys():
            context.scene.objects.active = bpy.data.objects["sketch_object"]
        else:
            bpy.ops.mesh.primitive_vert_add()
            bpy.ops.object.mode_set(mode = 'OBJECT')
            context.object.name = "sketch_object"
            
        bpy.ops.object.mode_set(mode = 'TEXTURE_PAINT')

        # if there is no material, add one.
        if not isinstance(context.active_object.active_material, bpy.types.Material):
            mat_name = "SketchMat"
            mat = bpy.data.materials.new(mat_name)
            mat.use_nodes = True
            
            context.active_object.data.materials.append(mat)

            # clear all nodes to start clean
            nodes = mat.node_tree.nodes
            for node in nodes:
                nodes.remove(node)

            # create emission node
            node_emission = nodes.new(type='ShaderNodeEmission')
            node_emission.inputs[0].default_value = (1,1,1,1)
            node_emission.inputs[1].default_value = 1.0
            node_emission.location = 0,0

            # create output node
            node_output = nodes.new(type='ShaderNodeOutputMaterial')   
            node_output.location = 400,0
            
            # link nodes
            links = mat.node_tree.links
            link = links.new(node_emission.outputs[0], node_output.inputs[0])
                        
            context.active_object.active_material = mat

        # requires "Additional Texture Slots" to be installed
        bpy.ops.alm.paint_slots()
        
        context.area.type = "IMAGE_EDITOR"
        context.space_data.mode = "PAINT"
        context.object.active_material.paint_active_slot = 1 - len(context.object.active_material.texture_paint_slots)

        
        self.report({"INFO"}, "New Image Generated.")
        
        
        return {'FINISHED'}


class SketchButtonPanel(Panel):

    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_label = "Start Sketching"
    bl_category = "Tools"
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("alm.sketch", text="Add Image", icon="FACESEL_HLT")


def register():
    bpy.utils.register_class(SketchOperator)
    bpy.utils.register_class(SketchButtonPanel)
    
def unregister():
    bpy.utils.unregister_class(SketchOperator)
    bpy.utils.unregister_class(SketchButtonPanel)
        
if __name__ == "__main__":
    register()
