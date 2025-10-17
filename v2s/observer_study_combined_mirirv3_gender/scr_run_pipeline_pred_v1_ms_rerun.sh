#!/bin/bash

dl_version=28
batch_size=32
dose_level=${1}

lambda_val_ind_mdiff=0
lambda_val_ind_chdiff=${2}

for gender in M F
do
for Ud in 64
do
  for isIO in 1
  do
    start=$(date +%s)
    echo "=================================================================================="
    echo "python3 pipeline_pred_v1_ms_rerun.py --dl_version ${dl_version} --Ud ${Ud} --dose_level ${dose_level} --isIO ${isIO} --batch_size ${batch_size} --lambda_val_ind_chdiff ${lambda_val_ind_chdiff} --lambda_val_ind_mdiff ${lambda_val_ind_mdiff} --gender ${gender}"
    echo "=================================================================================="
    python3 pipeline_pred_v1_ms_rerun.py --dl_version ${dl_version} --Ud ${Ud} --dose_level ${dose_level} --isIO ${isIO} --batch_size ${batch_size} --lambda_val_ind_chdiff ${lambda_val_ind_chdiff} --lambda_val_ind_mdiff ${lambda_val_ind_mdiff} --gender ${gender}
    end=$(date +%s)
    echo "Elapsed Time: $(($end-$start)) seconds"
  done
done
done
