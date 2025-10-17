import os
import shutil

def copy_files_with_patterns(src_folder, dest_folder, patterns,patient):
    """
    Copy files from src_folder to dest_folder if they match any of the given patterns.
    
    Parameters:
    src_folder (str): Source folder to search for files.
    dest_folder (str): Destination folder to copy files to.
    patterns (list of str): List of filename patterns to match.
    """
    finally_des_path=os.path.join(dest_folder,patient)
    
    if not os.path.exists(finally_des_path):
        os.makedirs(finally_des_path)

    for root, dirs, files in os.walk(src_folder):
        for file in files:
            if any(pattern in file for pattern in patterns):
                src_file = os.path.join(root, file)
                dest_file = os.path.join(finally_des_path, file)
                shutil.copy(src_file, dest_file)
                print(f'Copied: {src_file} to {dest_file}')
                
    ct_fname=src_folder+'/ct.ict'
    ct_head_fname=src_folder+'/ct.hct'
    CDRP_fname=src_folder+'/CDRP.par'
    
    des_ct_fname=finally_des_path+'/ct.ict'
    des_ct_head_fname=finally_des_path+'/ct.hct'
    des_CDRP=finally_des_path+'/CDRP.par'
                
    shutil.copy(ct_fname, des_ct_fname)
    shutil.copy(ct_head_fname, des_ct_head_fname)
    shutil.copy(CDRP_fname, des_CDRP)


# Example usage
source_folder = '/data03/user-storage/y.zezhang/Ashequr/data_spie_v2/train_mc_castor'
destination_folder = '/data01/user-storage/y.zezhang/2024_subsample_project/mod_subsample_projection/30/training_de_def'
file_patterns = ['d1.a00', 'd1.h00']

patient_list=os.listdir('/data01/user-storage/y.zezhang/demist/train_mc_castor_mirirv12_apr3') 

for patient in patient_list:
    sub_source_folder=source_folder+'/'+patient+'/mod_proj'
    copy_files_with_patterns(sub_source_folder, destination_folder, file_patterns,patient)