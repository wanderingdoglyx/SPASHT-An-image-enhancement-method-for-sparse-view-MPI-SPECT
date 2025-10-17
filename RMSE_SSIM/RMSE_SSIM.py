import os
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
from collections import defaultdict

def calculate_rmse(imageA, imageB):
    """Calculate Root Mean Squared Error (RMSE) between two images."""
    return np.sqrt(np.mean((imageA - imageB) ** 2))

def calculate_ssim(imageA, imageB):
    """Calculate Structural Similarity Index (SSIM) between two images."""
    return ssim(imageA, imageB, multichannel=True)

def load_image(image_path):
    """Load an image from the specified path."""
    image = cv2.imread(image_path)
    if image is not None:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

def calculate_metrics_for_groups(groupA_dir, groupB_dir):
    """Calculate RMSE and SSIM between two groups of images."""
    groupA_images = sorted([os.path.join(groupA_dir, img) for img in os.listdir(groupA_dir)])
    groupB_images = sorted([os.path.join(groupB_dir, img) for img in os.listdir(groupB_dir)])

    rmse_list = []
    ssim_list = []

    for imgA_path, imgB_path in zip(groupA_images, groupB_images):
        imageA = load_image(imgA_path)
        imageB = load_image(imgB_path)

        if imageA is not None and imageB is not None and imageA.shape == imageB.shape:
            rmse_value = calculate_rmse(imageA, imageB)
            ssim_value = calculate_ssim(imageA, imageB)

            rmse_list.append(rmse_value)
            ssim_list.append(ssim_value)

            print(f"{os.path.basename(imgA_path)} vs {os.path.basename(imgB_path)}: RMSE={rmse_value:.4f}, SSIM={ssim_value:.4f}")
        else:
            print(f"Skipping {os.path.basename(imgA_path)} and {os.path.basename(imgB_path)} due to size mismatch or loading issue.")

    # Return the average RMSE and SSIM values
    avg_rmse = np.mean(rmse_list) if rmse_list else None
    avg_ssim = np.mean(ssim_list) if ssim_list else None

    return avg_rmse, avg_ssim

def my_read_bin(cur_inp_file, data_type, input_shape):
  A = np.fromfile(cur_inp_file, dtype = data_type)
  A[np.isnan(A)] = 0
  A = np.reshape(A, input_shape)
  A = np.transpose(A, [2, 1, 0])
  return A


pat_id_arr_fname = f'/data01/user-storage/y.zezhang/2024_subsample_project/document/zitong_patient_list/pat_id_diseased_v2.txt'
diseased_patients = np.loadtxt(pat_id_arr_fname, dtype = 'str', comments="#", delimiter=",", unpack=False)

pat_id_arr_fname = f'/data01/user-storage/y.zezhang/2024_subsample_project/document/zitong_patient_list/pat_id_healthy_v2.txt'
healthy_patients = np.loadtxt(pat_id_arr_fname, dtype = 'str', comments="#", delimiter=",", unpack=False)

location_setting=  ['a','i']
extent_setting =  [30,60] #[30,90,60] 
severity_setting=  [100,175,250] #[100,175,250]

CT_category=['CTAC']

observer_study_list = os.listdir('/data01/user-storage/y.zezhang/2024_subsample_project/mod_SA_images')

def_folder='/data01/user-storage/y.zezhang/2024_subsample_project/mod_Neural_network_training/centroid_mask/testing'
base_folder = '/data01/user-storage/y.zezhang/2024_subsample_project/mod_SA_images'
full_view_folder='/data01/user-storage/y.zezhang/2024_subsample_project/mod_SA_images/30'

inp_shape = (48, 48, 48)
inp_shape_orig = (48, 48, 48)

