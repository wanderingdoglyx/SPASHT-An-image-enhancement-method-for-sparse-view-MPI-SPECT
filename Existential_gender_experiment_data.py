import os

# Function to get the list of subfolder names in a directory
def get_subfolder_names(directory):
    return [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]

# Function to filter rows based on subfolder names from two directories
def filter_rows_by_subfolder_names(subfolder_names1, subfolder_names2, input_file_path, output_file_path):
    # Combine subfolder names from both directories
    combined_subfolder_names = set(subfolder_names1).union(set(subfolder_names2))

    # Open the input file and read its content
    with open(input_file_path, 'r') as input_file:
        lines = input_file.readlines()

    # Prepare a list to hold filtered lines
    filtered_lines = []

    # Iterate over the lines, check if the first column matches any subfolder name
    for line in lines:
        first_column_value = line.strip().split('\t')[0]
        if first_column_value in combined_subfolder_names:
            filtered_lines.append(line)

    # Write the filtered lines to the output file
    with open(output_file_path, 'w') as output_file:
        output_file.writelines(filtered_lines)

    print(f"Filtered content saved as '{output_file_path}'")

# Paths to your directories and files
directory_path1 = '/data01/user-storage/y.zezhang/2024_subsample_project/mod_subsample_projection/30/hl_asq'  # Replace with the path to your first directory
directory_path2 = '/data01/user-storage/y.zezhang/2024_subsample_project/mod_subsample_projection/30/def' # Replace with the path to your second directory
input_file_path = '/data01/user-storage/y.zezhang/2024_subsample_project/document/combined_final_test_pat_list_hl.txt'        # Replace with the path to your input text file
output_file_path = '/data01/user-storage/y.zezhang/2024_subsample_project/document/combined_final_test_pat_list_hl_v2.txt'       # Replace with the path to save the filtered output file

# Get the list of subfolder names from both directories
subfolder_names1 = get_subfolder_names(directory_path1)
subfolder_names2 = get_subfolder_names(directory_path2)

# Filter the rows in the text file by subfolder names from both directories
filter_rows_by_subfolder_names(subfolder_names1, subfolder_names2, input_file_path, output_file_path)