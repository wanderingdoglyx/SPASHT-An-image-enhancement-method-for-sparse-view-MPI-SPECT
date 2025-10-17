import scipy.io
import os

def save_patient_list_to_txt(patient_list, file_name):
    with open(file_name, 'w') as file:
        for patient_id in patient_list:
            # Write the patient ID as a plain string, without list brackets or quotes
            file.write(f"{patient_id[0]}\n")

def read_and_save_patient_lists(mat_file_male, mat_file_female, output_dir):
    # Load the .mat files
    mat_data_male = scipy.io.loadmat(mat_file_male)
    mat_data_female = scipy.io.loadmat(mat_file_female)

    # Extract the patient lists
    M_patients = mat_data_male['M_patients'].squeeze().tolist()
    F_patients = mat_data_female['F_patients'].squeeze().tolist()

    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save the male patient list
    save_patient_list_to_txt(M_patients, os.path.join(output_dir, 'ze_M_patients.txt'))
    print("M_patients list saved to M_patients.txt")

    # Save the female patient list
    save_patient_list_to_txt(F_patients, os.path.join(output_dir, 'ze_F_patients.txt'))
    print("F_patients list saved to F_patients.txt")

    # Combine both lists
    combined_patients = M_patients + F_patients
    save_patient_list_to_txt(combined_patients, os.path.join(output_dir, 'ze_combined_patients.txt'))
    print("Combined patient list saved to combined_patients.txt")


# Example usage
mat_file_male = '/data01/user-storage/y.zezhang/2024_subsample_project/document/zitong_patient_list/M_patients.mat'      # Replace with the path to your .mat file containing M_patients
mat_file_female = '/data01/user-storage/y.zezhang/2024_subsample_project/document/zitong_patient_list/F_patients.mat'  # Replace with the path to your .mat file containing F_patients
output_dir = '/data01/user-storage/y.zezhang/2024_subsample_project/document/zitong_patient_list'                  # Replace with the desired output directory

read_and_save_patient_lists(mat_file_male, mat_file_female, output_dir)
