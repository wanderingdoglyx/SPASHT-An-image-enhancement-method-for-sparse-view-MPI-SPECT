import os
import shutil


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


file_path = "patient_selection.txt"
diseased_patients, healthy_patients = read_patient_file(file_path)
isIO=0
CT_category='CTAC'

# Lists to hold patient IDs and codes
diseased_patient_ids = []
def_type_arr= []

# Process each entry in the list
for entry in diseased_patients:
    parts = entry.split()
    diseased_patient_ids.append(parts[0])
    def_type_arr.append(parts[1])

nn_version='2s500'

subsample_slice=15
bench=32
lmbdchdiff=7
lmbdmdiff=0


location_setting=  ['a','i']
extent_setting =  [30,90,60] 
severity_setting=   [100,175,250,500]

def_folder='/data01/user-storage/y.zezhang/data_for_zezhang_mar29/test_data_mirirv3_sa_wd'
sa_base=f'/data01/user-storage/y.zezhang/2024_subsample_project/mod_Neural_network_training/learning/subsample_3d_v{nn_version}/pred'
save_folder = f'/data01/user-storage/y.zezhang/2024_subsample_project/mod_SA_images/subsample_3d_v{nn_version}_d{subsample_slice}_lmbdchdiff{lmbdchdiff}_nn'


for diag in ['diseased', 'healthy']:
    
    status_folder=os.path.join(save_folder,diag)
    subensemble_idx = 0
    
    if not os.path.exists(status_folder):
        os.makedirs(status_folder)
    for location in location_setting:
        for extent in extent_setting:
          for severity in severity_setting:
            for index, di_item in enumerate(diseased_patients):
                if diag == 'diseased':
                    for index, di_item in enumerate(diseased_patients):
                        
                        
                        patient=diseased_patient_ids[index]
                        def_type= f'd{location}21{extent}s{severity}'
                        def_centroid_type=def_type.split('s')[0]
                    
                    
                        cur_path=os.path.join(sa_base,def_type)
                        #cur_path=os.path.join(cur_path,def_type)
                    
                        SA_fname='recon_pat'+ patient +'_'+def_type+'_d'+str(subsample_slice)+'_it8_b'+str(bench)+'_lmbdchdiff'+str(lmbdchdiff)+'_lmbdmdiff'+str(lmbdmdiff)+'.img'
                        SA_name=os.path.join(cur_path,SA_fname)
                        
                        
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
                    
                    
                        cur_path=os.path.join(sa_base,'hl')
                        
                    
                        SA_fname='recon_pat'+ patient +'_'+'hl'+'_d'+str(subsample_slice)+'_it8_b'+str(bench)+'_lmbdchdiff'+str(lmbdchdiff)+'_lmbdmdiff'+str(lmbdmdiff)+'.img'
                        SA_name=os.path.join(cur_path,SA_fname)
                        
                        
                        save_subfolder=os.path.join(status_folder,patient)
                        save_subfolder=os.path.join(save_subfolder,CT_category)
                        save_subfolder=os.path.join(save_subfolder,'hl')
                        
                        dest_path=save_subfolder+'/'+'extended_reoriented_windowed.img'
                        
                        if not os.path.exists(save_subfolder):
                            os.makedirs(save_subfolder)
                            
                        shutil.copy(SA_name, dest_path)
