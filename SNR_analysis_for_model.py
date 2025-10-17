import numpy as np
import argparse
#from custom_function import *
from glob import iglob
from collections import defaultdict
import scipy.ndimage
import scipy.io as sio
import sys
import os
import csv
from scipy.ndimage.interpolation import shift
import scipy.io
from scipy.io import savemat

def my_read_bin(cur_inp_file, data_type, input_shape):
  A = np.fromfile(cur_inp_file, dtype = data_type)
  A[np.isnan(A)] = 0
  A = np.reshape(A, input_shape)
  A = np.transpose(A, [2, 1, 0])
  return A

def my_write_bin(cur_out_file, data_type, data):
  #data = np.transpose(data, [2, 0, 1])
  data.astype(data_type).tofile(cur_out_file)
  return

def center_to_def_loc(SA_rec, cur_loc, offset):
  SA_rec_sliced = SA_rec[:,:,cur_loc[2]+offset]
  sh_x = SA_rec_sliced.shape[1]//2 - cur_loc[0]
  sh_y = SA_rec_sliced.shape[0]//2 - cur_loc[1]
  SA_rec_sh = shift(SA_rec_sliced, [sh_y, sh_x], prefilter=False)
  return SA_rec_sh


dl_version='_a2'
batch_size=32
dose_level=1
bt_size=32
lambda_val_ind_mdiff=0
lambda_val_ind_chdiff=6

Ud=32
isIO=0

location_setting=['i']  #['a','i']
extent_setting = [45]  #[30,45,60] 
severity_setting= [250] # [100,175,250]

base_folder = '/data01/user-storage/y.zezhang/data_for_zezhang_mar29'###############################################################################
root_folder = f'{base_folder}/learning/den_3d_v{dl_version}/pred'; #####################################################################################
root_folder_mirirv3 = f'{base_folder}/learning/den_3d_v{dl_version}/pred_mirirv3'########################################################################
root_folder_prev = f'{base_folder}/test_data_sa_wd';###################################################################################################################
root_folder_prev_mirirv3 = f'{base_folder}/test_data_mirirv3_sa_wd';######################################################################################################
save_folder = f'{base_folder}/SNR/den_3d_v{dl_version}/lmbd_mdiff{lambda_val_ind_chdiff}/d{dose_level}/'###########


#if not os.path.isdir(save_folder):
#  os.mkdir(save_folder)
os.makedirs(save_folder, exist_ok=True)

inp_shape = (48, 48, 48)
inp_shape_orig = (48, 48, 48)

# loading patient list
hl_pat_list_fname = f'{base_folder}/final_test_pat_list_hl.txt'
hl_pat_list = np.loadtxt(hl_pat_list_fname, dtype=str)

def_pat_list_fname = f'{base_folder}/final_test_pat_list_def.txt'
def_pat_list = np.loadtxt(def_pat_list_fname, dtype=str)

hl_pat_list_fname = f'{base_folder}/final_test_pat_list_hl_src.txt'
hl_pat_list_src = np.loadtxt(hl_pat_list_fname, dtype=str)

def_pat_list_fname = f'{base_folder}/final_test_pat_list_def_src.txt'
def_pat_list_src = np.loadtxt(def_pat_list_fname, dtype=str)

print('loading pre-written channels file...')
if Ud == 32:
    U_flag = ''
elif Ud == 64:
    U_flag = f'_{Ud}'

U = np.load(f'{base_folder}/U{U_flag}.npy')
print('U shape: ',U.shape)
U = np.transpose(U, [1,0])

print(f'loading images... || D: {dose_level}')
ff = {'diseased':defaultdict(list), 'healthy':defaultdict(list)}
pat_ind_arr = {'diseased':def_pat_list, 'healthy':hl_pat_list}
pat_ind_arr_src = {'diseased':def_pat_list_src, 'healthy':hl_pat_list_src}

def_name_arr = []
for diag in ['diseased', 'healthy']:
    for idx_list in range(len(pat_ind_arr[diag])):
      pat_ind = pat_ind_arr[diag][idx_list]
      src_name = pat_ind_arr_src[diag][idx_list]
      #print(pat_ind)
      subensemble_idx = 0
      for location in location_setting:
        for extent in extent_setting:
          for severity in severity_setting:
            if diag == 'diseased':
              def_name = f'd{location}21{extent}s{severity}'
              def_name_mod = ''
              centroid_fname_flag = '_mod'
            else:
              def_name = f'hl'
              def_name_mod = f'hl'
              centroid_fname_flag = '_mod_again3'

            if src_name == 'mirirv3':
              centroid_fname_flag = '_mod'
              root_folder_act = root_folder_mirirv3
              root_folder_prev_act = root_folder_prev_mirirv3
            else:
              root_folder_act = root_folder
              root_folder_prev_act = root_folder_prev
