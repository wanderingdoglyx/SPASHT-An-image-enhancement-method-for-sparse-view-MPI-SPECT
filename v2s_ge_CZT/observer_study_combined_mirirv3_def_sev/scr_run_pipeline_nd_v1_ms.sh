#!/bin/bash
for sev_ind in 0 1 2
do
for Ud in 64
do
  for dose_level in {1..8}
  do
    for isIO in 1
    do
      echo "=================================================================================="
      echo "python3 pipeline_nd_v1_ms.py --Ud ${Ud} --dose_level ${dose_level} --isIO ${isIO} --sev_ind ${sev_ind}"
      echo "=================================================================================="
      python3 pipeline_nd_v1_ms.py --Ud ${Ud} --dose_level ${dose_level} --isIO ${isIO} --sev_ind ${sev_ind}
    done
  done
done
done
