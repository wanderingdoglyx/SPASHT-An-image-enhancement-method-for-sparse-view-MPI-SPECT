import numpy as np
import os


# Define the paths
input_filename = 'reoriented_windowed.img'
root_dir = '/data01/user-storage/y.zezhang/2024_subsample_project/mod_SA_images'  # Specify the root directory to search in

# Search for all instances of the file in folder and subfolder
def find_files(root_dir, filename):
    file_paths = []
    for dirpath, _, filenames in os.walk(root_dir):
        if filename in filenames:
            file_paths.append(os.path.join(dirpath, filename))
    return file_paths

# Find all file paths
file_paths = find_files(root_dir, input_filename)

if file_paths:
    for file_path in file_paths:
        print(f"Processing file: {file_path}")
        
        # Read the binary data
        original_shape = (32, 48, 48)
        data = np.fromfile(file_path, dtype=np.float32).reshape(original_shape)

        # Create a new array with the desired shape, filled with zeros
        new_shape = (48, 48, 48)
        new_data = np.zeros(new_shape, dtype=np.float32)

        # Calculate the start and end indices for the original data
        start_idx = (new_shape[0] - original_shape[0]) // 2
        end_idx = start_idx + original_shape[0]

        # Copy the original data into the new array
        new_data[start_idx:end_idx, :, :] = data

        # Save the new data back to a binary file with a new name in the same directory
        output_filename = os.path.join(os.path.dirname(file_path), 'extended_reoriented_windowed.img')
        new_data.tofile(output_filename)
        
        print(f"New file saved as: {output_filename}")
else:
    print("No files found")