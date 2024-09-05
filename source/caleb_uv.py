bl_info = {
    "name": "CalebUV",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy

# Define the operator that scales selected objects
class OBJECT_OT_CalebUV(bpy.types.Operator):
    """Scale selected objects by 2"""
    bl_idname = "object.caleb_uv_operator"
    bl_label = "CalebUV"

    def execute(self, context):
        # Scale each selected object by 2
        for obj in bpy.context.selected_objects:
            obj.scale = [s * 2 for s in obj.scale]
        return {'FINISHED'}

# Define the panel that will have the button
class OBJECT_PT_CalebUVPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "CalebUV"
    bl_idname = "OBJECT_PT_caleb_uv"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'CalebUV'

    def draw(self, context):
        layout = self.layout
        # Create a button and link it to the operator
        layout.operator("object.caleb_uv_operator")

# Register and unregister the classes
def register():
    bpy.utils.register_class(OBJECT_OT_CalebUV)
    bpy.utils.register_class(OBJECT_PT_CalebUVPanel)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_CalebUV)
    bpy.utils.unregister_class(OBJECT_PT_CalebUVPanel)

if __name__ == "__main__":
    register()
