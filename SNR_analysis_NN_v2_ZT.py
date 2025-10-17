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
from scipy.ndimage import shift
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


pat_id_arr_fname = f'/data01/user-storage/y.zezhang/2024_subsample_project/document/zitong_patient_list/pat_id_diseased_v3.txt'
diseased_patients = np.loadtxt(pat_id_arr_fname, dtype = 'str', comments="#", delimiter=",", unpack=False)

pat_id_arr_fname = f'/data01/user-storage/y.zezhang/2024_subsample_project/document/zitong_patient_list/pat_id_healthy_v3.txt'
healthy_patients = np.loadtxt(pat_id_arr_fname, dtype = 'str', comments="#", delimiter=",", unpack=False)

isIO=0

dl_version='2s'
batch_size=32
subsample_level=15
bt_size=32
lambda_val_ind_mdiff=0

#lambda_val_ind_chdiff=7
lambda_val_ind_chdiff=0


Ud=64
isIO=0

location_setting=['i','a']  #['a','i']
extent_setting = [30,60]  #[30,45,60] 
severity_setting= [100,175,250] # [100,175,250]


base_folder = f'/data01/user-storage/y.zezhang/2024_subsample_project/mod_Neural_network_training/learning/subsample_3d_v{dl_version}/pred'##########################
save_base_folder = f'/data01/user-storage/y.zezhang/2024_subsample_project/mod_Neural_network_training/learning/subsample_3d_v{dl_version}'#
save_folder = f'{save_base_folder}/SNR/NN_lmbd_mdiff{lambda_val_ind_chdiff}/d{subsample_level}/'###########
def_folder='/data01/user-storage/y.zezhang/2024_subsample_project/mod_Neural_network_training/centroid_mask/testing'

SA_folder='/data01/user-storage/y.zezhang/2024_subsample_project/mod_SA_images'

#if not os.path.isdir(save_folder):
#  os.mkdir(save_folder)
os.makedirs(save_folder, exist_ok=True)

inp_shape = (48, 48, 48)
inp_shape_orig = (48, 48, 48)

#observer_study_list = os.listdir('/data01/user-storage/y.zezhang/2024_subsample_project/mod_SA_images')


print('loading pre-written channels file...')
if Ud == 32:
    U_flag = ''
elif Ud == 64:
    U_flag = f'_{Ud}'

U = np.load(f'/data01/user-storage/y.zezhang/2024_subsample_project/mod_Neural_network_training/U{U_flag}.npy')
print('U shape: ',U.shape)
U = np.transpose(U, [1,0])

print(f'loading images... || D: {subsample_level}')
ff = {'diseased':defaultdict(list), 'healthy':defaultdict(list)}
pat_ind_arr = {'diseased':diseased_patients , 'healthy':healthy_patients}
#pat_ind_arr_src = {'diseased':def_pat_list_src, 'healthy':hl_pat_list_src}

#def_name_arr = []
#for diag in ['diseased', 'healthy']:
    #for idx_list in range(len(pat_ind_arr[diag])):
      #pat_ind = pat_ind_arr[diag][idx_list]
      #src_name = pat_ind_arr_src[diag][idx_list]
      #print(pat_ind)
      
      
