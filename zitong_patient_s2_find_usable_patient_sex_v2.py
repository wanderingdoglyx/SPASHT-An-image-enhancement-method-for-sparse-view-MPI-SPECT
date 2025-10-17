def read_patient_ids(file_path):
    with open(file_path, 'r') as file:
        return set(line.strip() for line in file)

def find_overlapping_patient_ids(file1, file2, output_file):
    # Read patient IDs from both text files
    patient_ids_1 = read_patient_ids(file1)
    patient_ids_2 = read_patient_ids(file2)

    # Find overlapping patient IDs
    overlapping_ids = patient_ids_1.intersection(patient_ids_2)

    # Save overlapping patient IDs to a new text file
    with open(output_file, 'w') as file:
        for patient_id in sorted(overlapping_ids):
            file.write(f"{patient_id}\n")

    print(f"Overlapping patient IDs saved to {output_file}")

# Example usage
female_patient = '/data01/user-storage/y.zezhang/2024_subsample_project/document/zitong_patient_list/ze_F_patients.txt'   # Replace with the path to your first patient ID text file
male_patient = '/data01/user-storage/y.zezhang/2024_subsample_project/document/zitong_patient_list/ze_M_patients.txt'  # Replace with the path to your second patient ID text file

healthy_patient='/data01/user-storage/y.zezhang/2024_subsample_project/document/zitong_patient_list/pat_id_healthy_v2.txt'
diseased_patient='/data01/user-storage/y.zezhang/2024_subsample_project/document/zitong_patient_list/pat_id_diseased_v2.txt'

male_diseased_patient = '/data01/user-storage/y.zezhang/2024_subsample_project/document/zitong_patient_list/ze_male_diseased_patient_ids.txt'  # Replace with the desired output file path
male_healthy_patient = '/data01/user-storage/y.zezhang/2024_subsample_project/document/zitong_patient_list/ze_male_healthy_patient_ids.txt'
female_diseased_patient = '/data01/user-storage/y.zezhang/2024_subsample_project/document/zitong_patient_list/ze_female_diseased_patient_ids.txt'  
female_healthy_patient = '/data01/user-storage/y.zezhang/2024_subsample_project/document/zitong_patient_list/ze_female_healthy_patient_ids.txt'


find_overlapping_patient_ids(diseased_patient, male_patient, male_diseased_patient)
find_overlapping_patient_ids(healthy_patient, male_patient, male_healthy_patient)
find_overlapping_patient_ids(diseased_patient, female_patient, female_diseased_patient)
find_overlapping_patient_ids(healthy_patient, female_patient, female_healthy_patient)