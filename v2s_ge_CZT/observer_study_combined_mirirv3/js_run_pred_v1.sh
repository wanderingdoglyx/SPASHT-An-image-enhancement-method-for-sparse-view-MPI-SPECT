#!/bin/bash

#BSUB -q general
#BSUB -G compute-a.jha
#BSUB -R "rusage[mem=24GB]"
#BSUB -g /rahman.m/a.jha
#BSUB -J DBLR_DN28_PP_OS_PRED2[8-11]
#BSUB -o /scratch1/fs1/a.jha/asheq/adaptive_spect/job_outputs/DBLR_DN28_PP_OS_PRED2.%I.out
#BSUB -e /scratch1/fs1/a.jha/asheq/adaptive_spect/job_outputs/DBLR_DN28_PP_OS_PRED2.%I.err
#BSUB -a 'docker(asheq/joint_recon:fs4_learning_tf22)'

./scr_run_pred_v1.sh ${LSB_JOBINDEX}
