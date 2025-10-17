import os
import pandas as pd

# Paths to the Excel files and main directory
excel_file_1 = '/data01/user-storage/y.zezhang/2024_subsample_project/document/collimator_record/collimator_training_data.xlsx'  # Replace with the actual path
excel_file_2 = '/data01/user-storage/y.zezhang/2024_subsample_project/document/collimator_record/collimator_testing_data.xlsx'  # Replace with the actual path
main_directory = '/data01/user-storage/y.zezhang/2024_subsample_project/mod_subsample_projection/30/hl_asq_full'             # Replace with the path to the directory containing subfolders

# Output files
czt_output_file = '/data01/user-storage/y.zezhang/2024_subsample_project/document/collimator_record/patients_with_CZT.txt'
nai_output_file = '/data01/user-storage/y.zezhang/2024_subsample_project/document/collimator_record/patients_with_NaI.txt'

# Read Excel files and ensure 'patient' column is read as a string
data1 = pd.read_excel(excel_file_1, dtype={'patient': str})
data2 = pd.read_excel(excel_file_2, dtype={'patient': str})

# Combine both dataframes into a single one
data = pd.concat([data1, data2])

# Get list of subfolder names in the main directory
subfolder_names = [name for name in os.listdir(main_directory) if os.path.isdir(os.path.join(main_directory, name))]

# Filter out patients present in subfolder names
filtered_data = data[~data['patient'].isin(subfolder_names)]
#filtered_data = data
# Open output files to write filtered patient IDs based on Material type
with open(czt_output_file, 'w') as czt_file, open(nai_output_file, 'w') as nai_file:
    for index, row in filtered_data.iterrows():
        if row['Material'] == 'CZT':
            czt_file.write(f"{row['patient']}\n")
        elif row['Material'] == 'NaI':
            nai_file.write(f"{row['patient']}\n")

print(f"Patients with Material = 'CZT' have been recorded in {czt_output_file}.")
print(f"Patients with Material = 'NaI' have been recorded in {nai_output_file}.")