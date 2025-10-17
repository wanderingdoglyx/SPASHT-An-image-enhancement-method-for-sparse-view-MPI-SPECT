# Function to combine three text files into one with three columns
def combine_files(file1_path, file2_path, file3_path, output_file_path):
    # Open the first file and read the content
    with open(file1_path, 'r') as file1:
        file1_lines = file1.readlines()

    # Open the second file and read the content
    with open(file2_path, 'r') as file2:
        file2_lines = file2.readlines()

    # Open the third file and read the content
    with open(file3_path, 'r') as file3:
        file3_lines = file3.readlines()

    # Ensure all files have the same number of lines
    if len(file1_lines) != len(file2_lines) or len(file2_lines) != len(file3_lines):
        print("Warning: The files have different numbers of lines. Extra lines will be ignored.")

    # Determine the number of lines to process (based on the shortest file)
    num_lines = min(len(file1_lines), len(file2_lines), len(file3_lines))

    # Open the output file for writing
    with open(output_file_path, 'w') as output_file:
        # Iterate over the lines and write them to the output file
        for i in range(num_lines):
            # Combine the lines from all three files into one line with three columns
            combined_line = f"{file1_lines[i].strip()}\t{file2_lines[i].strip()}\t{file3_lines[i].strip()}\n"
            output_file.write(combined_line)

    print(f"Combined file saved as '{output_file_path}'")

# Paths to your input files and output file
#file1_path = 'file1.txt'
#file2_path = 'file2.txt'
#file3_path = 'file3.txt'
#output_file_path = 'combined_file.txt'

# Call the function to combine the files
#combine_files(file1_path, file2_path, file3_path, output_file_path)


# Paths to your input files and output file
file1_path = '/data01/user-storage/y.zezhang/2024_subsample_project/document/demist/final_test_pat_list_def.txt'
file2_path = '/data01/user-storage/y.zezhang/2024_subsample_project/document/demist/final_test_pat_list_def_gender.txt'
file3_path = '/data01/user-storage/y.zezhang/2024_subsample_project/document/demist/final_test_pat_list_def_src.txt'
output_file_path = '/data01/user-storage/y.zezhang/2024_subsample_project/document/combined_final_test_pat_list_def.txt'
combine_files(file1_path, file2_path, file3_path, output_file_path)

file1_path = '/data01/user-storage/y.zezhang/2024_subsample_project/document/demist/final_test_pat_list_hl.txt'
file2_path = '/data01/user-storage/y.zezhang/2024_subsample_project/document/demist/final_test_pat_list_hl_gender.txt'
file3_path = '/data01/user-storage/y.zezhang/2024_subsample_project/document/demist/final_test_pat_list_hl_src.txt'
output_file_path = '/data01/user-storage/y.zezhang/2024_subsample_project/document/combined_final_test_pat_list_hl.txt'
# Call the function to combine the files
combine_files(file1_path, file2_path, file3_path, output_file_path)

# Paths to your input files and output file
file1_path = '/data01/user-storage/y.zezhang/2024_subsample_project/document/zitong_patient_list/final_v2_test_pat_list_def.txt'
file2_path = '/data01/user-storage/y.zezhang/2024_subsample_project/document/zitong_patient_list/final_v2_test_pat_list_def_gender.txt'
file3_path = '/data01/user-storage/y.zezhang/2024_subsample_project/document/zitong_patient_list/final_v2_test_pat_list_def_src.txt'
output_file_path = '/data01/user-storage/y.zezhang/2024_subsample_project/document/zitong_patient_list/combined_v2_final_test_pat_list_def.txt'
combine_files(file1_path, file2_path, file3_path, output_file_path)

file1_path = '/data01/user-storage/y.zezhang/2024_subsample_project/document/zitong_patient_list/final_v2_test_pat_list_hl.txt'
file2_path = '/data01/user-storage/y.zezhang/2024_subsample_project/document/zitong_patient_list/final_v2_test_pat_list_hl_gender.txt'
file3_path = '/data01/user-storage/y.zezhang/2024_subsample_project/document/zitong_patient_list/final_v2_test_pat_list_hl_src.txt'
output_file_path = '/data01/user-storage/y.zezhang/2024_subsample_project/document/zitong_patient_list/combined_v2_final_test_pat_list_hl.txt'
# Call the function to combine the files
combine_files(file1_path, file2_path, file3_path, output_file_path)