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

Ud=64
subsample_slice=10##########################################################
#subsample_slice=30##########################################################
CT_category=['CTAC']

def_folder='/data01/user-storage/y.zezhang/data_for_zezhang_mar29/test_data_mirirv3_sa_wd'
base_folder = '/data01/user-storage/y.zezhang/2024_subsample_project/mod_SA_images'
save_folder = f'{base_folder}/{subsample_slice}'



#if not os.path.isdir(save_folder):
#  os.mkdir(save_folder)
os.makedirs(save_folder, exist_ok=True)

inp_shape = (48, 48, 48)
inp_shape_orig = (48, 48, 48)



print('loading pre-written channels file...')
if Ud == 32:
  U_flag = ''
elif Ud == 64:
  U_flag = f'_{Ud}'

U = np.load(f'U{U_flag}.npy')
print('U shape: ',U.shape)
U = np.transpose(U, [1,0])

print(f'loading images... || slice number: {subsample_slice}')

ff = {'diseased':defaultdict(list), 'healthy':defaultdict(list)}
pat_ind_arr = {'diseased':diseased_patients, 'healthy':healthy_patients}

for CT_method in CT_category:
  for diag in ['diseased', 'healthy']:
    status_folder=os.path.join(base_folder,diag)
    subensemble_idx = 0
    if diag == 'diseased':
      for index, di_item in enumerate(diseased_patients):
        
        
        patient=diseased_patient_ids[index]
        def_type=def_type_arr[index]
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
      for hl_item in healthy_patients:
        patient=hl_item
        
        cur_path=os.path.join(status_folder,patient)
        cur_path=os.path.join(cur_path,CT_method)
        cur_path=os.path.join(cur_path,'hl')
  
        SA_name=os.path.join(cur_path,'extended_reoriented_windowed.img')
        
        def_loc_path=os.path.join(def_folder,patient)
        def_loc_fname=def_loc_path +'/'+ 'def_centroid_' + 'da2190' + '_mod.bin'
        
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
fname_tSN = f'{save_folder}/t_subsample{subsample_slice}_IO{isIO}_Ud{Ud}.txt'
with open(fname_tSN, 'w') as f:
    f.writelines('Initial Line\nLarge\n')
    for dd in tN:
        f.writelines(f"{dd}\n")
    f.writelines('*\n')
    for dd in tS:
        f.writelines(f"{dd}\n")
    f.writelines('*')

print('done')



