#!/bin/bash
#for i in {0..10}; do echo $i; done
#for i in `seq 0 2 10`; do echo $i; done
#job_ind=${1}
#for job_ind in 58 68

source activate tf_gpu

#for job_ind in 18 11 28 21 38 31;
#for job_ind in 20 19 16 14 12 13;
for job_ind in 30 29 26 24 22 23 40 39 36 34 32 33;
do
#echo $job_ind
  for lambda_val_ind_mdiff in 0
  do
    ./scripts/scr_train_v1_loop_custom.sh ${job_ind} ${lambda_val_ind_mdiff}
    rm core*
    sleep 60s
    ./scripts/scr_retrain_v1_loop_custom.sh ${job_ind} ${lambda_val_ind_mdiff}
    rm core*
    sleep 60s
    ./scripts/scr_test_v1.sh ${job_ind} ${lambda_val_ind_mdiff}
    rm core*
    sleep 60s
    ./scripts/scr_test_mirirv3_v1.sh ${job_ind} ${lambda_val_ind_mdiff}
    rm core*
    sleep 60s
    ./scripts/scr_test_ZT_v1.sh ${job_ind} ${lambda_val_ind_mdiff}
    rm core*
  done
done