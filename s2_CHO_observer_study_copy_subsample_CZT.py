import os
import shutil
import numpy as np

def read_patient_file(file_path):
    """
    Reads the patient selection file and returns the lists of diseased and healthy patients.

    Parameters:
    file_path (str): The path to the patient selection text file.

    Returns:
    Tuple[List[str], List[str]]: A tuple containing two lists: one for diseased patients and one for healthy patients.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    diseased_patients = []
    healthy_patients = []
    is_diseased = False
    is_healthy = False

    for line in lines:
        line = line.strip()
        if line == "Selected diseased patients:":
            is_diseased = True
            is_healthy = False
        elif line == "Selected healthy patients:":
            is_diseased = False
            is_healthy = True
        elif is_diseased:
            if line:
                diseased_patients.append(line)
        elif is_healthy:
            if line:
                healthy_patients.append(line)

    return diseased_patients, healthy_patients

def read_columns_separately(file_path):
    # Initialize empty lists to store each column's values
    first_column = []
    second_column = []
    third_column = []

    # Open the file and read its content
    with open(file_path, 'r') as file:
        lines = file.readlines()

        # Iterate over each line in the file
        for line in lines:
            # Split the line by the tab character (or other delimiter)
            columns = line.strip().split('\t')

            # Ensure the line has at least three columns
            if len(columns) >= 3:
                # Append each column value to the corresponding list
                first_column.append(columns[0])
                second_column.append(columns[1])
                third_column.append(columns[2])

    return first_column, second_column, third_column


#output_file_czt_def = '/data01/user-storage/y.zezhang/2024_subsample_project/document/collimator_record/czt_testing_patients_def.txt'   # Output file for the first half of patients
#output_file_czt_hl = '/data01/user-storage/y.zezhang/2024_subsample_project/document/collimator_record/czt_testing_patients_hl.txt'  # Output file for the second half of patients
#output_file_nai_def = '/data01/user-storage/y.zezhang/2024_subsample_project/document/collimator_record/nai_testing_patients_def.txt'   # Output file for the first half of patients
#output_file_nai_hl = '/data01/user-storage/y.zezhang/2024_subsample_project/document/collimator_record/nai_testing_patients_hl.txt'  # Output file for the second half of patients


pat_id_arr_fname = f'/data01/user-storage/y.zezhang/2024_subsample_project/document/collimator_record/patients_with_CZT_def.txt' 
diseased_patients = np.loadtxt(pat_id_arr_fname, dtype = 'str', comments="#", delimiter=",", unpack=False)

pat_id_arr_fname = f'/data01/user-storage/y.zezhang/2024_subsample_project/document/collimator_record/patients_with_CZT_hl.txt'
healthy_patients = np.loadtxt(pat_id_arr_fname, dtype = 'str', comments="#", delimiter=",", unpack=False)
#file_path = "patient_selection.txt"
#diseased_patients, healthy_patients = read_patient_file(file_path)

#diseased_patients, healthy_patients = columns_def1,columns_hl1
isIO=0
CT_category='CTAC'

'''
# Lists to hold patient IDs and codes
diseased_patient_ids = []
def_type_arr= []

# Process each entry in the list
for entry in diseased_patients:
    parts = entry.split()
    diseased_patient_ids.append(parts[0])
    def_type_arr.append(parts[1])
'''
location_setting=  ['a','i']
extent_setting =  [30,90,60] 
severity_setting=   [100,175,250]
subsample_level=['5','10','15']

def_folder='/data01/user-storage/y.zezhang/2024_subsample_project/mod_Neural_network_training/centroid_mask/ge_total'
#sa_base='/data01/user-storage/y.zezhang/2024_subsample_project/mod_Neural_network_training/30/ge_total'
#save_folder = '/data01/user-storage/y.zezhang/2024_subsample_project/mod_SA_images_ge/30'

for sp in subsample_level:
    sa_base=f'/data01/user-storage/y.zezhang/2024_subsample_project/mod_Neural_network_training/{sp}/ge_total'
    save_folder = f'/data01/user-storage/y.zezhang/2024_subsample_project/mod_SA_images_ge/{sp}'

    for diag in ['diseased', 'healthy']:
        
        status_folder=os.path.join(save_folder,diag)
        subensemble_idx = 0
        
        if not os.path.exists(status_folder):
            os.makedirs(status_folder)

                #for index, di_item in enumerate(diseased_patients):
        if diag == 'diseased':
            for location in location_setting:
                for extent in extent_setting:
                    for severity in severity_setting:
                        for di_item in diseased_patients:
                            
                            
                            patient=di_item
                            def_type=f'd{location}21{extent}s{severity}'
                            def_centroid_type=def_type.split('s')[0]
                        
                        
                            cur_path=os.path.join(sa_base,patient)
                            cur_path=os.path.join(cur_path,'CTAC',def_type)
                        
                            #SA_fname='recon_pat'+ patient +'_d1_it8_c30o5.img'
                            SA_fname='reoriented_windowed.img'
                            SA_name=os.path.join(cur_path,SA_fname)
                            
                            if not os.path.exists(SA_name):
                                print(f"File for {SA_name} does not exist, skipping.")
                                continue  # Skip to the next county
                            
                            
                            save_subfolder=os.path.join(status_folder,patient)
                            save_subfolder=os.path.join(save_subfolder,CT_category)
                            save_subfolder=os.path.join(save_subfolder,def_type)
                            
                            dest_path=save_subfolder+'/'+'extended_reoriented_windowed.img'
                            
                            if not os.path.exists(save_subfolder):
                                os.makedirs(save_subfolder)
                                
                                
                            shutil.copy(SA_name, dest_path)
                            
                            
                            
        elif diag == 'healthy':
            for hl_item in healthy_patients:
                
                            patient=hl_item
                            
                        #  SA_name=os.path.join(cur_path,'extended_reoriented_windowed.img')
                            
                            def_type=f'd{location}21{extent}s{severity}'
                            def_centroid_type=def_type.split('s')[0]
                        
                        
                            cur_path=os.path.join(sa_base,patient)
                            cur_path=os.path.join(cur_path,'CTAC','hl')
                        
                            #SA_fname='recon_pat'+ patient +'_d1_it8_c30o5.img'
                            SA_fname='reoriented_windowed.img'
                            SA_name=os.path.join(cur_path,SA_fname)
                            
                            if not os.path.exists(SA_name):
                                print(f"File for {SA_name} does not exist, skipping.")
                                continue  # Skip to the next county
                            
                            save_subfolder=os.path.join(status_folder,patient)
                            save_subfolder=os.path.join(save_subfolder,CT_category)
                            save_subfolder=os.path.join(save_subfolder,'hl')
                            
                            dest_path=save_subfolder+'/'+'extended_reoriented_windowed.img'
                            
                            if not os.path.exists(save_subfolder):
                                os.makedirs(save_subfolder)
                                
                            shutil.copy(SA_name, dest_path)


