import numpy as np
import argparse
from custom_function import *
from glob import iglob
from collections import defaultdict
import scipy.ndimage
import scipy.io as sio
import sys
import os
import csv
from scipy.ndimage.interpolation import shift

def my_read_bin(cur_inp_file, data_type, input_shape):
  A = np.fromfile(cur_inp_file, dtype = data_type)
  A[np.isnan(A)] = 0
  A = np.reshape(A, input_shape)
  A = np.transpose(A, [2, 1, 0])
  return A

def center_to_def_loc(SA_rec, cur_loc, offset):
  SA_rec_sliced = SA_rec[:,:,cur_loc[2]+offset]
  sh_x = SA_rec_sliced.shape[1]//2 - cur_loc[0]
  sh_y = SA_rec_sliced.shape[0]//2 - cur_loc[1]
  SA_rec_sh = shift(SA_rec_sliced, [sh_y, sh_x], prefilter=False)
  return SA_rec_sh

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


pat_id_arr_fname = f'/data01/user-storage/y.zezhang/2024_subsample_project/document/zitong_patient_list/pat_id_diseased_v3.txt'
diseased_patients = np.loadtxt(pat_id_arr_fname, dtype = 'str', comments="#", delimiter=",", unpack=False)

pat_id_arr_fname = f'/data01/user-storage/y.zezhang/2024_subsample_project/document/zitong_patient_list/pat_id_healthy_v3.txt'
healthy_patients = np.loadtxt(pat_id_arr_fname, dtype = 'str', comments="#", delimiter=",", unpack=False)
#pat_id_arr_fname_def = '/data01/user-storage/y.zezhang/2024_subsample_project/document/zitong_patient_list/combined_v2_final_test_pat_list_def.txt'  # Replace with the path to your combined text file
#columns_def1,columns_def2,columns_def3 = read_columns_separately(pat_id_arr_fname_def)

#pat_id_arr_fname_hl = '/data01/user-storage/y.zezhang/2024_subsample_project/document/zitong_patient_list/combined_v2_final_test_pat_list_hl.txt'  # Replace with the path to your combined text file
#columns_hl1,columns_hl2,columns_hl3 = read_columns_separately(pat_id_arr_fname_hl)


#file_path = "patient_selection.txt"
#diseased_patients, healthy_patients = read_patient_file(file_path)
#diseased_patients, healthy_patients = columns_def1,columns_hl1


'''
file_path = "patient_selection.txt"
diseased_patients, healthy_patients = read_patient_file(file_path)
isIO=0

# Lists to hold patient IDs and codes
diseased_patient_ids = []
def_type_arr= []

# Process each entry in the list
for entry in diseased_patients:
    parts = entry.split()
    diseased_patient_ids.append(parts[0])
    def_type_arr.append(parts[1])
'''
Ud=32
#subsample_slice=10##########################################################
#subsample_slice=30##########################################################

location_setting=  ['a','i']
extent_setting =  [30,60] #[30,90,60] 
severity_setting=  [100,175,250] #[100,175,250]

location_setting_combined=   '_'.join(map(str,location_setting))
extent_setting_combined =   '_'.join(map(str,extent_setting))
severity_setting_combined=   '_'.join(map(str,severity_setting))

CT_category=['CTAC']

observer_study_list = os.listdir('/data01/user-storage/y.zezhang/2024_subsample_project/mod_SA_images')

def_folder='/data01/user-storage/y.zezhang/2024_subsample_project/mod_Neural_network_training/centroid_mask/testing'
base_folder = '/data01/user-storage/y.zezhang/2024_subsample_project/mod_SA_images'

#save_folder = f'{base_folder}/{subsample_slice}'
inp_shape = (48, 48, 48)
inp_shape_orig = (48, 48, 48)
isIO=0

