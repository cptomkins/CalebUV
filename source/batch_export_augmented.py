import bpy
import os
import random
import re

original_folder = 'assets/original'
augmented_folder = 'assets/augmented'

DEFAULT_TRANSFORMS = {
    "translation": (0, 0, 0),
    "rotation": (0, 0, 0),
    "scale": (1, 1, 1)
}

def generate_random_transform():
    translation = (
        random.uniform(-10, 10),
        random.uniform(-10, 10),
        random.uniform(-10, 10)
    )
    rotation = (
        random.uniform(0, 3.14159),
        random.uniform(0, 3.14159), 
        random.uniform(0, 3.14159)  
    )
    scale_value = random.uniform(0.5, 10)
    scale = (scale_value, scale_value, scale_value)
    
    return translation, rotation, scale

def apply_transform_to_all_objects(objects, translation, rotation, scale):
    for obj in objects:
        obj.location.x += translation[0]
        obj.location.y += translation[1]
        obj.location.z += translation[2]
        
        obj.rotation_euler[0] = rotation[0]
        obj.rotation_euler[1] = rotation[1]
        obj.rotation_euler[2] = rotation[2]
        
        obj.scale = scale
        print(obj.scale)

def process_file(filename, augment_count=3):
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    original_filepath = os.path.join(original_folder, filename)
    base_name = os.path.splitext(filename)[0]
    
    pattern = re.compile(rf"^{re.escape(base_name)}_\d{{2}}\.obj$")
    existing_versions = [f for f in os.listdir(augmented_folder) if pattern.match(f)]
    start_count = len(existing_versions)
    augment_count = augment_count - start_count

    if augment_count <= 0:
        print(f"Skipping {filename}, already augmented.")
        return
    elif existing_versions:
        print(f"Only augmenting {filename} {augment_count}x. Some files already exist.")
    
    if filename.endswith('.fbx'):
        bpy.ops.import_scene.fbx(filepath=original_filepath)
    elif filename.endswith('.obj'):
        bpy.ops.wm.obj_import(filepath=original_filepath)
    
    imported_objects = bpy.context.selected_objects
    for i in range(1 + start_count, augment_count + start_count + 1):
        bpy.ops.object.select_all(action='DESELECT')
        apply_transform_to_all_objects(imported_objects, DEFAULT_TRANSFORMS["translation"], DEFAULT_TRANSFORMS["rotation"], DEFAULT_TRANSFORMS["scale"])

        translation, rotation, scale = generate_random_transform()
        apply_transform_to_all_objects(imported_objects, translation, rotation, scale)

        augmented_filename = f"{base_name}_{i:02d}.obj"
        augmented_filepath = os.path.join(augmented_folder, augmented_filename)
        bpy.ops.wm.obj_export(filepath=augmented_filepath, export_selected_objects=False, export_materials=False)  # Export all objects
        
    bpy.ops.object.select_all(action='DESELECT')
    for obj in imported_objects:
        obj.select_set(True)
    bpy.ops.object.delete()

    print(f"Augmented versions of {filename} exported.")

def main():

    if not os.path.exists(augmented_folder):
        os.makedirs(augmented_folder)

    for filename in os.listdir(original_folder):
        if filename.endswith('.fbx') or filename.endswith('.obj'):
            process_file(filename)

    print("Processing complete.")

if __name__ == "__main__":
    main()
