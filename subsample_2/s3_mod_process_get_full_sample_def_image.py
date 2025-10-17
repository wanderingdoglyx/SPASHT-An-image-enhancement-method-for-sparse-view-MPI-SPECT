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

def copy_specific_files(src_dir, dst_dir,filename,patient):
    # Create the destination directory if it doesn't exist
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    # Counter for renaming files
    #file_counter = 1

    # Iterate over all files in the source directory
    # for filename in os.listdir(src_dir):
        # Check if the filename contains the specified strings
        #if all(x in filename for x in ["d1.a00", "s175"]) and ("da" in filename or "di" in filename):
            # Construct the full file path
    src_file = os.path.join(src_dir, filename)
    
    # Generate new filename
    new_filename = f"mod_proj_{loc}21{ext}{sev}_obj_{patient}_d1.a00"
    
    dst_file = os.path.join(dst_dir,patient ,new_filename)
    
    # Copy the file to the destination directory
    shutil.copy2(src_file, dst_file)
    print(f"Copied {src_file} to {dst_file}")
    
   
# Example usage
source_folder = '/data01/user-storage/y.zezhang/data_from_zitong_real_patient_project/mod_prj'
destination_folder = '/data01/user-storage/y.zezhang/2024_subsample_project/mod_subsample_projection/30/def'
file_patterns = ['d1.a00', 'd1.h00']

patient_list=os.listdir('/data01/user-storage/y.zezhang/data_for_zezhang_mar29/test_data_mirirv3_sa_wd') 


for patient in patient_list:
    sub_source_folder=source_folder+'/'+patient+'/mod_proj'
    copy_files_with_patterns(sub_source_folder, destination_folder, file_patterns,patient)
    

# add 500 serverity
source_folder = '/data01/user-storage/y.zezhang/data_from_zitong_real_patient_project/mod_prj_v2'
destination_folder = '/data01/user-storage/y.zezhang/2024_subsample_project/mod_subsample_projection/30/def'

#patient_list=os.listdir('/data01/user-storage/y.zezhang/data_for_zezhang_mar29/test_data_mirirv3_sa_wd') 

extension=[30,60,90]
#severity=['s100','s175','s250']
severity=['s500']
location=['di','da']

for patient in patient_list:
    for ext in extension:
        for sev in severity:
            for loc in location:
    
                #sub_source_folder=source_folder+'/'+patient
                sub_source_folder=source_folder+'/'+patient
                filename=f'mp_{loc}21{ext}{sev}_obj_{patient}_d1.a00'
                copy_specific_files(sub_source_folder,destination_folder,filename,patient)