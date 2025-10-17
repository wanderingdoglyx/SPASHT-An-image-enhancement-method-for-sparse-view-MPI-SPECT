import random

def split_patients_file(input_file, output_file_1, output_file_2):
    """
    Reads a text file of patient IDs, randomly shuffles the list, 
    and splits it into two separate output files with equal numbers of patients.

    Parameters:
        input_file (str): Path to the input file containing patient IDs.
        output_file_1 (str): Path for the first output file to store half of the patients.
        output_file_2 (str): Path for the second output file to store the other half of the patients.
    """
    # Read patient IDs from the input file
    with open(input_file, 'r') as file:
        patients = [line.strip() for line in file.readlines()]

    # Shuffle the patient list to ensure random distribution
    random.shuffle(patients)

    # Calculate the midpoint to divide the list into two halves
    midpoint = len(patients) // 2

    # Split the patients into two halves
    patients_part1 = patients[:midpoint]
    patients_part2 = patients[midpoint:]

    # Write the first half to the first output file
    with open(output_file_1, 'w') as file1:
        for patient in patients_part1:
            file1.write(f"{patient}\n")

    # Write the second half to the second output file
    with open(output_file_2, 'w') as file2:
        for patient in patients_part2:
            file2.write(f"{patient}\n")

    print(f"Patients have been split into '{output_file_1}' and '{output_file_2}'.")

# Example usage
# Input and output file paths
input_file_czt = '/data01/user-storage/y.zezhang/2024_subsample_project/document/collimator_record/czt_testing_patients.txt'           # Input file containing the list of patients
output_file_czt_def = '/data01/user-storage/y.zezhang/2024_subsample_project/document/collimator_record/czt_testing_patients_def.txt'   # Output file for the first half of patients
output_file_czt_hl = '/data01/user-storage/y.zezhang/2024_subsample_project/document/collimator_record/czt_testing_patients_hl.txt'  # Output file for the second half of patients

input_file_nai = '/data01/user-storage/y.zezhang/2024_subsample_project/document/collimator_record/nai_testing_patients.txt'           # Input file containing the list of patients
output_file_nai_def = '/data01/user-storage/y.zezhang/2024_subsample_project/document/collimator_record/nai_testing_patients_def.txt'   # Output file for the first half of patients
output_file_nai_hl = '/data01/user-storage/y.zezhang/2024_subsample_project/document/collimator_record/nai_testing_patients_hl.txt'  # Output file for the second half of patients


split_patients_file(input_file_czt, output_file_czt_def, output_file_czt_hl)
split_patients_file(input_file_nai, output_file_nai_def, output_file_nai_hl)
    