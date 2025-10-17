import random

# Function to randomly select n rows from the input file with a seed for reproducibility
def select_random_rows(input_file, output_file, n, seed_value):
    # Set the seed for reproducibility
    random.seed(seed_value)
    
    # Read all lines from the input file
    with open(input_file, 'r') as infile:
        lines = infile.readlines()
    
    # Check if n is less than the total number of lines
    if n > len(lines):
        print(f"Requested number of rows ({n}) exceeds the total lines in the file ({len(lines)}).")
        return
    
    # Randomly select n lines
    selected_lines = random.sample(lines, n)
    
    # Write the selected lines to the output file
    with open(output_file, 'w') as outfile:
        outfile.writelines(selected_lines)
    
    print(f"{n} rows have been written to {output_file}.")

source_path=f'/data01/user-storage/y.zezhang/2024_subsample_project/document'
save_path=f'/datastore01/user-storage/y.zezhang/image_inspect'
# Example usage

n = 130                    # Replace with the number of rows you want to select
seed_value = 43#42            # Replace with your desired seed value

input_file = f'{source_path}/zitong_patient_list/pat_id_diseased_v3_defect_selected.txt'   # Replace with the path of your input file
output_file = f'{save_path}/observer_study_patient_list/pat_id_diseased_pilot_defect_selected.txt' # Replace with the path of your output file
select_random_rows(input_file, output_file, n, seed_value)

input_file = f'{source_path}/zitong_patient_list/pat_id_healthy_v3.txt'   # Replace with the path of your input file
output_file = f'{save_path}/observer_study_patient_list/pat_id_healthy_pilot.txt' # Replace with the path of your output file
select_random_rows(input_file, output_file, n, seed_value)