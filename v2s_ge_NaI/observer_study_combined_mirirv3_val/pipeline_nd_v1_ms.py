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

def run_cho(Ud, dose_level, isIO):

  base_folder = '/data/rahman.m/projects/dl_denoising/debug/db_defect_insertion/data_spie/'
  root_folder = f'{base_folder}/test_data_sa_wd_fix2_48cube' #change: 2/6/23
  root_folder_mirirv3 = f'{base_folder}/test_data_mirirv3_sa_wd_48cube' #change: 2/6/23
  root_folder_prev = f'{base_folder}/test_data_sa_wd'
  root_folder_mirirv3_prev = f'{base_folder}/test_data_mirirv3_sa_wd' #change: 2/6/23
  save_folder = f'{base_folder}/val_data_sa_wd_tSN_fix3_remsev500ext90addsev175_combined_mirirv3_48cube' #change: 2/6/23
  if not os.path.isdir(save_folder):
    os.mkdir(save_folder)

  inp_shape = (48, 48, 48) #change: 2/6/23
  inp_shape_orig = (48, 48, 48)  #change: 2/6/23

  # loading patient list
  hl_pat_list_fname = f'{base_folder}/final_val_pat_list_hl_split.txt'
  hl_pat_list = np.loadtxt(hl_pat_list_fname, dtype=str)

  def_pat_list_fname = f'{base_folder}/final_val_pat_list_def_split.txt'
  def_pat_list = np.loadtxt(def_pat_list_fname, dtype=str)

  hl_pat_list_fname = f'{base_folder}/final_val_pat_list_hl_src_split.txt'
  hl_pat_list_src = np.loadtxt(hl_pat_list_fname, dtype=str)

  def_pat_list_fname = f'{base_folder}/final_val_pat_list_def_src_split.txt'
  def_pat_list_src = np.loadtxt(def_pat_list_fname, dtype=str)

  print('loading pre-written channels file...')
  if Ud == 32:
    U_flag = ''
  elif Ud == 64:
    U_flag = f'_{Ud}'

  U = np.load(f'{base_folder}/dependencies/observer_study_ZT/U{U_flag}.npy')
  print('U shape: ',U.shape)
  U = np.transpose(U, [1,0])

  print(f'loading images... || D: {dose_level}')
  ff = {'diseased':defaultdict(list), 'healthy':defaultdict(list)}
  pat_ind_arr = {'diseased':def_pat_list, 'healthy':hl_pat_list}
  pat_ind_arr_src = {'diseased':def_pat_list_src, 'healthy':hl_pat_list_src}

  def_name_arr = []
  for diag in ['diseased', 'healthy']:
    for idx_list in range(len(pat_ind_arr[diag])):
    #for pat_ind in pat_ind_arr[diag]:
      pat_ind = pat_ind_arr[diag][idx_list]
      src_name = pat_ind_arr_src[diag][idx_list]
      #print(pat_ind)
      subensemble_idx = 0
      for location in ['a','i']:
        for extent in [30,60]:
          for severity in [100,175,250]:
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
              root_folder_prev_act = root_folder_mirirv3_prev #change: 2/6/23
            else:
              root_folder_act = root_folder
              root_folder_prev_act = root_folder_prev
  

            def_name_arr.append(f'd{location}21{extent}s{severity}')
            SA_name = \
              f'{root_folder_act}/{pat_ind}/{def_name}/recon_pat{pat_ind}' + \
              f'_d{dose_level}_it8' + \
              f'_c30o5.img'
            def_loc_fname = \
              f'{root_folder_prev_act}/{pat_ind}/def_centroid_d{location}21{extent}{centroid_fname_flag}.bin'
            cur_loc = np.fromfile(def_loc_fname, dtype = 'float32').astype(int) - 1 #0 -based / but nn2D has 1 shift

            
            SA_rec_base = my_read_bin(SA_name, 'float32', inp_shape_orig)
            for offset in [7,8,9]: #change: 2/6/23 because added 16 more slices in z direction, cs shifted by 8
              SA_rec = center_to_def_loc(SA_rec_base, cur_loc, offset)
              SA_rec = SA_rec[8:40,8:40]
              if Ud != 32:
                SA_rec = scipy.ndimage.zoom(SA_rec, Ud/32, order=0) # upsampling to 512X512
              SA_rec = (SA_rec-np.min(SA_rec))/(np.max(SA_rec)-np.min(SA_rec))*255
              SA_rec = SA_rec - np.mean(SA_rec) # remove zero frequency component
              ff[diag][subensemble_idx].append(SA_rec.flatten())
            if isIO == 1:
              subensemble_idx += 1

            if pat_ind == pat_ind_arr[diag][0]:
              pass
              #my_write_bin(f'{root_folder}/SA_rec_d{location}21{extent}.npy', 'float32', SA_rec)
  ###################################################################

  print('calculating test statistics...')
  tS_sum = []
  tN_sum = []


  # write txt
  if isIO == 1:
    for i in range(subensemble_idx):
      print('sub-ensemble: '+str(i))
      tS, tN = MultiLDpooled(ff['diseased'][i],ff['healthy'][i],U,isIO)
      tS_sum.append(tS);
      tN_sum.append(tN);

  if isIO == 1:
    tS_sum = np.concatenate(tS_sum)
    tN_sum = np.concatenate(tN_sum)
    fname_tSN = f'{save_folder}/tSN_seall_d{dose_level}_c30o5_IO{isIO}_Ud{Ud}.txt'
    with open(fname_tSN, 'w') as f:
      f.writelines('Initial Line\nLarge\n')
      for dd in tN_sum:
          f.writelines(f"{dd}\n")
      f.writelines('*\n')
      for dd in tS_sum:
          f.writelines(f"{dd}\n")
      f.writelines('*')
  else:
    tS, tN = MultiLDpooled(ff['diseased'][0],ff['healthy'][0],U,isIO)
    fname_tSN = f'{save_folder}/tSN_seall_d{dose_level}_c30o5_IO{isIO}_Ud{Ud}.txt'
    with open(fname_tSN, 'w') as f:
      f.writelines('Initial Line\nLarge\n')
      for dd in tN:
          f.writelines(f"{dd}\n")
      f.writelines('*\n')
      for dd in tS:
          f.writelines(f"{dd}\n")
      f.writelines('*')

  print('done')

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--Ud', type=int, help="Ch dim")
  parser.add_argument('--dose_level', type=int, help="dose_level")
  parser.add_argument('--isIO', type=int, help="is IO?")
  args = parser.parse_args()
  run_cho(args.Ud, args.dose_level, args.isIO)