for study_project in observer_study_list:
  
  save_folder = f'{base_folder}/{study_project}'
  sub_base_folder=os.path.join(base_folder,study_project)
  
  if not os.path.isdir(save_folder):
    os.mkdir(save_folder)
  #os.makedirs(save_folder, exist_ok=True)


  print('loading pre-written channels file...')
  if Ud == 32:
    U_flag = ''
  elif Ud == 64:
    U_flag = f'_{Ud}'

  U = np.load(f'U{U_flag}.npy')
  print('U shape: ',U.shape)
  U = np.transpose(U, [1,0])

  print(f'loading images... ')

  ff = {'diseased':defaultdict(list), 'healthy':defaultdict(list)}
  pat_ind_arr = {'diseased':diseased_patients, 'healthy':healthy_patients}

  for CT_method in CT_category:
    for diag in ['diseased', 'healthy']:
      status_folder=os.path.join(sub_base_folder,diag)
      subensemble_idx = 0
      for location in location_setting:
        for extent in extent_setting:
          for severity in severity_setting:          
            if diag == 'diseased':
              for  di_item in diseased_patients:
                
                
                patient=di_item
                def_type=f'd{location}21{extent}s{severity}'
                def_centroid_type=def_type.split('s')[0]
              
              
                cur_path=os.path.join(status_folder,patient)
                cur_path=os.path.join(cur_path,CT_method)
                cur_path=os.path.join(cur_path,def_type)
              
                SA_name=os.path.join(cur_path,'extended_reoriented_windowed.img')
                
                def_loc_path=os.path.join(def_folder,patient)
                def_loc_fname=def_loc_path +'/'+ 'def_centroid_' + def_centroid_type + '_mod.bin'
                
                SA_rec_base = my_read_bin(SA_name, 'float32', inp_shape_orig)    
                cur_loc = np.fromfile(def_loc_fname, dtype = 'float32').astype(int) - 1 #0 -based / but nn2D has 1 shift
                
                for offset in [7,8,9]:
                  SA_rec = center_to_def_loc(SA_rec_base, cur_loc, offset)
                  SA_rec = SA_rec[8:40,8:40]
                  if Ud != 32:
                    SA_rec = scipy.ndimage.zoom(SA_rec, Ud/32, order=0) # upsampling to 512X512
                  SA_rec = (SA_rec-np.min(SA_rec))/(np.max(SA_rec)-np.min(SA_rec))*255
                  SA_rec = SA_rec - np.mean(SA_rec) # remove zero frequency component
                  ff[diag][subensemble_idx].append(SA_rec.flatten())
                
                
                
            elif diag == 'healthy':
              for hl_index,hl_item in enumerate(healthy_patients):
                patient=hl_item
                def_type=f'd{location}21{extent}s{severity}'
                
                cur_path=os.path.join(status_folder,patient)
                cur_path=os.path.join(cur_path,CT_method)
                cur_path=os.path.join(cur_path,'hl')
          
                SA_name=os.path.join(cur_path,'extended_reoriented_windowed.img')
                
                def_loc_path=os.path.join(def_folder,patient)
                def_centroid_type=def_type.split('s')[0]
                def_loc_fname=def_loc_path +'/'+ 'def_centroid_' + def_centroid_type + '_mod.bin'
                
                SA_rec_base = my_read_bin(SA_name, 'float32', inp_shape_orig)    
                cur_loc = np.fromfile(def_loc_fname, dtype = 'float32').astype(int) - 1 #0 -based / but nn2D has 1 shift 
                
                for offset in [7,8,9]:
                  SA_rec = center_to_def_loc(SA_rec_base, cur_loc, offset)
                  SA_rec = SA_rec[8:40,8:40]
                  if Ud != 32:
                    SA_rec = scipy.ndimage.zoom(SA_rec, Ud/32, order=0) # upsampling to 512X512
                  SA_rec = (SA_rec-np.min(SA_rec))/(np.max(SA_rec)-np.min(SA_rec))*255
                  SA_rec = SA_rec - np.mean(SA_rec) # remove zero frequency component
                  ff[diag][subensemble_idx].append(SA_rec.flatten())
                
          #if isIO == 1:
          #  subensemble_idx += 1

          #if pat_ind == pat_ind_arr[diag][0]:
          #  pass

      
      

  #np.save(f'{root_folder}/SA_rec_d{location}21{extent}.npy', SA_rec)
  ###################################################################

  print('calculating test statistics...')
  tS_sum = []
  tN_sum = []


  # write txt


  tS, tN = MultiLDpooled(ff['diseased'][0],ff['healthy'][0],U,isIO)
  fname_tSN = f'{save_folder}/t_ZT_loc_{location_setting_combined}_sev_{severity_setting_combined}_ext_{extent_setting_combined}_subsample{study_project}_IO{isIO}_Ud{Ud}.txt'
  with open(fname_tSN, 'w') as f:
      f.writelines('Initial Line\nLarge\n')
      for dd in tN:
          f.writelines(f"{dd}\n")
      f.writelines('*\n')
      for dd in tS:
          f.writelines(f"{dd}\n")
      f.writelines('*')

  print('done')
