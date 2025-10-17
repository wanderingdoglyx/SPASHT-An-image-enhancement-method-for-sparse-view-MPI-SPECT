import os

def read_patient_ids_from_txt(file_path):
    with open(file_path, 'r') as file:
        return set(line.strip() for line in file)

def get_subfolder_names(directory):
    return set(name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name)))

def find_overlapping_patient_ids(txt_file, folder, output_file):
    # Read patient IDs from the text file
    patient_ids = read_patient_ids_from_txt(txt_file)

    # Get subfolder names from the directory
    subfolders = get_subfolder_names(folder)

    # Find the overlapping patient IDs
    overlapping_ids = patient_ids.intersection(subfolders)

    # Save the overlapping patient IDs to a new text file
    with open(output_file, 'w') as file:
        for patient_id in sorted(overlapping_ids):
            file.write(f"{patient_id}\n")
    
    print(f"Overlapping patient IDs saved to {output_file}")

# Example usage
txt_file = 'ze_combined_patients.txt'     # Replace with the path to your patient ID text file
folder = '/data01/user-storage/y.zezhang/2024_subsample_project/mod_subsample_projection/30/def'  # Replace with the path to your directory
output_file = 'ze_combined_patients.txt'  # Replace with the desired output file path

find_overlapping_patient_ids(txt_file, folder, output_file)