for location in location_setting:
    for extent in extent_setting:
        for severity in severity_setting:
            for diag in ['diseased', 'healthy']:
                for di_item in diseased_patients:
                    subensemble_idx = 0
                    if diag == 'diseased':
                        
                        patient=di_item
                        
                        def_name = f'd{location}21{extent}s{severity}'
                        def_centroid_type=def_name.split('s')[0]
                        
                        nn_folder=f'd{subsample_level}_lmbdchdiff{lambda_val_ind_chdiff}_nn'
                        cur_path=os.path.join(SA_folder,nn_folder,diag,patient,'CTAC',def_name)
                        
                        SA_fname='extended_reoriented_windowed.img'
                    
                        SA_name=os.path.join(cur_path,SA_fname)
                        
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
                            #SA_rec = SA_rec - np.mean(SA_rec) # remove zero frequency component
                            ff[diag][subensemble_idx].append(SA_rec.flatten())
                        
            
                
                    elif diag == 'healthy':
                        for hl_item in healthy_patients:
                            
                            patient=hl_item
                            #cur_path=os.path.join(SA_folder,'hl')
                            
                            nn_folder=f'd{subsample_level}_lmbdchdiff{lambda_val_ind_chdiff}_nn'
                            cur_path=os.path.join(SA_folder,nn_folder,diag,patient,'CTAC','hl')
                        
                            SA_fname='extended_reoriented_windowed.img'

                            #SA_fname='recon_pat'+ patient +'_'+'hl'+'_d'+str(subsample_level)+'_it8_b'+str(bt_size)+'_lmbdchdiff'+str(lambda_val_ind_chdiff)+'_lmbdmdiff'+str(lambda_val_ind_mdiff)+'.img'              
                            SA_name=os.path.join(cur_path,SA_fname)
                            
                            def_name = f'd{location}21{extent}s{severity}'
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
                                #SA_rec = SA_rec - np.mean(SA_rec) # remove zero frequency component
                                ff[diag][subensemble_idx].append(SA_rec.flatten())
                        




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

            np.save(save_folder +'delta_f_bar_'+str(dl_version)+'_d'+str(subsample_level)+'_location'+str(location)+"_extent"+str(extent)+'_severity'+str(severity),delta_f_bar)
            np.save(save_folder +"delta_v_bar_"+str(dl_version)+'_d'+str(subsample_level)+'_location'+str(location)+"_extent"+str(extent)+'_severity'+str(severity),delta_v_bar)
            np.save(save_folder + "K_"+str(dl_version)+'_d'+str(subsample_level)+'_location'+str(location)+"_extent"+str(extent)+'_severity'+str(severity),K)
            np.save(save_folder +'IS'+str(dl_version)+'_d'+str(subsample_level)+'_location'+str(location)+"_extent"+str(extent)+'_severity'+str(severity),np.mean(IS,axis=1))
            np.save(save_folder +"IN"+str(dl_version)+'_d'+str(subsample_level)+'_location'+str(location)+"_extent"+str(extent)+'_severity'+str(severity),np.mean(IN,axis=1))

            #savemat('delta_f_bar_'+str(dl_version)+'_d'+str(dose_level),delta_g_bar)
            #savemat("vData_"+str(dl_version)+'_d'+str(dose_level),vData)
            #savemat("K_"+str(dl_version)+'_d'+str(dose_level),K)
            #,{"vData_"+str(dl_version)+'_d'+str(dose_level): vData },{"K_"+str(dl_version)+'_d'+str(dose_level): K }
            mdic={'delta_f_bar_'+str(dl_version)+'_d'+str(subsample_level): delta_f_bar,
                    "delta_v_bar_"+str(dl_version)+'_d'+str(subsample_level): delta_v_bar,
                    "K_"+str(dl_version)+'_d'+str(subsample_level): K,
                    "IS_"+str(dl_version)+'_d'+str(subsample_level): np.mean(IS,axis=1),
                    "IN_"+str(dl_version)+'_d'+str(subsample_level):np.mean(IN,axis=1) }
                    

            savemat(save_folder +'SNR_data_'+str(dl_version)+'_d'+str(subsample_level)+'_location'+str(location)+"_extent"+str(extent)+'_severity'+str(severity)+'.mat', mdic)

            print('done')

'''
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

np.save(save_folder +'delta_f_bar_'+str(dl_version)+'_d'+str(subsample_level)+'_location'+str(location_setting)+"_extent"+str(extent_setting)+'_severity'+str(severity_setting),delta_f_bar)
np.save(save_folder +"delta_v_bar_"+str(dl_version)+'_d'+str(subsample_level)+'_location'+str(location_setting)+"_extent"+str(extent_setting)+'_severity'+str(severity_setting),delta_v_bar)
np.save(save_folder + "K_"+str(dl_version)+'_d'+str(subsample_level)+'_location'+str(location_setting)+"_extent"+str(extent_setting)+'_severity'+str(severity_setting),K)
np.save(save_folder +'IS'+str(dl_version)+'_d'+str(subsample_level)+'_location'+str(location_setting)+"_extent"+str(extent_setting)+'_severity'+str(severity_setting),np.mean(IS,axis=1))
np.save(save_folder +"IN"+str(dl_version)+'_d'+str(subsample_level)+'_location'+str(location_setting)+"_extent"+str(extent_setting)+'_severity'+str(severity_setting),np.mean(IN,axis=1))

#savemat('delta_f_bar_'+str(dl_version)+'_d'+str(dose_level),delta_g_bar)
#savemat("vData_"+str(dl_version)+'_d'+str(dose_level),vData)
#savemat("K_"+str(dl_version)+'_d'+str(dose_level),K)
#,{"vData_"+str(dl_version)+'_d'+str(dose_level): vData },{"K_"+str(dl_version)+'_d'+str(dose_level): K }
mdic={'delta_f_bar_'+str(dl_version)+'_d'+str(subsample_level): delta_f_bar,
      "delta_v_bar_"+str(dl_version)+'_d'+str(subsample_level): delta_v_bar,
      "K_"+str(dl_version)+'_d'+str(subsample_level): K,
      "IS_"+str(dl_version)+'_d'+str(subsample_level): np.mean(IS,axis=1),
      "IN_"+str(dl_version)+'_d'+str(subsample_level):np.mean(IN,axis=1) }
      

savemat(save_folder +'SNR_data'+str(dl_version)+'_d'+str(subsample_level)+'_location'+str(location_setting)+"_extent"+str(extent_setting)+'_severity'+str(severity_setting)+'.mat', mdic)
'''