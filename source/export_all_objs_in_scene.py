import bpy
import os

# Define the prefix and output directory
prefix = "object"
output_directory = "C:\\Packages\\CalebUV\\assets\\temp"

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Loop through all objects in the scene
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':  # Only export mesh objects
        # Select the object
        bpy.ops.object.select_all(action='DESELECT')  # Deselect all objects
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj

        # Construct the filename
        file_path = os.path.join(output_directory, f"{prefix}_{obj.name}.obj")

        # Export the selected object as an OBJ file
        bpy.ops.export_scene.obj(
            filepath=file_path,
            use_selection=True,
            use_materials=False  # Do not write materials
        )

        print(f"Exported {obj.name} to {file_path}")

print("Export completed.")
