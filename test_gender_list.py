# Function to combine two text files into one with two columns
def combine_files(file1_path, file2_path, output_file_path):
    # Open the first file and read the content
    with open(file1_path, 'r') as file1:
        file1_lines = file1.readlines()

    # Open the second file and read the content
    with open(file2_path, 'r') as file2:
        file2_lines = file2.readlines()

    # Ensure both files have the same number of lines
    if len(file1_lines) != len(file2_lines):
        print("Warning: The files have different numbers of lines. Extra lines will be ignored.")

    # Determine the number of lines to process (based on the shorter file)
    num_lines = min(len(file1_lines), len(file2_lines))

    # Open the output file for writing
    with open(output_file_path, 'w') as output_file:
        # Iterate over the lines and write them to the output file
        for i in range(num_lines):
            # Combine the lines from both files into one line with two columns
            combined_line = f"{file1_lines[i].strip()}\t{file2_lines[i].strip()}\n"
            output_file.write(combined_line)

    print(f"Combined file saved as '{output_file_path}'")

# Paths to your input files and output file
#file1_path = '/data01/user-storage/y.zezhang/2024_subsample_project/document/demist/final_test_pat_list_def.txt'
#file2_path = '/data01/user-storage/y.zezhang/2024_subsample_project/document/demist/final_test_pat_list_def_gender.txt'
#output_file_path = '/data01/user-storage/y.zezhang/2024_subsample_project/document/combined_final_test_pat_list_def.txt'

file1_path = '/data01/user-storage/y.zezhang/2024_subsample_project/document/demist/final_test_pat_list_hl.txt'
file2_path = '/data01/user-storage/y.zezhang/2024_subsample_project/document/demist/final_test_pat_list_hl_gender.txt'
output_file_path = '/data01/user-storage/y.zezhang/2024_subsample_project/document/combined_final_test_pat_list_hl.txt'
# Call the function to combine the files
combine_files(file1_path, file2_path, output_file_path)