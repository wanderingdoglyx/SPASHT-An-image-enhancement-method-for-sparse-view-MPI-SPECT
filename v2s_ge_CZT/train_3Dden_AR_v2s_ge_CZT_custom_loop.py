======================================================================================================================
## Import Libraries  ##
#=============================================================================================================================
import sys, os, gc
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
import os
#import network model
from Den3D_Model_AR_v1_Loop import build_dennet3D, ClearMemory
plt.switch_backend('Agg')
tf.compat.v1.enable_eager_execution()
#tf.config.run_functions_eagerly(True)


def log_plot_loss_metric(
                train_metric, val_metric,
                train_label, val_label,
                ylabel_name, fig_title,
                png_filename
              ): 

  fig, ax = plt.subplots()
  ax.plot(train_metric, label=train_label)
  ax.plot(val_metric, label=val_label)
  ax.set_yscale('log')
  ax.set_xlabel('epoch')
  ax.set_ylabel(ylabel_name)
  ax.set_title(fig_title)
  ax.legend()

  plt.savefig(png_filename, bbox_inches='tight') 
  plt.close(fig)

  return

def get_indices(train_pat_index, test_pat_index, num_data_dict, loc_arr, ext_arr, sev_arr):
  train_index = []
  test_index = []

  j = 0
  for hd in ['hl']:
    for ind_pat in range(num_data_dict[hd]['start_ind'], num_data_dict[hd]['end_ind'] + 1):
      for loc in loc_arr:
        for ext in ext_arr:
          if (ind_pat in train_pat_index):
            train_index.append(j)
          else:
            test_index.append(j)
          j = j + 1

  for hd in ['def']:
    for ind_pat in range(num_data_dict[hd]['start_ind'], num_data_dict[hd]['end_ind'] + 1):
      for loc in loc_arr:
        for ext in ext_arr:
          for sev in sev_arr:
            if (ind_pat in train_pat_index):
              train_index.append(j)
            else:
              test_index.append(j)
            j = j + 1

  return train_index, test_index



def my_read_bin(cur_inp_file, data_type, input_shape):
  A = np.fromfile(cur_inp_file, dtype = data_type)
  A[np.isnan(A)] = 0
  A = np.reshape(A, input_shape)
  A = np.transpose(A, [2, 1, 0, 3])
  return A

#@tf.function
def train_step(model, x_batch_train, y_batch_train, y_batch_loc_train, y_batch_mask_train, opt):
  with tf.GradientTape() as tape:
    model([x_batch_train, y_batch_train, y_batch_loc_train, y_batch_mask_train], training=True)
    loss_value = sum(model.losses)

  grads = tape.gradient(loss_value, model.trainable_weights)
  opt.apply_gradients(zip(grads, model.trainable_weights))
  return loss_value
   
#@tf.function
def val_step(model, x_batch_val, y_batch_val,y_batch_loc_val,y_batch_mask_val):
  # forward pass multipe times to get IW estimate
  model([x_batch_val, y_batch_val, y_batch_loc_val, y_batch_mask_val], training=False)
  loss_value = sum(model.losses)
  return loss_value

