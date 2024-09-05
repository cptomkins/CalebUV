import os
import json

# Define the directories
good_uv_dir = 'assets/goodUV/'
bad_uv_dir = 'assets/badUV/'
output_json_path = 'assets/uv_data.json'

# Function to parse OBJ file and extract data
def parse_obj(file_path):
    vertices = []  # Vertex positions (v)
    uvs = []       # UV coordinates (vt)
    normals = []   # Normals (vn)
    faces = []     # Faces (f)

    with open(file_path, 'r') as obj_file:
        for line in obj_file:
            parts = line.strip().split()
            if len(parts) == 0:
                continue
            prefix = parts[0]

            if prefix == 'v':  # Vertex positions
                vertices.append([float(parts[1]), float(parts[2]), float(parts[3])])
            elif prefix == 'vt':  # UV coordinates
                uvs.append([float(parts[1]), float(parts[2])])
            elif prefix == 'vn':  # Normal vectors
                normals.append([float(parts[1]), float(parts[2]), float(parts[3])])
            elif prefix == 'f':  # Faces
                # Faces can refer to vertices, UVs, and normals
                # Parse face definitions like "f 1/1/1 2/2/2 3/3/3"
                face = []
                for part in parts[1:]:
                    indices = part.split('/')
                    vertex_index = int(indices[0]) if indices[0] else None
                    uv_index = int(indices[1]) if len(indices) > 1 and indices[1] else None
                    normal_index = int(indices[2]) if len(indices) > 2 and indices[2] else None
                    face.append({
                        'vertex_index': vertex_index,
                        'uv_index': uv_index,
                        'normal_index': normal_index
                    })
                faces.append(face)

    return {
        'vertices': vertices,
        'uvs': uvs,
        'normals': normals,
        'faces': faces
    }

# Function to collect data and save to JSON
def collect_data_to_json():
    uv_data = []

    # Iterate over "good" UV files
    for good_uv_file in os.listdir(good_uv_dir):
        if not good_uv_file.endswith('.obj'):
            continue

        # Find corresponding "bad" UV file
        base_name = os.path.splitext(good_uv_file)[0].replace('_goodUV', '')
        bad_uv_file = f"{base_name}_badUV.obj"

        good_uv_path = os.path.join(good_uv_dir, good_uv_file)
        bad_uv_path = os.path.join(bad_uv_dir, bad_uv_file)

        if os.path.exists(good_uv_path) and os.path.exists(bad_uv_path):
            print(f"Processing pair: {good_uv_file} and {bad_uv_file}")

            # Extract data from both files
            good_data = parse_obj(good_uv_path)
            bad_data = parse_obj(bad_uv_path)

            # Ensure the same vertex count and face count; otherwise, there's a mismatch
            if len(good_data['vertices']) != len(bad_data['vertices']) or len(good_data['faces']) != len(bad_data['faces']):
                print(f"Warning: Mismatch in data for {good_uv_file} and {bad_uv_file}")
                continue

            # Store data
            uv_data.append({
                'model': base_name,
                'good_data': good_data,
                'bad_data': bad_data
            })

    # Write to JSON file
    with open(output_json_path, 'w') as json_file:
        json.dump(uv_data, json_file, indent=4)
    print(f"UV data saved to {output_json_path}")

# Run the function to collect and save data
collect_data_to_json()
