import os
import shutil

def get_subfolder_list(folder_path):
    try:
        subfolders = [name for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))]
        return set(subfolders)
    except Exception as e:
        print(f"Error reading subfolders in {folder_path}: {e}")
        return set()

def delete_non_common_subfolders(folder_path, common_subfolders):
    try:
        current_subfolders = get_subfolder_list(folder_path)
        for subfolder in current_subfolders:
            if subfolder not in common_subfolders:
                subfolder_path = os.path.join(folder_path, subfolder)
                try:
                    shutil.rmtree(subfolder_path)
                    print(f"Deleted: {subfolder_path}")
                except Exception as e:
                    print(f"Error deleting {subfolder_path}: {e}")
    except Exception as e:
        print(f"Error processing folder {folder_path}: {e}")

# Paths to the two folders
folder1_path = '/data04/user-storage/y.zezhang/dl_denoising/db_pipeline/sim_4_11_mirirv1_test/data/def_segments'
folder2_path = '/data01/user-storage/y.zezhang/2024_subsample_project/mod_subsample_projection/30/hl_asq'

# Get the subfolder lists
subfolders1 = get_subfolder_list(folder1_path)
subfolders2 = get_subfolder_list(folder2_path)

# Find common subfolders
common_subfolders = subfolders1.intersection(subfolders2)

# Delete non-common subfolders in the second folder
delete_non_common_subfolders(folder2_path, common_subfolders)