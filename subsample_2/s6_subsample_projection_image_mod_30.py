import os
import numpy as np
import shutil


def my_read_bin(cur_inp_file, data_type, input_shape):
  A = np.fromfile(cur_inp_file, dtype = data_type)
  A[np.isnan(A)] = 0
  A = np.reshape(A, input_shape)
  #A = np.transpose(A, [2, 1, 0])
  return A

def my_write_bin(cur_out_file, data_type, data):
  data = np.transpose(data, [2, 1, 0])
  data.astype(data_type).tofile(cur_out_file)
  return

def process_image_and_header_files(image_file, head_file, save_path, sample_rate, patient, image_file_name, head_file_name, subsample_slices):
    def my_read_bin(file_path, dtype, shape):
        data = np.fromfile(file_path, dtype=dtype)
        return data.reshape(shape)
    
    def my_write_bin(file_path, dtype, data):
        data.astype(dtype).tofile(file_path)
    
    # Read the binary image file into a matrix
    image_matrix = my_read_bin(image_file, np.float32, [30, 64, 64])
    
    # Subsample the first dimension of the matrix
    image_matrix_subsample = image_matrix[::sample_rate, :, :]
    
    # Define the output file path for the subsampled image
    cur_out_file = os.path.join(save_path, str(subsample_slices), patient, image_file_name)
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(cur_out_file), exist_ok=True)
    
    # Write the subsampled image matrix to the output file
    my_write_bin(cur_out_file, np.float32, image_matrix_subsample)
    
    # Define the destination file path for the header file
    dest_file_path = os.path.join(save_path, str(subsample_slices), patient, head_file_name)
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
    
    # Copy the header file to the destination folder
    shutil.copy(head_file, dest_file_path)
    
    # Modify the copied header file in the destination folder
    with open(dest_file_path, 'r') as file:
        lines = file.readlines()
    
    with open(dest_file_path, 'w') as file:
        for line in lines:
            if line.strip() == '!number of projections := 30':
                file.write(f'!number of projections := {subsample_slices}\n')
            elif line.strip() == '!total number of images := 30':
                file.write(f'!total number of images := {subsample_slices}\n')
            elif line.strip() == '!number of images/energy window := 30':
                file.write(f'!number of images/energy window := {subsample_slices}\n')
            elif line.strip() == 'image duration (sec) := 30.000':
                file.write(f'image duration (sec) := {subsample_slices}\n')
            else:
                file.write(line)


def process_CT_image_and_header_files(image_file, head_file, save_path, patient, image_file_name, head_file_name, subsample_slices):
    def my_read_bin(file_path, dtype, shape):
        data = np.fromfile(file_path, dtype=dtype)
        return data.reshape(shape)
    
    def my_write_bin(file_path, dtype, data):
        data.astype(dtype).tofile(file_path)
    
    # Read the binary image file into a matrix
    image_matrix = my_read_bin(image_file, np.float32, [128, 128, 128])
    

    # Define the output file path for the subsampled image
    cur_out_file = os.path.join(save_path, str(subsample_slices), patient, image_file_name)
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(cur_out_file), exist_ok=True)
    
    # Write the subsampled image matrix to the output file
    #image_matrix= np.transpose(image_matrix, [0, 2, 1])
    
    #image_matrix = np.flip(image_matrix, axis=2)
    
    my_write_bin(cur_out_file, np.float32, image_matrix)
    
    # Define the destination file path for the header file
    dest_file_path = os.path.join(save_path, str(subsample_slices), patient, head_file_name)
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
    
    # Copy the header file to the destination folder
    shutil.copy(head_file, dest_file_path)
       
    # Modify the copied header file in the destination folder
    with open(dest_file_path, 'r') as file:
        lines = file.readlines()
    
    with open(dest_file_path, 'w') as file:
        for line in lines:
            if line.strip() == ';# scaling factor (mm/pixel) [3] := 6.800':
                file.write('scaling factor (mm/pixel) [3] := 6.800\n')
            if line.strip() == '!name of data file := ct.ict':
                file.write(f'!name of data file := {image_file_name}\n')
            else:
                file.write(line)

                
                
extension=[30,60,90]
severity=['s100','s175','s250','s500']
location=['di','da']

subsample_slices_list=[30]
#subsample_slices=15
#sample_rate=int(30/subsample_slices)

# Example usage
folder_path = '/data01/user-storage/y.zezhang/2024_subsample_project/mod_subsample_projection/30' 
save_path='/data01/user-storage/y.zezhang/2024_subsample_project/mod_subsample_projection/30_reco'
#save_path='/data01/user-storage/y.zezhang/2024_subsample_project/mod_subsample_projection'
patient_list=os.listdir('/data01/user-storage/y.zezhang/2024_subsample_project/mod_subsample_projection/30/def') 

for subsample_slices in subsample_slices_list:
    sample_rate=int(30/subsample_slices)
    for patient in patient_list:
        hl_image_file_name=f'{patient}.a00'
        hl_head_file_name=f'{patient}.h00'
        image_file=f'{folder_path}/processed_hl/{hl_image_file_name}'
        head_file=f'{folder_path}/processed_hl/{hl_head_file_name}'
        
        process_image_and_header_files(image_file, head_file, save_path, sample_rate, patient, hl_image_file_name, hl_head_file_name, subsample_slices)
        

        
        for ext in extension:
            for sev in severity:
                for loc in location:
                    image_file_name=f'mod_proj_{loc}21{ext}{sev}_obj_{patient}_d1.a00'
                    head_file_name=f'mod_proj_{loc}21{ext}{sev}_obj_{patient}_d1.h00'
                    image_file=f'{folder_path}/def/{patient}/{image_file_name}'                
                    head_file=f'{folder_path}/def/{patient}/{head_file_name}'
                    
                    process_image_and_header_files(image_file, head_file, save_path, sample_rate, patient, image_file_name, head_file_name, subsample_slices)

                    
                        
        CT_image_file_name=f'ct.ict'
        CT_head_file_name=f'ct.hct'
        CT_image_file=f'{folder_path}/def/{patient}/{CT_image_file_name}'
        CT_head_file=f'{folder_path}/def/{patient}/{CT_head_file_name}'
        CT_image_file_name_save=f'{patient}_ct.ict'
        CT_head_file_name_save=f'{patient}_ct.hct'
        
        process_CT_image_and_header_files(CT_image_file, CT_head_file, save_path, patient, CT_image_file_name_save,  CT_head_file_name_save, subsample_slices)

        