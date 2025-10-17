import os
import numpy as np
import shutil

# Example usage
folder_path = '/data01/user-storage/y.zezhang/data_from_zitong_real_patient_project/mod_prj' 
save_path='/data01/user-storage/y.zezhang/2024_subsample_project/subsample_projection'


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
                file.write('!number of projections := 10\n')
            elif line.strip() == '!total number of images := 30':
                file.write('!total number of images := 10\n')
            elif line.strip() == '!number of images/energy window := 30':
                file.write('!number of images/energy window := 10\n')
            elif line.strip() == 'image duration (sec) := 30.000':
                file.write('image duration (sec) := 10.000\n')
            else:
                file.write(line)


def process_CT_image_and_header_files(image_file, head_file, save_path, patient, image_file_name, head_file_name, subsample_slices):
    def my_read_bin(file_path, dtype, shape):
        data = np.fromfile(file_path, dtype=dtype)
        return data.reshape(shape)
    
    def my_write_bin(file_path, dtype, data):
        data.astype(dtype).tofile(file_path)
    
    # Read the binary image file into a matrix
    image_matrix = my_read_bin(image_file, np.float32, [64, 64, 64])
    

    # Define the output file path for the subsampled image
    cur_out_file = os.path.join(save_path, str(subsample_slices), patient, image_file_name)
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(cur_out_file), exist_ok=True)
    
    # Write the subsampled image matrix to the output file
    image_matrix= np.transpose(image_matrix, [0, 2, 1])
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
            else:
                file.write(line)

                
                
extension=[30,60,90]
severity=['s100','s175','s250']
location=['di','da']

subsample_slices=15
sample_rate=int(30/subsample_slices)

patient_list=os.listdir('/data01/user-storage/y.zezhang/data_from_zitong_real_patient_project/mod_prj') 


for patient in patient_list:
    image_file_name='out_hl_obj_tot_w1.a00'
    head_file_name='out_hl_obj_tot_w1.h00'
    image_file=f'{folder_path}/{patient}/{image_file_name}'
    head_file=f'{folder_path}/{patient}/{head_file_name}'
    
    process_image_and_header_files(image_file, head_file, save_path, sample_rate, patient, image_file_name, head_file_name, subsample_slices)
    
   
    
    CT_image_file_name='out_hl_obj.ict'
    CT_head_file_name='out_hl_obj.hct'
    CT_image_file=f'{folder_path}/{patient}/{CT_image_file_name}'
    CT_head_file=f'{folder_path}/{patient}/{CT_head_file_name}'
    
    process_CT_image_and_header_files(CT_image_file, CT_head_file, save_path,patient, CT_image_file_name, CT_head_file_name, subsample_slices)

    
    
    '''   
    image_matrix=my_read_bin(image_file, np.float32, [30,64,64])
    image_matrix_subsample=image_matrix[::sample_rate, :, :]
    
    cur_out_file= f'{save_path}/{subsample_slices}/{patient}/{image_file_name}'
    my_write_bin(cur_out_file, np.float32, image_matrix_subsample)
    
    # Copy the file to the destination folder
    dest_file_path=f'{save_path}/{subsample_slices}/{patient}/{head_file_name}'
    shutil.copy(head_file, dest_file_path)
    
    # Modify the file in the destination folder
    with open(dest_file_path, 'r') as file:
        lines = file.readlines()
    
    with open(dest_file_path, 'w') as file:
        for line in lines:
            if line.strip() == '!number of projections := 30':
                file.write('!number of projections := 10\n')
            elif line.strip() == '!total number of images := 30':
                file.write('!total number of images := 10\n')
            elif line.strip() == '!number of images/energy window := 30':
                file.write('!number of images/energy window := 10\n')
            elif line.strip() == 'image duration (sec) := 30.000':
                file.write('image duration (sec) := 10.000\n')
            else:
                file.write(line)
    '''
    
    for ext in extension:
        for sev in severity:
            for loc in location:
                image_file_name=f'out_{loc}21{ext}{sev}_obj_tot_w1.a00'
                head_file_name=f'out_{loc}21{ext}{sev}_obj_tot_w1.h00'
                image_file=f'{folder_path}/{patient}/{image_file_name}'                
                head_file=f'{folder_path}/{patient}/{head_file_name}'
                
                process_image_and_header_files(image_file, head_file, save_path, sample_rate, patient, image_file_name, head_file_name, subsample_slices)

                
                    
                CT_image_file_name=f'out_{loc}21{ext}{sev}_obj.ict'
                CT_head_file_name=f'out_{loc}21{ext}{sev}_obj.hct'
                CT_image_file=f'{folder_path}/{patient}/{CT_image_file_name}'
                CT_head_file=f'{folder_path}/{patient}/{CT_head_file_name}'
                
                process_CT_image_and_header_files(CT_image_file, CT_head_file, save_path, patient, CT_image_file_name, CT_head_file_name, subsample_slices)

                
                            
                
         
#