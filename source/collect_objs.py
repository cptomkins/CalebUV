import bpy
import os

# Define the directories
original_assets_dir = 'assets/original/'
good_uv_export_dir = 'assets/goodUV/'
bad_uv_export_dir = 'assets/badUV/'

# Ensure the export directories exist
os.makedirs(good_uv_export_dir, exist_ok=True)
os.makedirs(bad_uv_export_dir, exist_ok=True)

# Function to clear all objects from the scene
def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

# Function to import a model (OBJ/FBX/etc.)
def import_model(file_path):
    if file_path.lower().endswith('.obj'):
        bpy.ops.import_scene.obj(filepath=file_path)
    elif file_path.lower().endswith('.fbx'):
        bpy.ops.import_scene.fbx(filepath=file_path)
    # Add more import options if needed for different formats

# Function to export the model as OBJ
def export_model_as_obj(export_path):
    bpy.ops.export_scene.obj(filepath=export_path, use_selection=False, use_materials=False)

# Function to apply auto UV unwrapping to all meshes in the scene
def apply_auto_uv():
    for obj in bpy.context.selected_objects:
        if obj.type == 'MESH':
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.uv.smart_project(angle_limit=66, island_margin=0.02)
            bpy.ops.object.mode_set(mode='OBJECT')

# Iterate through assets in the original assets directory
for asset_file in os.listdir(original_assets_dir):
    if not asset_file.lower().endswith(('.obj', '.fbx')):  # Check only for OBJ or FBX files
        continue

    asset_path = os.path.join(original_assets_dir, asset_file)
    base_name = os.path.splitext(asset_file)[0]
    good_uv_export_path = os.path.join(good_uv_export_dir, base_name + '_goodUV.obj')
    bad_uv_export_path = os.path.join(bad_uv_export_dir, base_name + '_badUV.obj')

    # Skip processing if both exported files already exist
    if os.path.exists(good_uv_export_path) and os.path.exists(bad_uv_export_path):
        print(f"Skipping asset (already processed): {asset_path}")
        continue

    print(f"Processing asset: {asset_path}")

    # Clear the current scene
    clear_scene()

    # Import the original asset
    import_model(asset_path)

    # Export the original asset to the good UVs directory if not already exported
    if not os.path.exists(good_uv_export_path):
        export_model_as_obj(good_uv_export_path)
        print(f"Exported original asset with good UVs to: {good_uv_export_path}")

    # Apply automatic UV unwrapping
    apply_auto_uv()

    # Export the modified asset with new UVs to the bad UVs directory if not already exported
    if not os.path.exists(bad_uv_export_path):
        export_model_as_obj(bad_uv_export_path)
        print(f"Exported asset with auto-generated UVs to: {bad_uv_export_path}")

print("Processing completed!")
