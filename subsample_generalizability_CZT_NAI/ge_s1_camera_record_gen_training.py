import pydicom as dicom
import pydicom
import matplotlib.pylab as plt
import numpy as np
import os
from tempfile import TemporaryFile
import pandas as pd
import shutil 


def my_read_bin(cur_inp_file, data_type, input_shape):
  A = np.fromfile(cur_inp_file, dtype = data_type)
  A[np.isnan(A)] = 0
  A = np.reshape(A, input_shape)
  #A = np.transpose(A, [2, 1, 0])
  return A

def my_write_bin(cur_out_file, data_type, data):
  #data = np.transpose(data, [2, 1, 0])
  data.astype(data_type).tofile(cur_out_file)
  return

excel_file_name = 'collimator_training_data.xlsx'
csv_file_name = 'collimator_training_data.csv'
outputFolder = '/data01/user-storage/y.zezhang/2024_subsample_project/document/collimator_record'
#outputFolder = '/data03/user-storage/y.zezhang/Ashequr/data_spie_v2/train_mc_castor/00705441/mod_proj'
# Get the list of target patient 

training_patient_list_path = "/data01/user-storage/y.zezhang/2024_subsample_project/mod_Neural_network_training/30/training"

training_patient_list = os.listdir(training_patient_list_path)

# Get the list of patient data and directories
real_patient_data_path = "/data01/user-storage/y.zezhang/reg_PriPrj_ScaPrj_RegCT_DICOM"
patient_list = os.listdir(real_patient_data_path)

excel_file=f'{outputFolder}/{excel_file_name}'
csv_file=f'{outputFolder}/{csv_file_name}'

data = []
# select useful_data
useful_patient_list=[]
for patient in training_patient_list:
    for count, ele in enumerate(patient_list):
        if patient  in ele and 'PriPrj' in ele:
        
            #useful_patient_list.append(ele)
            useful_patient_path=os.path.join(real_patient_data_path, ele)
            patient_file_list = os.listdir(useful_patient_path)
            patient_file_list.remove('metacache.mim')
            patient_file=os.path.join(useful_patient_path, patient_file_list[0])  
            ds = dicom.dcmread(patient_file)
            
            collimator_grid_name=ds[0x00540022][0][0x00181180].value
            #Real_World_Value_Intercept=ds[0x00409096][0][0x00409224].value
            #Real_World_Value_Slope=ds[0x00409096][0][0x00409225].value
            # Determine material based on presence of 'w' in collimator grid name
            material = "CZT" if 'W' in collimator_grid_name else "NaI"

            # Append the data (file name, collimator grid name, material) to the list
            data.append([patient,  material, collimator_grid_name])
            print(f"Processed file '{patient}': {material}")
            

# Convert the list to a pandas DataFrame
df = pd.DataFrame(data, columns=["patient", "Material", "Collimator Grid Name" ])

# Write the DataFrame to an Excel file
df.to_excel(excel_file, index=False, engine='openpyxl')
df.to_csv(csv_file, index=False)
print(f"Data written to '{excel_file}' successfully.")



    