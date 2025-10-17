import os
import shutil
import random

def get_subfolder_names(folder_paths):
    """
    Given a list of folder paths, return a dictionary where the keys are the
    folder paths and the values are lists of subfolder names within those folders.

    Parameters:
    folder_paths (list of str): List of paths to the folders.

    Returns:
    dict: Dictionary with folder paths as keys and lists of subfolder names as values.
    """
    subfolders = {}

    for folder_path in folder_paths:
        try:
            # Get the list of subfolders
            subfolders[folder_path] = [name for name in os.listdir(folder_path)
                                       if os.path.isdir(os.path.join(folder_path, name))]
        except FileNotFoundError:
            print(f"Folder not found: {folder_path}")
        except PermissionError:
            print(f"Permission denied: {folder_path}")
        except Exception as e:
            print(f"An error occurred with folder {folder_path}: {e}")

    return subfolders

def copy_subfolders(source_folders, subfolder_list, destination, exclude_set):
    """
    Copy subfolders from a list to the destination folder, avoiding duplicates with exclude_set.

    Parameters:
    source_folders (list of str): List of source folder paths.
    subfolder_list (list of str): List of subfolder names to copy.
    destination (str): Path to the destination folder.
    exclude_set (set): Set of subfolder names to avoid duplicating.
    """
    copied_subfolders = set()

    for subfolder in subfolder_list:
        if subfolder not in exclude_set:
            copied = False
            for source_folder in source_folders:
                src_path = os.path.join(source_folder, subfolder)
                if os.path.exists(src_path):
                    try:
                        dest_path = os.path.join(destination, subfolder)
                        shutil.copytree(src_path, dest_path)
                        copied_subfolders.add(subfolder)
                        copied = True
                        break
                    except Exception as e:
                        print(f"Failed to copy {subfolder} from {src_path} to {destination}: {e}")
            if not copied:
                print(f"Subfolder {subfolder} not found in any source folder.")
                
    return copied_subfolders

# Define folder paths
def_folders = [
    '/data01/user-storage/y.zezhang/2024_subsample_project/mod_subsample_projection/30/training_de_def',
    '/data01/user-storage/y.zezhang/2024_subsample_project/mod_subsample_projection/30/def',
    '/data01/user-storage/y.zezhang/2024_subsample_project/mod_subsample_projection/30/def_asq'
]

hl_folders = [
    '/data01/user-storage/y.zezhang/2024_subsample_project/mod_subsample_projection/30/training_de_def',
    '/data01/user-storage/y.zezhang/2024_subsample_project/mod_subsample_projection/30/def',
    '/data01/user-storage/y.zezhang/2024_subsample_project/mod_subsample_projection/30/hl_asq'
]

# Define source main folder
#source_main_folder = '/data01/user-storage/y.zezhang/2024_subsample_project/mod_Neural_network_training/30'


# Define source folders
source_folders = [
    '/data01/user-storage/y.zezhang/data_for_zezhang_mar29/test_data_mirirv3_sa_wd_48cube',
    '/data01/user-storage/y.zezhang/data_for_zezhang_mar29/test_data_sa_wd_fix2_48cube',
    '/data01/user-storage/y.zezhang/data_for_zezhang_mar29/training_data_sa_wd_fix2_48cube'
]

# Define destination paths
def_destination = '/data01/user-storage/y.zezhang/2024_subsample_project/mod_Neural_network_training/30/testing'
hl_destination = '/data01/user-storage/y.zezhang/2024_subsample_project/mod_Neural_network_training/30/training'

# Create destination directories if they do not exist
os.makedirs(def_destination, exist_ok=True)
os.makedirs(hl_destination, exist_ok=True)

# Get subfolder names
group1_subfolders = get_subfolder_names(def_folders)
group2_subfolders = get_subfolder_names(hl_folders)

# Flatten the lists of subfolders
all_group1_subfolders = [subfolder for sublist in group1_subfolders.values() for subfolder in sublist]
all_group2_subfolders = [subfolder for sublist in group2_subfolders.values() for subfolder in sublist]

# Copy part of subfolders from group1 to destination1
random.shuffle(all_group1_subfolders)
num_to_copy = len(all_group1_subfolders) // 2  # Define how many to copy to destination1
group1_dest1_subfolders = all_group1_subfolders[:num_to_copy]

copied_subfolders_dest1 = copy_subfolders(source_folders, group1_dest1_subfolders, def_destination, set())

# Copy all remaining subfolders from group2 to destination2
remaining_group2_subfolders = [subfolder for subfolder in all_group2_subfolders if subfolder not in copied_subfolders_dest1]
copied_subfolders_dest2 = copy_subfolders(source_folders, remaining_group2_subfolders, hl_destination, copied_subfolders_dest1)

print(f"Subfolders copied to '{def_destination}': {copied_subfolders_dest1}")
print(f"Subfolders copied to '{hl_destination}': {copied_subfolders_dest2}")
