import os
import shutil

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

def copy_subfolders(source_folder, subfolder_list, destination):
    """
    Copy subfolders from a list to the destination folder.

    Parameters:
    source_folder (str): Path to the source folder.
    subfolder_list (list of str): List of subfolder names to copy.
    destination (str): Path to the destination folder.
    """
    copied_subfolders = set()

    for subfolder in subfolder_list:
        src_path = os.path.join(source_folder, subfolder)
        dest_path = os.path.join(destination, subfolder)
        if os.path.exists(src_path):
            try:
                shutil.copytree(src_path, dest_path)
                copied_subfolders.add(subfolder)
            except Exception as e:
                print(f"Failed to copy {subfolder} from {src_path} to {destination}: {e}")
        else:
            print(f"Source subfolder does not exist: {src_path}")
                
    return copied_subfolders

# Define folder paths
group1_folders = [  
    '/data01/user-storage/y.zezhang/2024_subsample_project/mod_subsample_projection/30/training_de_def'
]

group2_folders = [
    
    '/data01/user-storage/y.zezhang/2024_subsample_project/mod_subsample_projection/30/def'
]

group3_folders = [  
    '/data01/user-storage/y.zezhang/2024_subsample_project/mod_subsample_projection/30/hl_asq'
]

group4_folders = [
    
    '/data01/user-storage/y.zezhang/2024_subsample_project/mod_subsample_projection/30/def_asq'
]
# Define source folders
source_folder1 = '/data01/user-storage/y.zezhang/data_for_zezhang_mar29/training_data_sa_wd_fix2_48cube'
source_folder2 = '/data01/user-storage/y.zezhang/data_for_zezhang_mar29/test_data_mirirv3_sa_wd_48cube'
source_folder3 = '/data01/user-storage/y.zezhang/data_for_zezhang_mar29/test_data_sa_wd_fix2_48cube'
#source_folder2 = '/data01/user-storage/y.zezhang/data_for_zezhang_mar29/test_data_mirirv3_sa_wd_48cube'

# Define destination paths
destination1 = '/data01/user-storage/y.zezhang/2024_subsample_project/mod_Neural_network_training/30/training'
destination2 = '/data01/user-storage/y.zezhang/2024_subsample_project/mod_Neural_network_training/30/testing'
destination3 = '/data01/user-storage/y.zezhang/2024_subsample_project/mod_Neural_network_training/30/testing_demist'

# Create destination directories if they do not exist
os.makedirs(destination1, exist_ok=True)
os.makedirs(destination2, exist_ok=True)
os.makedirs(destination3, exist_ok=True)


# Get subfolder names
group1_subfolders = get_subfolder_names(group1_folders)
group2_subfolders = get_subfolder_names(group2_folders)
group3_subfolders = get_subfolder_names(group3_folders)
group4_subfolders = get_subfolder_names(group4_folders)

# Flatten the lists of subfolders
all_group1_subfolders = [subfolder for sublist in group1_subfolders.values() for subfolder in sublist]
all_group2_subfolders = [subfolder for sublist in group2_subfolders.values() for subfolder in sublist]
all_group3_subfolders = [subfolder for sublist in group3_subfolders.values() for subfolder in sublist]
all_group4_subfolders = [subfolder for sublist in group4_subfolders.values() for subfolder in sublist]

# Copy subfolders from group1 to destination1 using source_folder1
copied_subfolders_dest1 = copy_subfolders(source_folder1, all_group1_subfolders, destination1)

# Copy subfolders from group2 to destination2 using source_folder2
copied_subfolders_dest2 = copy_subfolders(source_folder2, all_group2_subfolders, destination2)

# Copy subfolders from group3 to destination2 using source_folder3
copied_subfolders_dest3 = copy_subfolders(source_folder3, all_group3_subfolders, destination3)

# Copy subfolders from group4 to destination2 using source_folder3
copied_subfolders_dest4 = copy_subfolders(source_folder3, all_group4_subfolders, destination3)


print(f"Subfolders copied to '{destination1}': {copied_subfolders_dest1}")
print(f"Subfolders copied to '{destination2}': {copied_subfolders_dest2}")
print(f"Subfolders copied to '{destination3}': {copied_subfolders_dest3}")
print(f"Subfolders copied to '{destination3}': {copied_subfolders_dest4}")

