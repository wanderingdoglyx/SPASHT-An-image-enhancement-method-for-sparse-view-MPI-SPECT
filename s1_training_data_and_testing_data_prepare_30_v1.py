import os
import shutil
from math import floor
from random import shuffle

def divide_and_copy_folders(source_dir, dest_dir, group1_name, group2_name, ratio):
    # Ensure destination directories exist
    group1_dir = os.path.join(dest_dir, group1_name)
    group2_dir = os.path.join(dest_dir, group2_name)
    os.makedirs(group1_dir, exist_ok=True)
    os.makedirs(group2_dir, exist_ok=True)
    
    # Get list of subfolders
    subfolders = [f for f in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, f))]
    
    # Shuffle the subfolders to ensure randomness
    shuffle(subfolders)
    
    # Calculate split index
    split_index = floor(len(subfolders) * ratio)
    
    # Divide subfolders into two groups
    group1 = subfolders[:split_index]
    group2 = subfolders[split_index:]
    
    # Function to copy subfolders to a destination
    def copy_subfolders(subfolders, dest):
        for folder in subfolders:
            src_path = os.path.join(source_dir, folder)
            dest_path = os.path.join(dest, folder)
            shutil.copytree(src_path, dest_path)
    
    # Copy the groups to the respective directories
    copy_subfolders(group1, group1_dir)
    copy_subfolders(group2, group2_dir)
    
    print(f'Group 1 ({len(group1)} folders) copied to: {group1_dir}')
    print(f'Group 2 ({len(group2)} folders) copied to: {group2_dir}')

# Example usage
source_directory = '/data01/user-storage/y.zezhang/data_for_zezhang_mar29/test_data_mirirv3_sa_wd_48cube'
destination_directory = '/data01/user-storage/y.zezhang/2024_subsample_project/mod_Neural_network_training/30'
group1_name = 'training'
group2_name = 'testing'
ratio = 0.8  # 80% of the folders in group1 and 20% in group2

divide_and_copy_folders(source_directory, destination_directory, group1_name, group2_name, ratio)
'''
num_pat = 184
num_data_dict = {
    'hl': {
            'start_ind': 0,
            'end_ind': num_pat-1,
            },
    'def': {
            'start_ind': 0,
            'end_ind': num_pat-1,
            }
    }

loc_arr = ['a', 'i']                  #############################################################
sev_arr = [100, 175, 250]             #############################################################
ext_arr = [30, 60]                    #############################################################
'''