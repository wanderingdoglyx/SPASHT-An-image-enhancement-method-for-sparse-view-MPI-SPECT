#!/bin/bash

dl_version=28
batch_size=32
dose_level=${1}

lambda_val_ind_mdiff=0
lambda_val_ind_chdiff=${2}

for ext_ind in 0 1 2 3
do
for Ud in 64
do
for isIO in 1 0
do
  echo "=================================================================================="
  echo "python3 pipeline_pred_v1_ms_rerun.py --dl_version ${dl_version} --Ud ${Ud} --dose_level ${dose_level} --isIO ${isIO} --batch_size ${batch_size} --lambda_val_ind_chdiff ${lambda_val_ind_chdiff} --lambda_val_ind_mdiff ${lambda_val_ind_mdiff} --ext_ind ${ext_ind}"
  echo "=================================================================================="
  python3 pipeline_pred_v1_ms_rerun.py --dl_version ${dl_version} --Ud ${Ud} --dose_level ${dose_level} --isIO ${isIO} --batch_size ${batch_size} --lambda_val_ind_chdiff ${lambda_val_ind_chdiff} --lambda_val_ind_mdiff ${lambda_val_ind_mdiff} --ext_ind ${ext_ind}
done
done
done
