#=============================================================================================================================
## Import Libraries  ##
#=============================================================================================================================
import sys, os
from pathlib import Path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
import numpy as np
import h5py
import time
import argparse
import tensorflow as tf
from tensorflow.python.framework.ops import disable_eager_execution
#disable_eager_execution()

from tensorflow.keras import backend as K
K.set_image_data_format('channels_last')
from tensorflow.keras import Model
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import plot_model
from tensorflow.keras.callbacks import Callback, ReduceLROnPlateau, ModelCheckpoint, CSVLogger
import scipy.io as sio
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split,KFold
from tensorflow.keras.layers import Input, Conv3D, Conv3DTranspose, MaxPooling3D, Dropout, BatchNormalization, concatenate, Add, Activation, LeakyReLU
from tensorflow.keras.activations import softmax
from tensorflow.keras.initializers import Constant

#import network model
from Den3D_Model_AR_v1_Loop import build_dennet3D_pred


def my_write_bin(cur_out_file, data_type, data):
  data = np.transpose(data, [2, 1, 0])
  data.astype(data_type).tofile(cur_out_file)
  return
def my_read_bin(cur_inp_file, data_type, input_shape):
  A = np.fromfile(cur_inp_file, dtype = data_type)
  A[np.isnan(A)] = 0
  A = np.reshape(A, input_shape)
  A = np.transpose(A, [2, 1, 0, 3])
  return A


#=============================================================================================================================
## Define training protocols  ##
#=============================================================================================================================
def test_seg3D(base_folder, weights_name, loss_fn_name, subsample_level, num_iter, bt_size, num_epochs, learning_folder,
                lambda_val_ind_chdiff, lambda_val_ind_mdiff, def_name):
  #mod_proj_da2130s100_obj_02943705_d5_it8
  #def_name = f'd{def_loc}21{def_ext}s{def_sev}'
  #-----------------------------------------------------------
  # Step-1: Data pre-processing
  #----------------------------------------------------------
  lambda_val_arr_chdiff = [0, 1e-3, 5e-3, 1e-2, 5e-2, 1e-1, 3e-1, 1e0, 5e0, 1e1]
  lambda_val_arr_mdiff = [0, 1e-1, 5e-1, 1e0, 5e0, 1e1, 3e1, 1e2, 5e2, 1e3]
  lambda_val_chdiff = lambda_val_arr_chdiff[lambda_val_ind_chdiff]
  lambda_val_mdiff = lambda_val_arr_mdiff[lambda_val_ind_mdiff]
  print(f'lambda_val_chdiff: {lambda_val_chdiff}')
  print(f'lambda_val_mdiff: {lambda_val_mdiff}')

  #data_folder = f'{base_folder}/test_data_sa_wd_fix2_48cube'  ##########################################################
  data_folder = f'{base_folder}/{subsample_level}/ge_total'
  #data_folder=f'{base_folder}/training_data_sa_wd_fix2_48cube'
  mod_data_folder = f'{base_folder}/learning/{learning_folder}'  ##########################################################
  label_data_folder=f'{base_folder}/30/ge_total'

  # load protocols
  subsample_level_max = 30
  num_z_slice = 64
  num_reg = 1
  Nx_in, Ny_in, Nz_in = 48, 48, 48
  num_input_channels = 1
  num_output_channels = num_reg
  Nx_out, Ny_out, Nz_out = 48, 48, 48

  input_shape = (Nx_in, Ny_in, Nz_in, num_input_channels)
  input_shape_orig = (Nz_in, Ny_in, Nx_in, num_input_channels)
  output_shape = (Nx_out, Ny_out, Nz_out, num_output_channels)
  output_shape_orig = (Nz_out, Ny_out, Nx_out, num_output_channels)

  num_test_dict = {
        'hl': {
                'start_ind': 0,
                'end_ind': 204,
              }
      }
  num_test_hl = num_test_dict['hl']['end_ind'] - num_test_dict['hl']['start_ind'] + 1
  #num_test_def = num_test_dict['def']['end_ind'] - num_test_dict['def']['start_ind'] + 1
  num_test = num_test_hl
  X_test = np.zeros((num_test,) + input_shape)
  print("X_test allocated")
  Y_test = np.zeros((num_test,) + output_shape)
  print("Y_test allocated")

  
  pat_id_arr_fname = f'/data01/user-storage/y.zezhang/2024_subsample_project/document/collimator_record/patients_with_CZT.txt'
  pat_id_arr = np.loadtxt(pat_id_arr_fname, dtype = 'str', comments="#", delimiter=",", unpack=False)

  
  j = 0
  sc_data = 255
  for hd in ['hl']:
    for ind_pat in range(num_test_dict[hd]['start_ind'], num_test_dict[hd]['end_ind'] + 1):
      
      #mod_proj_da2130s100_obj_02943705_d5_it8
      cur_inp_file = f'{data_folder}/{pat_id_arr[ind_pat]}/CTAC/{def_name}/reoriented_windowed.img'
      #cur_inp_file = f'{data_folder}/{pat_id_arr[ind_pat]}/{def_name}/recon_pat{pat_id_arr[ind_pat]}_d{subsample_level}_it{num_iter}_c30o5.img'
      
      #cur_label_file = f'{label_data_folder}/{pat_id_arr[ind_pat]}/{def_name}/recon_pat{pat_id_arr[ind_pat]}_d1_it{num_iter}_c30o5.img'
      cur_label_file = f'{label_data_folder}/{pat_id_arr[ind_pat]}/CTAC/{def_name}/reoriented_windowed.img'
      
      cur_X = my_read_bin(cur_inp_file, 'float32', input_shape_orig)
      cur_Y = my_read_bin(cur_label_file, 'float32', input_shape_orig)
      cur_X = (cur_X - np.min(cur_X))/(np.max(cur_X) - np.min(cur_X))*sc_data
      cur_Y = (cur_Y - np.min(cur_Y))/(np.max(cur_Y) - np.min(cur_Y))*sc_data
      X_test[j,:, :, :, :] = cur_X[:, :, :, :]
      Y_test[j,:, :, :, :] = cur_Y[:, :, :, :]
      j = j + 1

  print("--------------------------------------------------------")
  print("Test Input Shape => " + str(X_test.shape))
  print("Test Label Shape => " + str(Y_test.shape))
  print('Number of Test Examples: %d' % X_test.shape[0])
  print("--------------------------------------------------------")

  #-----------------------------------------------------------
  # Step-2: Build and Train Model
  #----------------------------------------------------------
  # Function Call: def build_segnet3D_par(input_shape,num_GPUs,num_reg):
  #parallel_model = build_segnet3D_par(input_shape,num_GPUs,num_reg)
  pred_model = build_dennet3D_pred(input_shape, num_reg)
  com_flag = f'_d{subsample_level}_it{num_iter}_b{bt_size}_lmbdchdiff{lambda_val_ind_chdiff}_lmbdmdiff{lambda_val_ind_mdiff}'
  com_flag_new = f'_{def_name}_d{subsample_level}_it{num_iter}_b{bt_size}_lmbdchdiff{lambda_val_ind_chdiff}_lmbdmdiff{lambda_val_ind_mdiff}'
  
  
  weights_base_name = f'{mod_data_folder}/weights/{weights_name}{com_flag}_ep{num_epochs:03d}.hdf5' #############################################################
  #weights_base_name= '/data01/user-storage/y.zezhang/data_for_zezhang_mar29/learning/den_3d_v28/weights/test_wt_v28_d6_it8_b32_lmbdchdiff0_lmbdmdiff2_f3_ep200.hdf5'
  pred_model.load_weights(weights_base_name, by_name = True)############################################################################
  Y_pred = pred_model.predict(X_test, batch_size=16) 
  
  
  #-----------------------------------------------------------
  # Step-3: Save 
  #----------------------------------------------------------
  # save individually
  j = 0
  for hd in ['hl']:
    for ind_pat in range(num_test_dict[hd]['start_ind'], num_test_dict[hd]['end_ind'] + 1):
      cur_pred = np.squeeze(Y_pred[j, :, :, :, :])
      cur_out_file = f'{mod_data_folder}/pred/{def_name}/recon_pat{pat_id_arr[ind_pat]}{com_flag_new}.img'
      my_write_bin(cur_out_file, 'float32', cur_pred)############################################################################
      j = j + 1

  return

