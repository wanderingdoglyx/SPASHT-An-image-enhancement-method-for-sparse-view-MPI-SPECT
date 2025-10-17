import os
import shutil

def copy_reconprim_folders(source_dir, dest_dir):
    # Ensure destination directory exists
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Walk through the source directory and its subdirectories
    for root, dirs, files in os.walk(source_dir):
        for dir_name in dirs:
            if 'ReconPrim' in dir_name:
                source_path = os.path.join(root, dir_name)
                dest_path = os.path.join(dest_dir, dir_name)
                
                # If destination folder exists, remove it
                if os.path.exists(dest_path):
                    shutil.rmtree(dest_path)
                
                # Copy the directory to the destination
                shutil.copytree(source_path, dest_path)
                print(f"Copied {source_path} to {dest_path}")


# Example usage
source_directory = '/data01/user-storage/asheq/projects/dl_denoising/MIM_data_mar31/MIRIR_data_June13_mim_7'
destination_directory = '/data01/user-storage/y.zezhang/data_from_zitong_real_patient_project/sa_v3_copy/dependencies/reco_prim'

copy_reconprim_folders(source_directory, destination_directory)