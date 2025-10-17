# Function to merge two text files into one
def merge_files(file1, file2, output_file):
    try:
        # Open the first file and read its content
        with open(file1, 'r') as f1:
            content1 = f1.read()

        # Open the second file and read its content
        with open(file2, 'r') as f2:
            content2 = f2.read()

        # Combine the content from both files
        combined_content = content1 + content2

        # Write the combined content into the output file
        with open(output_file, 'w') as output:
            output.write(combined_content)

        print(f"Files '{file1}' and '{file2}' merged successfully into '{output_file}'.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Replace 'file1.txt' and 'file2.txt' with your actual file paths
#file1 = 'file1.txt'
#file2 = 'file2.txt'
#output_file = 'merged_file.txt'
#merge_files(file1, file2, output_file)


healthy_patient='/data01/user-storage/y.zezhang/2024_subsample_project/document/zitong_patient_list/pat_id_healthy_v3.txt'
diseased_patient='/data01/user-storage/y.zezhang/2024_subsample_project/document/zitong_patient_list/pat_id_diseased_v3.txt'

male_diseased_patient = '/data01/user-storage/y.zezhang/2024_subsample_project/document/zitong_patient_list/ze_male_diseased_patient_ids.txt'  # Replace with the desired output file path
male_healthy_patient = '/data01/user-storage/y.zezhang/2024_subsample_project/document/zitong_patient_list/ze_male_healthy_patient_ids.txt'
female_diseased_patient = '/data01/user-storage/y.zezhang/2024_subsample_project/document/zitong_patient_list/ze_female_diseased_patient_ids.txt'  
female_healthy_patient = '/data01/user-storage/y.zezhang/2024_subsample_project/document/zitong_patient_list/ze_female_healthy_patient_ids.txt'

merge_files(male_diseased_patient, female_diseased_patient, diseased_patient)
merge_files(male_healthy_patient, female_healthy_patient, healthy_patient)
# Call the function
