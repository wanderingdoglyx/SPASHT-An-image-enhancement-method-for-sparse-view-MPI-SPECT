import os
import pandas as pd

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


########## 
pat_id_arr_fname_def = f'/data01/user-storage/y.zezhang/2024_subsample_project/document/zitong_patient_list/pat_id_diseased_v3.txt'
pat_id_arr_fname_hl = f'/data01/user-storage/y.zezhang/2024_subsample_project/document/zitong_patient_list/pat_id_healthy_v3.txt'

# CZT DEF
czt_file = '/data01/user-storage/y.zezhang/2024_subsample_project/document/collimator_record/patients_with_CZT_ZT_test.txt'
czt_file_output_def = '/data01/user-storage/y.zezhang/2024_subsample_project/document/collimator_record/patients_with_CZT_ZT_test_def.txt'
find_overlapping_patient_ids(czt_file, pat_id_arr_fname_def, czt_file_output_def)

#CZT HL
czt_file = '/data01/user-storage/y.zezhang/2024_subsample_project/document/collimator_record/patients_with_CZT_ZT_test.txt'
czt_file_output_hl = '/data01/user-storage/y.zezhang/2024_subsample_project/document/collimator_record/patients_with_CZT_ZT_test_hl.txt'
find_overlapping_patient_ids(czt_file, pat_id_arr_fname_hl, czt_file_output_hl)

#NAI DEF
nai_file = '/data01/user-storage/y.zezhang/2024_subsample_project/document/collimator_record/patients_with_NaI_ZT_test.txt'
nai_file_output_def = '/data01/user-storage/y.zezhang/2024_subsample_project/document/collimator_record/patients_with_NaI_ZT_test_def.txt'
find_overlapping_patient_ids(czt_file, pat_id_arr_fname_def, nai_file_output_def)

#NAI HL
nai_file = '/data01/user-storage/y.zezhang/2024_subsample_project/document/collimator_record/patients_with_NaI_ZT_test.txt'
nai_file_output_hl = '/data01/user-storage/y.zezhang/2024_subsample_project/document/collimator_record/patients_with_NaI_ZT_test_hl.txt'
find_overlapping_patient_ids(czt_file, pat_id_arr_fname_hl, nai_file_output_hl)
