import os

def get_subfolder_names(directory):
    return set(name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name)))

def find_non_overlapping_subfolders(folder1, folder2, output_file):
    # Get subfolder names from both directories
    subfolders1 = get_subfolder_names(folder1)
    subfolders2 = get_subfolder_names(folder2)

    # Find non-overlapping subfolders
    non_overlapping = (subfolders1.symmetric_difference(subfolders2))

    # Save the non-overlapping subfolder names to a text file
    with open(output_file, 'w') as file:
        for subfolder in sorted(non_overlapping):
            file.write(f"{subfolder}\n")
    
    print(f"Non-overlapping subfolder names saved to {output_file}")

# Example usage
folder1 = '/data01/user-storage/y.zezhang/2024_subsample_project/mod_subsample_projection/30/hl_asq'      # Replace with the path to your first directory
folder2 = '/data01/user-storage/y.zezhang/2024_subsample_project/mod_subsample_projection/30/hl_asq_part'     # Replace with the path to your second directory
output_file = 'missing_patient.txt'  # Replace with the desired output file path

find_non_overlapping_subfolders(folder1, folder2, output_file)