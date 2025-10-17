import os
import shutil
import numpy as np




pat_id_arr_fname = f'/data01/user-storage/y.zezhang/2024_subsample_project/document/zitong_patient_list/pat_id_diseased_v2.txt'
diseased_patients = np.loadtxt(pat_id_arr_fname, dtype = 'str', comments="#", delimiter=",", unpack=False)

pat_id_arr_fname = f'/data01/user-storage/y.zezhang/2024_subsample_project/document/zitong_patient_list/pat_id_healthy_v2.txt'
healthy_patients = np.loadtxt(pat_id_arr_fname, dtype = 'str', comments="#", delimiter=",", unpack=False)

#diseased_patients, healthy_patients = read_patient_file(file_path)
isIO=0
CT_category='CTAC'

nn_version='2s500'

subsample_slice=15
bench=32
lmbdchdiff=7
lmbdmdiff=0


location_setting=  ['a','i']
extent_setting =  [30,90,60] 
severity_setting=   [100,175,250,500]

def_folder='/data01/user-storage/y.zezhang/data_for_zezhang_mar29/test_data_mirirv3_sa_wd'
sa_base=f'/data01/user-storage/y.zezhang/2024_subsample_project/mod_Neural_network_training/learning/subsample_3d_v{nn_version}/pred'
save_folder = f'/data01/user-storage/y.zezhang/2024_subsample_project/mod_SA_images/subsample_3d_v{nn_version}_d{subsample_slice}_lmbdchdiff{lmbdchdiff}_nn'


for diag in ['diseased', 'healthy']:
    
    status_folder=os.path.join(save_folder,diag)
    subensemble_idx = 0
    
    if not os.path.exists(status_folder):
        os.makedirs(status_folder)
    for location in location_setting:
        for extent in extent_setting:
          for severity in severity_setting:
           
                if diag == 'diseased':
                    for  di_item in diseased_patients:
                        
                        
                        patient=di_item
                        def_type= f'd{location}21{extent}s{severity}'
                        def_centroid_type=def_type.split('s')[0]
                    
                    
                        cur_path=os.path.join(sa_base,def_type)
                        #cur_path=os.path.join(cur_path,def_type)
                    
                        SA_fname='recon_pat'+ patient +'_'+def_type+'_d'+str(subsample_slice)+'_it8_b'+str(bench)+'_lmbdchdiff'+str(lmbdchdiff)+'_lmbdmdiff'+str(lmbdmdiff)+'.img'
                        SA_name=os.path.join(cur_path,SA_fname)
                        
                        
                        save_subfolder=os.path.join(status_folder,patient)
                        save_subfolder=os.path.join(save_subfolder,CT_category)
                        save_subfolder=os.path.join(save_subfolder,def_type)
                        
                        dest_path=save_subfolder+'/'+'extended_reoriented_windowed.img'
                        
                        if not os.path.exists(save_subfolder):
                            os.makedirs(save_subfolder)
                            
                            
                        shutil.copy(SA_name, dest_path)
                        
                    
                        
                elif diag == 'healthy':
                    for hl_item in healthy_patients:
                        patient=hl_item
                        
                    #  SA_name=os.path.join(cur_path,'extended_reoriented_windowed.img')
                        
                        def_type=f'd{location}21{extent}s{severity}'
                        def_centroid_type=def_type.split('s')[0]
                    
                    
                        cur_path=os.path.join(sa_base,'hl')
                        
                    
                        SA_fname='recon_pat'+ patient +'_'+'hl'+'_d'+str(subsample_slice)+'_it8_b'+str(bench)+'_lmbdchdiff'+str(lmbdchdiff)+'_lmbdmdiff'+str(lmbdmdiff)+'.img'
                        SA_name=os.path.join(cur_path,SA_fname)
                        
                        
                        save_subfolder=os.path.join(status_folder,patient)
                        save_subfolder=os.path.join(save_subfolder,CT_category)
                        save_subfolder=os.path.join(save_subfolder,'hl')
                        
                        dest_path=save_subfolder+'/'+'extended_reoriented_windowed.img'
                        
                        if not os.path.exists(save_subfolder):
                            os.makedirs(save_subfolder)
                            
                        shutil.copy(SA_name, dest_path)
