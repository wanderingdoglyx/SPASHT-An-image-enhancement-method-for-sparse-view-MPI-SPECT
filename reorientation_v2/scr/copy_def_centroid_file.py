import os
import shutil

def copy_def_centroid_files(source_dir, dest_dir):
    # Walk through the source directory and its subdirectories
    for root, dirs, files in os.walk(source_dir):
        for file_name in files:
            if 'def_centroid' in file_name:
                source_file_path = os.path.join(root, file_name)
                
                # Create the relative path in the destination directory
                relative_path = os.path.relpath(root, source_dir)
                dest_subdir_path = os.path.join(dest_dir, relative_path)
                
                # Ensure the destination subdirectory exists
                if not os.path.exists(dest_subdir_path):
                    os.makedirs(dest_subdir_path)
                
                dest_file_path = os.path.join(dest_subdir_path, file_name)
                
                # Copy the file to the destination
                shutil.copy2(source_file_path, dest_file_path)
                print(f"Copied {source_file_path} to {dest_file_path}")

# Example usage
source_directory = '/data01/user-storage/y.zezhang/data_for_zezhang_mar29/training_data_sa_wd'
destination_directory = '/data01/user-storage/y.zezhang/data_from_zitong_real_patient_project/sa_v3/dependencies/def_center'

copy_def_centroid_files(source_directory, destination_directory)