#=============================================================================================================================
## Main  ##
#=============================================================================================================================
if __name__ == '__main__':
  # start a parser
  parser = argparse.ArgumentParser()
  parser.add_argument('--weights_name', type=str, help="path to save model weights as hdf5-file")
  parser.add_argument('--loss_fn_name', type=str, help="path to save loss curves as m-file")
  parser.add_argument('--base_folder', type=str, help="base folder for data and saving denoised images")
  parser.add_argument('--subsample_level', type=int, help="subsample_level")
  parser.add_argument('--num_iter', type=int, help="number of iterations in reconstructions")
  parser.add_argument('--batch_size', type=int, help="batch_size in learning scheme")
  parser.add_argument('--epochs', type=int, help="epochs in learning scheme")
  parser.add_argument('--learning_folder', type=str, help="saving folder of learning")
  parser.add_argument('--lambda_val_ind_chdiff', type=int, help="lambda value index of channel vector difference loss")
  parser.add_argument('--lambda_val_ind_mdiff', type=int, help="lambda value index of masked difference loss")
  parser.add_argument('--def_name', type=str, help="defect name")




  # parse the input arguments
  args = parser.parse_args()
  # Launch training routine
  test_seg3D(args.base_folder, args.weights_name, args.loss_fn_name, args.subsample_level, args.num_iter, args.batch_size, args.epochs, args.learning_folder,
                args.lambda_val_ind_chdiff, args.lambda_val_ind_mdiff, args.def_name)
 