#######################
            def_name_arr.append(f'd{location}21{extent}s{severity}')
            SA_name = \
              f'{root_folder_act}/{def_name}/recon_pat{pat_ind}' + \
              f'_{def_name}_d{dose_level}_it8' + \
              f'_b{bt_size}_lmbdchdiff{lambda_val_ind_chdiff}_lmbdmdiff{lambda_val_ind_mdiff}.img'
              #f'_c30o5.img'
            def_loc_fname = \
              f'{root_folder_prev_act}/{pat_ind}/def_centroid_d{location}21{extent}{centroid_fname_flag}.bin'
            cur_loc = np.fromfile(def_loc_fname, dtype = 'float32').astype(int) - 1 #0 -based / but nn2D has 1 shift
############################
            
            SA_rec_base = my_read_bin(SA_name, 'float32', inp_shape_orig)
            #print(SA_rec.shape)
            for offset in [7,8,9]:
              SA_rec = center_to_def_loc(SA_rec_base, cur_loc, offset)
              SA_rec = SA_rec[8:40,8:40]
              if Ud != 32:
                SA_rec = scipy.ndimage.zoom(SA_rec, Ud/32, order=0) # upsampling to 512X512
              SA_rec = (SA_rec-np.min(SA_rec))/(np.max(SA_rec)-np.min(SA_rec))*255
              #SA_rec = SA_rec - np.mean(SA_rec) # remove zero frequency component ###############################################
              ff[diag][subensemble_idx].append(SA_rec.flatten())
            if isIO == 1:
              subensemble_idx += 1

  #np.save(f'{root_folder}/SA_rec_d{location}21{extent}.npy', SA_rec)
  ###################################################################

print('calculating test statistics...')
tS_sum = []
tN_sum = []


#print('sub-ensemble: '+str(i))
IS=ff['diseased'][0]
IN=ff['healthy'][0]
U=U
IO=isIO

tS = np.zeros(len(IS))
tN = np.zeros(len(IN))
IS = np.transpose(np.asmatrix(IS), [1,0]) # (262144,N)
IN = np.transpose(np.asmatrix(IN), [1,0])  # (262144,N)

vS = np.matmul(U,IS) # (5,N-1)
vN = np.matmul(U,IN) # (5,N)


delta_f_bar=np.mean(IS,axis=1)-np.mean(IN,axis=1)
delta_v_bar = np.matmul(U,np.mean(IS,axis=1)-np.mean(IN,axis=1)) # (5,262144)(262144,1) -> (5,1)

#delta_g_bar = np.matmul(U,np.mean(IS,axis=1)-np.mean(IN,axis=1)) # (5,262144)(262144,1) -> (5,1)
vData = np.concatenate((vS,vN),axis=1) # (5,2N-1)
K = np.cov(vData) # (5,5)

np.save(save_folder +'delta_f_bar_'+str(dl_version)+'_d'+str(dose_level)+'_location'+str(location_setting)+"_extent"+str(extent_setting)+'_severity'+str(severity_setting),delta_f_bar)
np.save(save_folder +"delta_v_bar_"+str(dl_version)+'_d'+str(dose_level)+'_location'+str(location_setting)+"_extent"+str(extent_setting)+'_severity'+str(severity_setting),delta_v_bar)
np.save(save_folder + "K_"+str(dl_version)+'_d'+str(dose_level)+'_location'+str(location_setting)+"_extent"+str(extent_setting)+'_severity'+str(severity_setting),K)
np.save(save_folder +'IS'+str(dl_version)+'_d'+str(dose_level)+'_location'+str(location_setting)+"_extent"+str(extent_setting)+'_severity'+str(severity_setting),np.mean(IS,axis=1))
np.save(save_folder +"IN"+str(dl_version)+'_d'+str(dose_level)+'_location'+str(location_setting)+"_extent"+str(extent_setting)+'_severity'+str(severity_setting),np.mean(IN,axis=1))

#savemat('delta_f_bar_'+str(dl_version)+'_d'+str(dose_level),delta_g_bar)
#savemat("vData_"+str(dl_version)+'_d'+str(dose_level),vData)
#savemat("K_"+str(dl_version)+'_d'+str(dose_level),K)
#,{"vData_"+str(dl_version)+'_d'+str(dose_level): vData },{"K_"+str(dl_version)+'_d'+str(dose_level): K }
mdic={'delta_f_bar_'+str(dl_version)+'_d'+str(dose_level): delta_f_bar,
      "delta_v_bar_"+str(dl_version)+'_d'+str(dose_level): delta_v_bar,
      "K_"+str(dl_version)+'_d'+str(dose_level): K,
      "IS_"+str(dl_version)+'_d'+str(dose_level): np.mean(IS,axis=1),
      "IN_"+str(dl_version)+'_d'+str(dose_level):np.mean(IN,axis=1) }
      

savemat(save_folder +'SNR_data'+str(dl_version)+'_d'+str(dose_level)+'_location'+str(location_setting)+"_extent"+str(extent_setting)+'_severity'+str(severity_setting)+'.mat', mdic)

