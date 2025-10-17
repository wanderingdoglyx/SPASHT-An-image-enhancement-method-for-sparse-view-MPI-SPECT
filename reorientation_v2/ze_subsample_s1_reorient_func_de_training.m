function ze_subsample_s1_reorient_func_de_training(patient_list,def_name, AC_method, category,slice_number)


    tStart = tic;
    addpath('src/')

    fdir_base = '/data01/user-storage/y.zezhang/data_from_zitong_real_patient_project/sa_v3_copy/dependencies/';

    %% folder setup

    %base_res_dir = ['/data01/user-storage/y.zezhang/2024_subsample_project/reconstruction/' ,AC_method,'/10','/'];
    base_res_dir = ['/data01/user-storage/y.zezhang/2024_subsample_project/mod_reconstruction/' ,slice_number,'/',AC_method,'/'];
    base_save_dir = ['/data01/user-storage/y.zezhang/2024_subsample_project/mod_SA_images/',slice_number,'/',category,'/'];


    %% read patients list

    pat_id_arr = patient_list;
    
    %% param setup
    N = 64;
    num_iter = 8;
    %def_name = 'hl';
    bt_size = 16;
    res_factor = 2;
        
    if strcmp(slice_number, '30')    
        flag_filter = 1;
    else
        flag_filter = 0;
    end

    %flag_filter = 0;
    filter.type = 'lp';
    filter.cutoff_freq = 0.3;
    filter.order = 5;
    
    pred_shape = [64, 64, 64];
    
    %% read each patient, reorient and save
    for ind_pat = 1:length(pat_id_arr)
        pat_id = pat_id_arr{ind_pat};

        if strcmp(category, 'healthy')
    
            pat_name=[pat_id,'_it8.img'];


        elseif strcmp(category, 'diseased')

            pat_name=['mod_proj_',def_name,'_obj_',pat_id,'_d1_it8.img'];

        end
            %pat_id = pat_id_arr{1};

            fname = fullfile(base_res_dir, pat_id, pat_name ); %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            recon_tx = my_fread(fname, inf, 'float32');
            recon_tx = reshape(recon_tx, [64, 64, 64]);
            recon_tx = process_castor_recon(recon_tx);

            %% reorient
            recon_sa = ze_subsample_reorient_tx_to_sa_de_training(pat_id, fdir_base, recon_tx, res_factor, ...
            flag_filter, filter);
            
            %% save
            reori_folder_save = fullfile(base_save_dir, pat_id, AC_method, def_name);
            if ~isfolder(reori_folder_save)
                mkdir(reori_folder_save);
            end


            fname = fullfile(reori_folder_save, 'reoriented.img');
            my_fwrite(fname, recon_sa, 'float32');
            
            fprintf('ind_pat: %d || def_name: %s || AC: %s\n', ind_pat, def_name,AC_method);
        

    end
end