#=============================================================================================================================
## Define training protocols  ##
#=============================================================================================================================
def train_seg3D(base_folder, weights_name, loss_fn_name, subsample_level, num_iter, bt_size, num_epochs, learning_folder, 
                lambda_val_ind_chdiff, lambda_val_ind_mdiff):

  #-----------------------------------------------------------
  # Step-1: Data pre-processing
  #----------------------------------------------------------
  lambda_val_arr_chdiff = [0, 1e-3, 5e-3, 1e-2, 5e-2, 1e-1, 3e-1, 1e0, 5e0, 1e1]
  lambda_val_arr_mdiff = [0, 1e-1, 5e-1, 1e0, 5e0, 1e1, 3e1, 1e2, 5e2, 1e3]
  lambda_val_chdiff = lambda_val_arr_chdiff[lambda_val_ind_chdiff]
  lambda_val_mdiff = lambda_val_arr_mdiff[lambda_val_ind_mdiff]
  print(f'lambda_val_chdiff: {lambda_val_chdiff}')
  print(f'lambda_val_mdiff: {lambda_val_mdiff}')


  label_data_folder=f'{base_folder}/30/ge_total'
  data_folder = f'{base_folder}/{subsample_level}/ge_total'
  data_folder_prev = f'{base_folder}/centroid_mask/ge_total'
  mod_data_folder = f'{base_folder}/learning/{learning_folder}'

  # load protocols
  subsample_level_max = 30
  num_z_slice = 64
  num_reg = 1
  Nx_in, Ny_in, Nz_in = 48, 48, 48
  Nz_in_prev = 32
  num_input_channels = 1
  num_output_channels = num_reg
  Nx_out, Ny_out, Nz_out = 48, 48, 48
  Nz_out_prev = 32

  input_shape = (Nx_in, Ny_in, Nz_in, num_input_channels)
  input_shape_prev = (Nx_in, Ny_in, Nz_in_prev, num_input_channels)
  loc_shape = (Nx_in, Ny_in, 1)
  input_shape_orig = (Nz_in, Ny_in, Nx_in, num_input_channels)
  input_shape_orig_prev = (Nz_in_prev, Ny_in, Nx_in, num_input_channels)
  output_shape = (Nx_out, Ny_out, Nz_out, num_output_channels)
  output_shape_orig = (Nz_out, Ny_out, Nx_out, num_output_channels)
  output_shape_orig_prev = (Nz_out_prev, Ny_out, Nx_out, num_output_channels)

  num_pat = 205
  num_data_dict = {
        'hl': {
                'start_ind': 0,
                'end_ind': num_pat-1,
              },
        'def': {
                'start_ind': 0,
                'end_ind': num_pat-1,
              }
      }
  
  loc_arr = ['a', 'i']                  #############################################################
  sev_arr = [100, 175, 250]             #############################################################
  ext_arr = [30, 60]                    #############################################################

  remove_indices = [] # 3, 51, def center not in center  # remove indice 1 in test case#[77,90,110,140]
  num_train_hl = num_data_dict['hl']['end_ind'] - num_data_dict['hl']['start_ind'] + 1
  num_train_def = num_data_dict['def']['end_ind'] - num_data_dict['def']['start_ind'] + 1
  num_train = num_train_hl*len(loc_arr)*len(ext_arr) + num_train_def * len(loc_arr)* len(ext_arr) * len(sev_arr)
  X_data = np.zeros((num_train,) + input_shape)
  print("X_data allocated")
  Y_data = np.zeros((num_train,) + output_shape)
  Y_data_loc = np.zeros((num_train,) + loc_shape)
  Y_data_mask = np.zeros((num_train,) + input_shape)
  print("Y_data allocated")

 
 
  

  #pat_id_arr = os.listdir('/data01/user-storage/y.zezhang/2024_subsample_project/mod_Neural_network_training/'+str(subsample_level)+'/training')
  pat_id_arr_fname = f'/data01/user-storage/y.zezhang/2024_subsample_project/document/collimator_record/patients_with_CZT.txt'
  pat_id_arr = np.loadtxt(pat_id_arr_fname, dtype = 'str', comments="#", delimiter=",", unpack=False)


  sc_data = 255
  j = 0
  for hd in ['hl']:
    for ind_pat in range(num_data_dict[hd]['start_ind'], num_data_dict[hd]['end_ind'] + 1):
      if (ind_pat in remove_indices):
        print(f'Removing: {ind_pat}')
        continue
      cur_inp_file = f'{data_folder}/{pat_id_arr[ind_pat]}/CTAC/{hd}/reoriented_windowed.img'
      #cur_label_file = f'{label_data_folder}/{pat_id_arr[ind_pat]}/{hd}/recon_pat{pat_id_arr[ind_pat]}_d1_it{num_iter}_c30o5.img'
      cur_label_file = f'{label_data_folder}/{pat_id_arr[ind_pat]}/CTAC/{hd}/reoriented_windowed.img'
      
      cur_X = my_read_bin(cur_inp_file, 'float32', input_shape_orig)
      cur_Y = my_read_bin(cur_label_file, 'float32', input_shape_orig)
      #print(f'Ind: {ind_pat} || Pat id: {pat_id_arr[ind_pat]} || Sum train X: {np.sum(cur_X)} || Sum train Y: {np.sum(cur_Y)} || Rat: {np.sum(cur_X)/np.sum(cur_Y):.2f}')
      #print(f'Ind: {ind_pat} || Pat id: {pat_id_arr[ind_pat]} || Rat: {np.sum(cur_X)/np.sum(cur_Y):.2f}')
      cur_X = (cur_X - np.min(cur_X))/(np.max(cur_X) - np.min(cur_X))*sc_data
      cur_Y = (cur_Y - np.min(cur_Y))/(np.max(cur_Y) - np.min(cur_Y))*sc_data
      for loc in loc_arr:
        for ext in ext_arr:
          def_loc_fname = f'{data_folder_prev}/{pat_id_arr[ind_pat]}/def_mask_d{loc}21{ext}.bin'
          cur_mask = my_read_bin(def_loc_fname, 'uint8', input_shape_orig_prev)
          def_loc_fname = f'{data_folder_prev}/{pat_id_arr[ind_pat]}/def_centroid_d{loc}21{ext}_mod.bin'
          cur_loc = np.fromfile(def_loc_fname, dtype = 'float32').astype(int) - 1 + 1 #0 -based / but nn2D has 1 shift ###########################################################
          #cur_loc= location_map_allocator.location_coordinate()

          X_data[j,:, :, :, :] = cur_X
          Y_data[j,:, :, :, :] = cur_Y
          Y_data_mask[j,:, :, -Nz_in_prev//2+Nz_in//2:Nz_in//2+Nz_in_prev//2, :] = cur_mask #8:39
          Y_data_loc[j, cur_loc[1] , cur_loc[0], 0] = 1.0 #28 #######################################################################
          #Y_data_loc[j, cur_loc[2] , cur_loc[1], 0] = 1.0
          j = j + 1

  for hd in ['def']:
    for ind_pat in range(num_data_dict[hd]['start_ind'], num_data_dict[hd]['end_ind'] + 1):
      if (ind_pat in remove_indices):
        print(f'Removing: {ind_pat}')
        continue
      for loc in loc_arr:
        for ext in ext_arr:
          def_loc_fname = f'{data_folder_prev}/{pat_id_arr[ind_pat]}/def_mask_d{loc}21{ext}.bin'
          cur_mask = my_read_bin(def_loc_fname, 'uint8', input_shape_orig_prev)
          def_loc_fname = f'{data_folder_prev}/{pat_id_arr[ind_pat]}/def_centroid_d{loc}21{ext}_mod.bin'
          cur_loc = np.fromfile(def_loc_fname, dtype = 'float32').astype(int) - 1 + 1 #######################################################################
          #cur_loc= location_map_allocator.location_coordinate()
          
          for sev in sev_arr:
            def_name = f'd{loc}21{ext}s{sev}'
            cur_inp_file = f'{data_folder}/{pat_id_arr[ind_pat]}/CTAC/{def_name}/reoriented_windowed.img'
            # cur_label_file = f'{label_data_folder}/{pat_id_arr[ind_pat]}/{def_name}/recon_pat{pat_id_arr[ind_pat]}_d1_it{num_iter}_c30o5.img'
            cur_label_file = f'{label_data_folder}/{pat_id_arr[ind_pat]}/CTAC/{def_name}/reoriented_windowed.img'
            
            cur_X = my_read_bin(cur_inp_file, 'float32', input_shape_orig)
            cur_Y = my_read_bin(cur_label_file, 'float32', input_shape_orig)
            cur_X = (cur_X - np.min(cur_X))/(np.max(cur_X) - np.min(cur_X))*sc_data
            cur_Y = (cur_Y - np.min(cur_Y))/(np.max(cur_Y) - np.min(cur_Y))*sc_data

            X_data[j,:, :, :, :] = cur_X
            Y_data[j,:, :, :, :] = cur_Y
            Y_data_mask[j,:, :, -Nz_in_prev//2+Nz_in//2:Nz_in//2+Nz_in_prev//2, :] = cur_mask
            Y_data_loc[j, cur_loc[1] , cur_loc[0], 0] = 1.0 #28 ###
            
            #print(f'Ind: {ind_pat} || Pat id: {pat_id_arr[ind_pat]} || Sum train X: {np.sum(X_data[j,:, :, :, :])} || Sum train Y: {np.sum(Y_data[j,:, :, :, :])}')
            j = j + 1

  X_data = X_data[:j, :, :, :, :]
  Y_data = Y_data[:j, :, :, :, :]
  Y_data_loc = Y_data_loc[:j, :]
  Y_data_mask = Y_data_mask[:j, :, :, :, :]
  print("--------------------------------------------------------")
  print("Training Input Shape => " + str(X_data.shape))
  print("Training Label Shape => " + str(Y_data.shape))
  print("Training Location input Shape => " + str(Y_data_loc.shape))
  print("Training Location mask Shape => " + str(Y_data_mask.shape))
  print('Number of Training Examples: %d' % X_data.shape[0])
  print("--------------------------------------------------------")
  #======================================================================================================================================
  # Import channels
  #======================================================================================================================================
  #channel_fname = base_folder+'/U_64.npy'
  #channel_fname = f'U_64.npy'
  channel_fname = f'U.npy'
  U = np.load(channel_fname)
  #ch_dim, num_ch = 64, 4
  ch_dim, num_ch = 32, 4
  U = np.reshape(U, [ch_dim, ch_dim, 1, num_ch])
  U = tf.convert_to_tensor(U, np.float32)
  num_fold = 5
  rand_state = 1

  #======================================================================================================================================
  # custom loops over folds
  #======================================================================================================================================
  kf = KFold(n_splits = num_fold, random_state = rand_state, shuffle = True)
  all_val_loss = np.zeros((num_epochs,))
  for ind_fold, (train_pat_index, test_pat_index) in enumerate(kf.split(np.arange(num_pat))):
    #===================================
    # clear
    #===================================
    X_train = None
    X_test = None
    Y_train = None
    Y_test = None
    Y_train_loc = None
    Y_test_loc = None
    Y_train_mask = None
    Y_test_mask = None
    model = None
    checkpoint = None
    train_history = None
    csv_logger = None
    K.clear_session();
    train_dataset = None
    val_dataset = None
    gc.collect();

    #===================================
    # set up fold data
    #===================================
    #print("TRAIN:", train_pat_index, "TEST:", test_pat_index)
    print('='*80)
    print(f'FOLD: {ind_fold+1}/{num_fold}')
    print('='*80)
    train_index, test_index = get_indices(train_pat_index, test_pat_index, num_data_dict, loc_arr, ext_arr, sev_arr)
    X_train, X_test = X_data[train_index], X_data[test_index]
    Y_train, Y_test = Y_data[train_index], Y_data[test_index]
    Y_train_loc, Y_test_loc = Y_data_loc[train_index], Y_data_loc[test_index]
    Y_train_mask, Y_test_mask = Y_data_mask[train_index], Y_data_mask[test_index]
    print("--------------------------------------------------------")
    print("Training Input Shape => " + str(X_train.shape))
    print("Testing Input Shape => " + str(X_test.shape))
  
    train_dataset = tf.data.Dataset.from_tensor_slices((X_train, Y_train, Y_train_loc, Y_train_mask))
    train_dataset = train_dataset.shuffle(buffer_size=len(X_train)).batch(bt_size)
    val_dataset = tf.data.Dataset.from_tensor_slices((X_test, Y_test, Y_test_loc, Y_test_mask)).batch(bt_size)
    

    #===================================
    # custom loop
    #===================================
    denoise_obs_net = build_dennet3D(input_shape, loc_shape, num_reg, lambda_val_chdiff, lambda_val_mdiff, U)
    com_flag = f'_d{subsample_level}_it{num_iter}_b{bt_size}_lmbdchdiff{lambda_val_ind_chdiff}_lmbdmdiff{lambda_val_ind_mdiff}_f{ind_fold}'
    weights_base_name = f'{mod_data_folder}/weights/{weights_name}' + com_flag
    opt = tf.keras.optimizers.Adam(learning_rate=1e-3) #change

    #print(f'tf.executing_eagerly(): {tf.executing_eagerly()}')
    logs = {}
    logs_it = {}
    val_flag = 1

    for epoch in range(num_epochs):
      start_time = time.time()
      print(f'Epoch:{epoch + 1}/{num_epochs}')
      #=====================================================================
      # step-1: Training steps
      #=====================================================================
      denoise_obs_net.reset_metrics()
      loss_value = 0
      for step, (x_train_batch, y_train_batch, y_train_loc_batch, y_train_mask_batch) in enumerate(train_dataset):
        # step-1: Do a training step fo each minibatch=>
        # forward run + auto-differnetiate + backprop update
        # loss_value += train_step(denoise_obs_net, x_train_batch, y_train_batch, opt)
        cur_loss = train_step(denoise_obs_net, x_train_batch, y_train_batch, y_train_loc_batch, y_train_mask_batch, opt)
        loss_value += cur_loss
        for m in denoise_obs_net.metrics:
          if 'train_' + m.name in logs_it:
            logs_it['train_' + m.name].append(m.result())
          else:
            logs_it['train_' + m.name] = [m.result()]

      #=====================================================================
      # step-2: log all losses and metrics on each epoch end of training set
      #=====================================================================
      for m in denoise_obs_net.metrics:
        if 'train_' + m.name in logs:
          logs['train_' + m.name].append(m.result())
        else:
          logs['train_' + m.name] = [m.result()]

      cur_train_loss = loss_value / (step + 1)
      if 'train_loss' in logs:
        logs['train_loss'].append(cur_train_loss)
      else:
        logs['train_loss'] = [cur_train_loss]

      #=====================================================================
      # step-3: log metric in terminal
      #=====================================================================
      print(
              f'Train: loss={cur_train_loss:.3f} || ' \
              f"mse = {logs['train_mse'][-1]:.3f} || " \
              f"chv_mse = {logs['train_chv_mse'][-1]:.3f} || " \
              f"masked_diff = {logs['train_masked_diff'][-1]:.3f} || " \
          )

      if val_flag:
        #=====================================================================
        # step-3: Validation steps
        #=====================================================================
        denoise_obs_net.reset_metrics()
        loss_value = 0
        for step, (x_batch_val, y_batch_val, y_batch_loc_val, y_batch_mask_val) in enumerate(val_dataset):
          loss_value += val_step(denoise_obs_net, x_batch_val, y_batch_val, y_batch_loc_val, y_batch_mask_val)

        #=====================================================================
        # step-4: log all losses and metrics on each epoch end of validation set
        #=====================================================================
        for m in denoise_obs_net.metrics:
          if 'val_' + m.name in logs:
            logs['val_' + m.name].append(m.result())
          else:
            logs['val_' + m.name] = [m.result()]

        cur_val_loss = loss_value / (step + 1)
        if 'val_loss' in logs:
          logs['val_loss'].append(cur_val_loss)
        else:
          logs['val_loss'] = [cur_val_loss]

      #=====================================================================
      # step-5: log metric in terminal
      #=====================================================================
      if val_flag:
        print(
              f'Val  : loss={cur_val_loss  :.3f} || ' \
              f"mse = {logs['val_mse'][-1]:.3f} || " \
              f"chv_mse = {logs['val_chv_mse'][-1]:.3f} || " \
              f"masked_diff = {logs['val_masked_diff'][-1]:.3f} || " \
          )
        print(f'Elapsed time: {(time.time() - start_time):.2f}s')
      print('=' * 60)

      #=====================================================================
      # step-6: save model, relevant metrics and loss function
      #=====================================================================
      save_freq = 20 #change
      if (epoch + 1) % num_epochs == 0:
        weights_filename = f'{weights_base_name}_ep{epoch+1:03d}.hdf5'
        denoise_obs_net.save_weights(
                            weights_filename,
                            save_format='h5',
                          )
    #-----------------------------------------------------------
    # Step-3: Save model and loss curve
    #----------------------------------------------------------
    # train and validation losses
    train_loss = logs['train_loss']
    val_loss = logs['val_loss']
    print(f'Val_loss:{val_loss}')
    all_val_loss += val_loss

    # train and validation metrics
    # MSE
    train_mse = logs['train_mse']
    val_mse = logs['val_mse']

    # chv_mse
    train_chv_mse = logs['train_chv_mse']
    val_chv_mse = logs['val_chv_mse']

    # masked_diff
    train_masked_diff = logs['train_masked_diff']
    val_masked_diff = logs['val_masked_diff']

    mdict = {
              "train_loss": train_loss, "val_loss": val_loss, 
              "train_mse": train_mse, "val_mse": val_mse,
              "train_chv_mse": train_chv_mse, "val_chv_mse": val_chv_mse,
              "train_masked_diff": train_masked_diff, "val_masked_diff": val_masked_diff,
            }
    loss_curve_name = loss_fn_name + com_flag

    sio.savemat(f'{mod_data_folder}/losses/{loss_curve_name}.mat', mdict)
    np.save(f'{mod_data_folder}/losses/{loss_curve_name}.npy', mdict)

    sio.savemat(f'{mod_data_folder}/losses/{loss_curve_name}_it.mat', logs_it)
    #-----------------------------------------------------------
    # Step-4: Plot loss and metric curve
    #----------------------------------------------------------
    # loss
    png_filename = f'{mod_data_folder}/losses/{loss_curve_name}.png'
    log_plot_loss_metric(
                          train_loss, val_loss, 
                          'Train Loss', 'Validation Loss', 
                          'Loss',
                          'Loss Curve',
                          png_filename
                        )

    # mse
    png_filename = f'{mod_data_folder}/losses/{loss_curve_name}_mse.png'
    log_plot_loss_metric(
                          train_mse, val_mse, 
                          'Train MSE', 'Validation MSE', 
                          'MSE',
                          'MSE Curve',
                          png_filename
                        )
    # chv_mse
    png_filename = f'{mod_data_folder}/losses/{loss_curve_name}_chv_mse.png'
    log_plot_loss_metric(
                          train_chv_mse, val_chv_mse, 
                          'Train CHV MSE', 'Validation CHV MSE', 
                          'CHV_MSE',
                          'CHV_MSE Curve',
                          png_filename
                        )
    # masked_diff
    png_filename = f'{mod_data_folder}/losses/{loss_curve_name}_masked_diff.png'
    log_plot_loss_metric(
                          train_masked_diff, val_masked_diff, 
                          'Train MASKED DIFF', 'Validation MASKED DIFF', 
                          'MASKED_DIFF',
                          'MASKED_DIFF Curve',
                          png_filename
                        )



  #-----------------------------------------------------------
  # save best validation loss epoch
  #----------------------------------------------------------
  print(f'All_val_loss: {all_val_loss}')
  all_fold_min_val_loss_ind = int(np.argmin(all_val_loss) + 1)
  print(f'Best Epoch: {all_fold_min_val_loss_ind}')
  com_flag = f'_d{subsample_level}_it{num_iter}_b{bt_size}_lmbdchdiff{lambda_val_ind_chdiff}_lmbdmdiff{lambda_val_ind_mdiff}'
  fname = f'{mod_data_folder}/losses/best_epoch_{com_flag}'
  np.savetxt(f'{fname}.txt',  np.atleast_1d(all_fold_min_val_loss_ind), fmt='%d')

  #denoise_obs_net.save('denoise_obs_net.h5')
  #-----------------------------------------------------------
  # EOF!!!
  #----------------------------------------------------------

  return denoise_obs_net

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

  # parse the input arguments
  args = parser.parse_args()
  # Launch training routine
  train_seg3D(args.base_folder, args.weights_name, args.loss_fn_name, args.subsample_level, args.num_iter, 
                args.batch_size, args.epochs, args.learning_folder, 
                args.lambda_val_ind_chdiff, args.lambda_val_ind_mdiff)

