import os
import shutil

def merge_folders(source_folder_1, source_folder_2, target_folder):
    # Create the target folder if it doesn't exist
    os.makedirs(target_folder, exist_ok=True)

    # Merge the first source folder into the target folder
    for item in os.listdir(source_folder_1):
        source_path = os.path.join(source_folder_1, item)
        target_path = os.path.join(target_folder, item)
        
        # If the item is a directory, use shutil.copytree; if a file, use shutil.copy2
        if os.path.isdir(source_path):
            shutil.copytree(source_path, target_path, dirs_exist_ok=True)  # Python 3.8+
        else:
            shutil.copy2(source_path, target_path)  # Copy file with metadata

    # Merge the second source folder into the target folder
    for item in os.listdir(source_folder_2):
        source_path = os.path.join(source_folder_2, item)
        target_path = os.path.join(target_folder, item)
        
        # If the item is a directory, use shutil.copytree; if a file, use shutil.copy2
        if os.path.isdir(source_path):
            shutil.copytree(source_path, target_path, dirs_exist_ok=True)  # Python 3.8+
        else:
            shutil.copy2(source_path, target_path)  # Copy file with metadata

    print(f"Merged '{source_folder_1}' and '{source_folder_2}' into '{target_folder}'.")

#sparse_level=['centroid_mask','5','10','15','30']
sparse_level=['30']
main_folder_base='/data01/user-storage/y.zezhang/2024_subsample_project/mod_Neural_network_training'
# Define your source and target folder paths
for sl in sparse_level:
    
    #source_folder_1 = f'{main_folder_base}/{sl}/testing'  # Replace with the path to your first folder
    source_folder_1 = f'{main_folder_base}/{sl}/testing_total'  # Replace with the path to your first folder
    source_folder_2 = f'{main_folder_base}/{sl}/training'  # Replace with the path to your second folder
    target_folder = f'{main_folder_base}/{sl}/ge_total'    # Replace with the path to your target folder

    # Call the function to merge folders
    merge_folders(source_folder_1, source_folder_2, target_folder)