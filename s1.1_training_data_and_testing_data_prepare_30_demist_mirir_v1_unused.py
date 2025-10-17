import os
import shutil

def read_columns_separately(file_path):
    # Initialize empty lists to store each column's values
    first_column = []
    second_column = []
    third_column = []

    # Open the file and read its content
    with open(file_path, 'r') as file:
        lines = file.readlines()

        # Iterate over each line in the file
        for line in lines:
            # Split the line by the tab character (or other delimiter)
            columns = line.strip().split('\t')

            # Ensure the line has at least three columns
            if len(columns) >= 3:
                # Append each column value to the corresponding list
                first_column.append(columns[0])
                second_column.append(columns[1])
                third_column.append(columns[2])

    return first_column, second_column, third_column


def copy_subfolders_by_name(names_list, source_dir1, source_dir2, target_dir):
    # Ensure the target directory exists
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # Function to copy matching subfolders from a source directory
    def copy_matching_subfolders(source_dir):
        for name in os.listdir(source_dir):
            subfolder_path = os.path.join(source_dir, name)
            if os.path.isdir(subfolder_path) and name in names_list:
                # Copy the subfolder to the target directory
                target_subfolder_path = os.path.join(target_dir, name)
                
                # If the target subfolder exists, remove it
                if os.path.exists(target_subfolder_path):
                    shutil.rmtree(target_subfolder_path)
                    print(f"Removed existing folder {target_subfolder_path}")

                # Copy the subfolder to the target directory
                shutil.copytree(subfolder_path, target_subfolder_path)
                print(f"Copied {name} from {source_dir} to {target_dir}")

    # Copy subfolders from both source directories
    copy_matching_subfolders(source_dir1)
    copy_matching_subfolders(source_dir2)
    
def merge_folders(src, dest):
    # Iterate over all items in the source directory
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)

        if os.path.isdir(src_path):
            # If the item is a directory, ensure it exists in the destination and recurse into it
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)
            merge_folders(src_path, dest_path)
        else:
            # If the item is a file, copy it to the destination (overwrite if it exists)
            shutil.copy2(src_path, dest_path)

def copy_and_merge_subfolders_by_name(names_list, source_dir1, source_dir2, target_dir):
    # Ensure the target directory exists
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # Function to copy and merge matching subfolders from a source directory
    def copy_matching_subfolders(source_dir):
        for name in os.listdir(source_dir):
            subfolder_path = os.path.join(source_dir, name)
            if os.path.isdir(subfolder_path) and name in names_list:
                # Define the target subfolder path
                target_subfolder_path = os.path.join(target_dir, name)
                
                # If the target subfolder doesn't exist, create it
                if not os.path.exists(target_subfolder_path):
                    os.makedirs(target_subfolder_path)

                # Merge the subfolder contents into the target subfolder
                merge_folders(subfolder_path, target_subfolder_path)
                print(f"Merged {name} from {source_dir} into {target_dir}")

    # Copy and merge subfolders from both source directories
    copy_matching_subfolders(source_dir1)
    copy_matching_subfolders(source_dir2)
    
    
pat_id_arr_fname_def = '/data01/user-storage/y.zezhang/2024_subsample_project/document/combined_final_test_pat_list_def.txt'  # Replace with the path to your combined text file
columns_def1,columns_def2,columns_def3 = read_columns_separately(pat_id_arr_fname_def)

pat_id_arr_fname_hl = '/data01/user-storage/y.zezhang/2024_subsample_project/document/combined_final_test_pat_list_hl_v2.txt'  # Replace with the path to your combined text file
columns_hl1,columns_hl2,columns_hl3 = read_columns_separately(pat_id_arr_fname_hl)


# Example usage
names_list = columns_def1 +columns_hl1  # Replace with your list of folder names
#print(names_list)
source_dir1 = '/data01/user-storage/y.zezhang/data_for_zezhang_mar29/test_data_sa_wd_fix2_48cube'         # Replace with the path to your first source directory
source_dir2 = '/data01/user-storage/y.zezhang/data_for_zezhang_mar29/test_data_mirirv3_sa_wd_48cube'        # Replace with the path to your second source directory
target_dir = '/data01/user-storage/y.zezhang/2024_subsample_project/mod_Neural_network_training/30/testing_demist'         # Replace with the path to your target directory

copy_subfolders_by_name(names_list, source_dir1, source_dir2, target_dir)