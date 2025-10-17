import os
import shutil
from math import floor
from random import shuffle

def copy_and_merge_folders(src_dir, dest_dir, folder_names):
    # Ensure destination directory exists
    os.makedirs(dest_dir, exist_ok=True)
    
    for folder_name in folder_names:
        src_folder_path = os.path.join(src_dir, folder_name)
        dest_folder_path = os.path.join(dest_dir, folder_name)
        
        if os.path.exists(src_folder_path) and os.path.isdir(src_folder_path):
            for root, dirs, files in os.walk(src_folder_path):
                # Construct the destination path
                dest_path = os.path.join(dest_folder_path, os.path.relpath(root, src_folder_path))
                
                # Ensure the destination path exists
                os.makedirs(dest_path, exist_ok=True)
                
                # Copy files
                for file in files:
                    src_file_path = os.path.join(root, file)
                    dest_file_path = os.path.join(dest_path, file)
                    shutil.copy2(src_file_path, dest_file_path)
                    
            print(f'Merged {src_folder_path} into {dest_folder_path}')
        else:
            print(f'Source folder {src_folder_path} does not exist or is not a directory')


slice_number=5

testing30full='/data01/user-storage/y.zezhang/2024_subsample_project/mod_Neural_network_training/30/testing'
training30full='/data01/user-storage/y.zezhang/2024_subsample_project/mod_Neural_network_training/30/training'


testing_patient = os.listdir(testing30full)
training_patient = os.listdir(training30full)


copy_directory_base_diseased='/data01/user-storage/y.zezhang/2024_subsample_project/mod_SA_images/'+str(slice_number)+'/diseased'
copy_directory_base_healthy='/data01/user-storage/y.zezhang/2024_subsample_project/mod_SA_images/'+str(slice_number)+'/healthy'
testing_destination_directory_base = '/data01/user-storage/y.zezhang/2024_subsample_project/mod_Neural_network_training/'+str(slice_number) +'/testing'
training_destination_directory_base = '/data01/user-storage/y.zezhang/2024_subsample_project/mod_Neural_network_training/'+str(slice_number) +'/training'


    
copy_and_merge_folders(copy_directory_base_diseased, testing_destination_directory_base, testing_patient)
copy_and_merge_folders(copy_directory_base_healthy, testing_destination_directory_base, testing_patient)
copy_and_merge_folders(copy_directory_base_healthy, training_destination_directory_base, training_patient)
copy_and_merge_folders(copy_directory_base_diseased, training_destination_directory_base, training_patient)