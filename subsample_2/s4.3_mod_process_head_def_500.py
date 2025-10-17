import os
import numpy as np
import shutil


                

# Example usage
folder_path = '/data01/user-storage/y.zezhang/2024_subsample_project/mod_subsample_projection/30/def' 
save_path='/data01/user-storage/y.zezhang/2024_subsample_project/mod_subsample_projection/30/def'
patient_list=os.listdir('/data01/user-storage/y.zezhang/2024_subsample_project/mod_subsample_projection/30/def') 

location=['da','di']
extent=['30','60','90']


for ext in extent:
    for loc in location:
        for patient in patient_list:
            
            hl_head_file_name=f'mod_proj_{loc}21{ext}s100_obj_{patient}_d1.h00'
            
            head_file=f'{folder_path}/{patient}/{hl_head_file_name}'
            
            # Copy the header file to the destination folder
            new_head_file_name=f'mod_proj_{loc}21{ext}s500_obj_'+patient+'_d1.h00'
            dest_file_path = os.path.join(save_path,patient,new_head_file_name)
            shutil.copy(head_file, dest_file_path)
            
            # Modify the copied header file in the destination folder
            with open(dest_file_path, 'r') as file:
                lines = file.readlines()
            
            with open(dest_file_path, 'w') as file:
                for line in lines:
                    if line.strip() == f'!name of data file := mod_proj_{loc}21{ext}s100_obj_{patient}_d1.a00':
                        file.write(f'!name of data file := mod_proj_{loc}21{ext}s500_obj_{patient}_d1.a00\n')
                    elif line.strip() == f'patient name := SMC_mod_proj_{loc}21{ext}s100_obj_{patient}_d1.a00':
                        file.write(f'patient name := SMC_mod_proj_{loc}21{ext}s500_obj_{patient}_d1.a00\n')
                    else:
                        file.write(line)

    

