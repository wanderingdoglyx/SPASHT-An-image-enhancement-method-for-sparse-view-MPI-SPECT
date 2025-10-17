import pandas as pd
import numpy as np

# Define file paths for the input and output
czt_input_file = '/data01/user-storage/y.zezhang/2024_subsample_project/document/collimator_record/patients_with_CZT.txt'  # Input file for CZT patients
nai_input_file = '/data01/user-storage/y.zezhang/2024_subsample_project/document/collimator_record/patients_with_NaI.txt'  # Input file for NaI patients

save_base='/data01/user-storage/y.zezhang/2024_subsample_project/document/collimator_record'
czt_train_file = f'{save_base}/czt_training_patients.txt'
czt_test_file = f'{save_base}/czt_testing_patients.txt'
nai_train_file = f'{save_base}/nai_training_patients.txt'
nai_test_file = f'{save_base}/nai_testing_patients.txt'

# Function to split patient IDs into training and testing sets
def split_data(input_file, train_file, test_file, train_ratio=0.7):
    # Read patient IDs from the input file
    with open(input_file, 'r') as file:
        patients = [line.strip() for line in file.readlines()]

    # Shuffle the patient list
    np.random.shuffle(patients)

    # Calculate the split index
    split_index = int(len(patients) * train_ratio)

    # Split into training and testing sets
    train_patients = patients[:split_index]
    test_patients = patients[split_index:]

    # Write the training and testing sets to their respective files
    with open(train_file, 'w') as train_file_handle:
        for patient in train_patients:
            train_file_handle.write(f"{patient}\n")

    with open(test_file, 'w') as test_file_handle:
        for patient in test_patients:
            test_file_handle.write(f"{patient}\n")

    print(f"Data split completed for {input_file}.")
    print(f"Training patients saved to {train_file}.")
    print(f"Testing patients saved to {test_file}.")

# Split CZT and NaI patient IDs
split_data(czt_input_file, czt_train_file, czt_test_file)
split_data(nai_input_file, nai_train_file, nai_test_file)