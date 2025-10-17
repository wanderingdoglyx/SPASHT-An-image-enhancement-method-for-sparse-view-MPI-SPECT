#!/bin/bash
source activate myenv

job_ind=${1}
num_dose=8
ext_ind=$(( (job_ind-1)/num_dose ))
dose_level=$(( (job_ind-1)%num_dose + 1 ))

for Ud in 64
do
  for isIO in 0
  do
    echo "=================================================================================="
    echo "python3 pipeline_nd_v1_ms.py --Ud ${Ud} --dose_level ${dose_level} --isIO ${isIO} --ext_ind ${ext_ind}"
    echo "=================================================================================="
    python3 pipeline_nd_v1_ms.py --Ud ${Ud} --dose_level ${dose_level} --isIO ${isIO} --ext_ind ${ext_ind}
  done
done
