#!/bin/bash
source activate myenv
dose_level=${1}
for Ud in 64
do
  for isIO in 0
  do
    start=$(date +%s)
    echo "=================================================================================="
    echo "python3 pipeline_nd_v1_ms.py --Ud ${Ud} --dose_level ${dose_level} --isIO ${isIO}"
    echo "=================================================================================="
    python3 pipeline_nd_v1_ms.py --Ud ${Ud} --dose_level ${dose_level} --isIO ${isIO}
    end=$(date +%s)
    echo "Elapsed Time: $(($end-$start)) seconds"
  done
done