for study_project in observer_study_list:
    
    rmse_list = []
    ssim_list = []


    save_folder = f'{base_folder}/{study_project}'
    sub_base_folder=os.path.join(base_folder,study_project)
    
    if not os.path.isdir(save_folder):
        os.mkdir(save_folder)
        
    print(f'loading images... ')

    ff = {'diseased':defaultdict(list), 'healthy':defaultdict(list)}
    pat_ind_arr = {'diseased':diseased_patients, 'healthy':healthy_patients}
        
    for CT_method in CT_category:
        for diag in ['diseased', 'healthy']:
            status_folder=os.path.join(sub_base_folder,diag)
            full_view_status_folder=os.path.join(full_view_folder,diag)
            #subensemble_idx = 0
            
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
                                SA_rec_base = my_read_bin(SA_name, 'float32', inp_shape_orig) 
                                SA_rec_base = (SA_rec_base-np.min(SA_rec_base))/(np.max(SA_rec_base)-np.min(SA_rec_base))*255
                    
                                full_view_cur_path=os.path.join(full_view_status_folder,patient)
                                full_view_cur_path=os.path.join(full_view_cur_path,CT_method)
                                full_view_cur_path=os.path.join(full_view_cur_path,def_type)  
                                
                                full_view_SA_name=os.path.join(full_view_cur_path,'extended_reoriented_windowed.img')
                                full_view_SA_rec_base = my_read_bin(full_view_SA_name, 'float32', inp_shape_orig) 
                                full_view_SA_rec_base = (full_view_SA_rec_base-np.min(full_view_SA_rec_base))/(np.max(full_view_SA_rec_base)-np.min(full_view_SA_rec_base))*255

                                rmse_value = calculate_rmse(SA_rec_base, full_view_SA_rec_base)
                                ssim_value = calculate_ssim(SA_rec_base, full_view_SA_rec_base)
        
                                rmse_list.append(rmse_value)
                                ssim_list.append(ssim_value)
                                
                                
                        elif diag == 'healthy':
                            for hl_item in healthy_patients:
                                patient=hl_item

                                cur_path=os.path.join(status_folder,patient)
                                cur_path=os.path.join(cur_path,CT_method)
                                cur_path=os.path.join(cur_path,'hl')
                        
                                SA_name=os.path.join(cur_path,'extended_reoriented_windowed.img')
                    
                                SA_rec_base = my_read_bin(SA_name, 'float32', inp_shape_orig) 
                                SA_rec_base = (SA_rec_base-np.min(SA_rec_base))/(np.max(SA_rec_base)-np.min(SA_rec_base))*255
                                
                                full_view_cur_path=os.path.join(full_view_status_folder,patient)
                                full_view_cur_path=os.path.join(full_view_cur_path,CT_method)
                                full_view_cur_path=os.path.join(full_view_cur_path,'hl') 
                                
                                full_view_SA_name=os.path.join(full_view_cur_path,'extended_reoriented_windowed.img')
                                full_view_SA_rec_base = my_read_bin(full_view_SA_name, 'float32', inp_shape_orig) 
                                full_view_SA_rec_base = (full_view_SA_rec_base-np.min(full_view_SA_rec_base))/(np.max(full_view_SA_rec_base)-np.min(full_view_SA_rec_base))*255
                                
                                rmse_value = calculate_rmse(SA_rec_base, full_view_SA_rec_base)
                                ssim_value = calculate_ssim(SA_rec_base, full_view_SA_rec_base)

                                rmse_list.append(rmse_value)
                                ssim_list.append(ssim_value)
        # Return the average RMSE and SSIM values
        
    avg_rmse = np.mean(rmse_list) if rmse_list else None
    avg_ssim = np.mean(ssim_list) if ssim_list else None

    output_file=f'{save_folder}/{study_project}_vs_full_view.txt'
    
    with open(output_file, 'w') as f:
        
        f.write(f"Comparing groups:\nGroup A: {study_project}\nGroup B: full_view \n")
        f.write('RMSE '+str(avg_rmse) + "\n")
        f.write('SSIM '+str(avg_ssim) + "\n")
        f.write("\n")
        
        
'''      
    groupA_dir = 'path_to_groupA_images'
    groupB_dir = 'path_to_groupB_images'

    avg_rmse, avg_ssim = calculate_metrics_for_groups(groupA_dir, groupB_dir)

    if avg_rmse is not None and avg_ssim is not None:
        print(f"Average RMSE: {avg_rmse:.4f}")
        print(f"Average SSIM: {avg_ssim:.4f}")
    else:
        print("No valid image pairs found for comparison.")
'''