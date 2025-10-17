#!/bin/bash

source activate tf-gpu2

dl_version=28
batch_size=32
job_ind=${1}
dose_level_arr=(4 5 6 7 8 4 5 6 7 8 7)

ch_arr_CHO=(9 7 9 3 4 0 0 0 0 0 9)

dose_level=${dose_level_arr[$(( job_ind-1 ))]}
lambda_val_ind_mdiff=0
lambda_val_ind_chdiff=${ch_arr_CHO[$(( job_ind-1 ))]}

for Ud in 64
do
  for isIO in 0
  do
    start=$(date +%s)
    echo "=================================================================================="
    echo "python3 pipeline_pred_v1_ms.py --dl_version ${dl_version} --Ud ${Ud} --dose_level ${dose_level} --isIO ${isIO} --batch_size ${batch_size} --lambda_val_ind_chdiff ${lambda_val_ind_chdiff} --lambda_val_ind_mdiff ${lambda_val_ind_mdiff}"
    echo "=================================================================================="
    python3 pipeline_pred_v1_ms.py --dl_version ${dl_version} --Ud ${Ud} --dose_level ${dose_level} --isIO ${isIO} --batch_size ${batch_size} --lambda_val_ind_chdiff ${lambda_val_ind_chdiff} --lambda_val_ind_mdiff ${lambda_val_ind_mdiff}
    end=$(date +%s)
    echo "Elapsed Time: $(($end-$start)) seconds"
  done
done
