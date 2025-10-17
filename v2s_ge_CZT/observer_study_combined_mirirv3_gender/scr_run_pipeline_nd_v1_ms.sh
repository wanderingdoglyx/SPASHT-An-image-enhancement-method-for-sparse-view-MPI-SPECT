#!/bin/bash
for gender in M F
do
for Ud in 64
do
  for dose_level in {1..8}
  do
    for isIO in 1
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
done
done
