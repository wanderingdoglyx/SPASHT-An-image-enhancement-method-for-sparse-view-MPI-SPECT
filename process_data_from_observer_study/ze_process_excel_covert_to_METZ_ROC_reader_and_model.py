import pandas as pd
import glob
import os
import datetime

study_name='pilot_study_METZ'

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

def replace_chars(input_string):
    # Replace '.' with '_'
    result_string = input_string.replace('.', '_')
    # Replace '@' with '_'
    result_string = result_string.replace('@', '_')
    return result_string


# Example usage
folder_path = '/data01/user-storage/y.zezhang/2024_false_defect_project/pilot_study/observer_study'  # Replace with your Excel file path

all_csv_data = read_all_csvs_in_folder(folder_path)


#==========================================
# save all random parameters setting text
#==========================================
txt_filename=f'{study_name}.txt'


for file_data in all_csv_data:
    
    trainer_name=file_data[0][0]
    trainer_name=replace_chars(trainer_name)
    txt_filename=f'{study_name}_{trainer_name}.txt'
    
    with open(txt_filename, "w") as file:
        lines = [f'Initial Line\n', 
            f'Large\n',]
        file.writelines(lines)
        for row in file_data:
            if int(row[2]) ==0:
                lines= [f'{row[3]}\n',]
                file.writelines(lines)
        lines= [f'*\n',]
        file.writelines(lines)
        for row in file_data:
            if int(row[2]) ==1:
                lines= [f'{row[3]}\n',]
                file.writelines(lines)
        lines= [f'*\n',]
        file.writelines(lines)  
    file.close()    