import os
import shutil
from math import floor
from random import shuffle
import numpy as np

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


slice_number=5

testing30full='/data01/user-storage/y.zezhang/2024_subsample_project/mod_Neural_network_training/30/testing'
training30full='/data01/user-storage/y.zezhang/2024_subsample_project/mod_Neural_network_training/30/training'


testing_patient = os.listdir(testing30full)
training_patient = os.listdir(training30full)


copy_directory_base_diseased='/data01/user-storage/y.zezhang/2024_subsample_project/mod_SA_images/'+str(slice_number)+'/diseased'
copy_directory_base_healthy='/data01/user-storage/y.zezhang/2024_subsample_project/mod_SA_images/'+str(slice_number)+'/healthy'
testing_destination_directory_base = '/data01/user-storage/y.zezhang/2024_subsample_project/mod_Neural_network_training/'+str(slice_number) +'/testing'
training_destination_directory_base = '/data01/user-storage/y.zezhang/2024_subsample_project/mod_Neural_network_training/'+str(slice_number) +'/training'
#testing_destination_directory_base_demist = '/data01/user-storage/y.zezhang/2024_subsample_project/mod_Neural_network_training/'+str(slice_number) +'/testing'


###
pat_id_arr_fname = f'/data01/user-storage/y.zezhang/2024_subsample_project/document/zitong_patient_list/pat_id_diseased_v2.txt'
diseased_patients = np.loadtxt(pat_id_arr_fname, dtype = 'str', comments="#", delimiter=",", unpack=False)

pat_id_arr_fname = f'/data01/user-storage/y.zezhang/2024_subsample_project/document/zitong_patient_list/pat_id_healthy_v2.txt'
healthy_patients = np.loadtxt(pat_id_arr_fname, dtype = 'str', comments="#", delimiter=",", unpack=False)

copy_and_merge_folders(copy_directory_base_diseased, testing_destination_directory_base, diseased_patients)
copy_and_merge_folders(copy_directory_base_healthy, testing_destination_directory_base, healthy_patients)
####


copy_and_merge_folders(copy_directory_base_diseased, testing_destination_directory_base, testing_patient)
copy_and_merge_folders(copy_directory_base_healthy, testing_destination_directory_base, testing_patient)
copy_and_merge_folders(copy_directory_base_healthy, training_destination_directory_base, training_patient)
copy_and_merge_folders(copy_directory_base_diseased, training_destination_directory_base, training_patient)

pat_id_arr_fname_def = '/data01/user-storage/y.zezhang/2024_subsample_project/document/combined_final_test_pat_list_def.txt'  # Replace with the path to your combined text file
columns_def1,columns_def2,columns_def3 = read_columns_separately(pat_id_arr_fname_def)

pat_id_arr_fname_hl = '/data01/user-storage/y.zezhang/2024_subsample_project/document/combined_final_test_pat_list_hl_v2.txt'  # Replace with the path to your combined text file
columns_hl,columns_hl2,columns_hl3 = read_columns_separately(pat_id_arr_fname_hl)

copy_and_merge_folders(copy_directory_base_diseased, testing_destination_directory_base, columns_def1)
copy_and_merge_folders(copy_directory_base_healthy, testing_destination_directory_base, columns_hl)

pat_id_arr_fname = f'/data01/user-storage/y.zezhang/2024_subsample_project/document/zitong_patient_list/pat_id_diseased_v2.txt'
diseased_patients = np.loadtxt(pat_id_arr_fname, dtype = 'str', comments="#", delimiter=",", unpack=False)

pat_id_arr_fname = f'/data01/user-storage/y.zezhang/2024_subsample_project/document/zitong_patient_list/pat_id_healthy_v2.txt'
healthy_patients = np.loadtxt(pat_id_arr_fname, dtype = 'str', comments="#", delimiter=",", unpack=False)

copy_and_merge_folders(copy_directory_base_diseased, testing_destination_directory_base, diseased_patients)
copy_and_merge_folders(copy_directory_base_healthy, testing_destination_directory_base, healthy_patients)