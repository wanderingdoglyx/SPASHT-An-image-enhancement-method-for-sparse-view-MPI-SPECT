#!/bin/bash

version=2s_ge_NaI
#old
#version=29

job_ind=${1}
lambda_val_ind_mdiff=${2}

num_lambda=10
lambda_val_ind_chdiff=$(( (job_ind - 1) % num_lambda ))
subsample_level_ind=$(( (job_ind - 1) / num_lambda -1))
subsample_level_arr=(
  10
  15
  5
  30
)

subsample_level=${subsample_level_arr[${subsample_level_ind}]}
#echo ${subsample_level}

epochs=250

batch_size_arr=(32)
#source activate tf-gpu2

base_folder=/data01/user-storage/y.zezhang/2024_subsample_project/mod_Neural_network_training ################################################
#learning_folder='den_3d_v'+str(version)
#full_learning_folder=base_folder+'/learning/'

#base_folder=/data/rahman.m/projects/dl_denoising/debug/db_defect_insertion/data_spie/
learning_folder=subsample_3d_v${version} #########################################################
full_learning_folder=${base_folder}/learning/${learning_folder}

for subfolder in weights losses pred
do
  if [[ ! -d $full_learning_folder/${subfolder} ]]
  then
    mkdir -p $full_learning_folder/${subfolder}
    echo "Making dir: $full_learning_folder/${subfolder}"
  fi
done

lambda_val_ind_mdiff_arr=(0 1 2 3 4 5 6 7 8 9)
#for lambda_val_ind_mdiff in ${lambda_val_ind_mdiff_arr[@]}
#do
  for batch_size in ${batch_size_arr[@]}
  do
    arglist=(
      --weights_name wt_v${version}
      --loss_fn_name ls_v${version}
      --base_folder ${base_folder}
      --subsample_level ${subsample_level}
      --num_iter 8
      --batch_size ${batch_size}
      --epochs ${epochs}
      --learning_folder ${learning_folder}
      --lambda_val_ind_chdiff ${lambda_val_ind_chdiff}
      --lambda_val_ind_mdiff ${lambda_val_ind_mdiff}
    )

    echo "python3 train_3Dden_AR_v${version}_custom_loop.py ${arglist[@]}"
    python3 train_3Dden_AR_v${version}_custom_loop.py ${arglist[@]}

  done
#done
