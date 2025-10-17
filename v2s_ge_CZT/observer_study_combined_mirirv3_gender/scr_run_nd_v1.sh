#!/bin/bash

source activate myenv
job_ind=${1}

genders=(M F)
num_dose=8
dose_level=$(( (job_ind-1)%num_dose + 1 ))
gender_id=$(( (job_ind-1)/num_dose ))
gender=${genders[$gender_id]}

for Ud in 64
do
  for isIO in 0
  do
    start=$(date +%s)
    echo "=================================================================================="
    echo "python3 pipeline_nd_v1_ms.py --Ud ${Ud} --dose_level ${dose_level} --isIO ${isIO} --gender ${gender}"
    echo "=================================================================================="
    python3 pipeline_nd_v1_ms.py --Ud ${Ud} --dose_level ${dose_level} --isIO ${isIO} --gender ${gender}
    end=$(date +%s)
    echo "Elapsed Time: $(($end-$start)) seconds"
  done
done
