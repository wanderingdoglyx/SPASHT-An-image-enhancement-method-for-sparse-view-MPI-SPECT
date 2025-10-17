clear;
close all;

addpath(genpath('/data01/user-storage/zitong/data/cardiac_trainsmission_less/patient_study/src/sa_v3/src'))

cur_data_path = '/data01/user-storage/zitong/data/cardiac_trainsmission_less/patient_study/data/SPIE/test/healthy/';
pat_id = '68469737';
def_type = 'dl_90_500';
cur_file = [cur_data_path,'/',pat_id,'/ScatLAC_rec/',def_type,'/reoriented_windowed.img'];
f = fopen(cur_file);
img = fread(f,'float32');
fclose(f)
img = reshape(img,48,48,32);

recon_cast_sa = img;
fname = 'test'
plot_sa_hla_vla_montage(recon_cast_sa, fname)