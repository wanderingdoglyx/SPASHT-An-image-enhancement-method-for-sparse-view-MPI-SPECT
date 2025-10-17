import pandas as pd
import glob
import os
import datetime

study_name='pilot_study'
modalities=3
number_of_reader=4
number_of_nondiseased_case=30
number_of_diseased_case=30

name_of_modalities=['sparse_view','task-specific','full_view']
#name_of_modalities=['task-specific','full_view','sparse_view']
#name_of_modalities=['full_view','sparse_view','task-specific']

# Function to read CSV file and store in arrays
def read_csv_to_arrays(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path)

    # Convert DataFrame to list of arrays
    arrays = df.values.tolist()

    return arrays

# Function to read all CSV files in a folder
def read_all_csvs_in_folder(folder_path):
    # List to store data from all files
    all_data = []

    # Get all CSV files in the folder
    csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

    # Loop through each file and read its data
    for file in csv_files:
        print(f'Reading {file}...')
        data_arrays = read_csv_to_arrays(file)
        all_data.append(data_arrays)

    return all_data



# Example usage
#folder_path = '/data01/user-storage/y.zezhang/2024_subsample_project/observer_study/manually selected patient result'  # Replace with your Excel file path
folder_path = '/data01/user-storage/y.zezhang/2024_subsample_project/observer_study/pilot_study_result/10 sparse-view level'
all_csv_data = read_all_csvs_in_folder(folder_path)


#==========================================
# save all random parameters setting text
#==========================================
txt_filename=f'{study_name}.imrmc'
current_time= datetime.datetime.now()


with open(txt_filename, "w") as file:
    lines = [f'Simulated iMRMC input from {current_time}\n', 
            f'\n',
            f'NR: {number_of_reader}\n',
            f'N0: {number_of_nondiseased_case*modalities}\n',
            f'N1: {number_of_diseased_case*modalities}\n',
            f'NM: {modalities}\n',
            f'\n',
            f'BEGIN DATA:\n',]
    file.writelines(lines)
    file_data = all_csv_data[0]
    for row in file_data:
            line = [f'-1,case{row[1]}{int(row[2])},0,{int(row[2])}\n', ]
            #line = [f'0,case{row[1]}{int(row[2])},-1,{int(row[2])}\n', ]
            #print(row)
            file.writelines(line)
                
    for file_data in all_csv_data:
        for row in file_data:
                #line = [f'reader{row[0]},case{row[1]}{int(row[2])},{name_of_modalities[(row[1]-1)%int(modalities)]},{(row[3])}\n', ]
                line = [f'reader{row[0]},case{row[1]}{int(row[2])},{name_of_modalities[(row[1]-1)%int(modalities)]},{(7-(row[3])+1)}\n', ]
                #print(row)
                file.writelines(line)
file.close()
#run in jupyter notebook