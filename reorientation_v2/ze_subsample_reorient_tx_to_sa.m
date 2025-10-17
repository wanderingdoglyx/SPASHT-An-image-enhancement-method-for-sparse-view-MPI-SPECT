function recon_sa = ze_subsample_reorient_tx_to_sa(...
        pat_id, fdir_base, recon_tx, res_factor, ...
        flag_filter, filter)

    %% read original SA reconstruction
    try
        series_desc_sa_recon = '_SA.DS_';
        fdir = [fullfile(fdir_base, 'all_recon_sa_mirirv3') filesep]; 
        %'/data01/user-storage/zitong/data/cardiac_trainsmission_less/patient_study/src/sa_v3/dependencies/all_recon_sa_mirirv3/'
        S = get_dir(fdir, series_desc_sa_recon, pat_id);
    catch
        fdir = [fullfile('/data02/user-storage/y.zezhang/zitong_file/cardiac_trainsmission_less/patient_study/src/sa/dependencies/', 'all_recon_sa_v3') filesep];
        %'/data01/user-storage/zitong/data/cardiac_trainsmission_less/patient_study/src/sa/dependencies/all_recon_sa_v3/'
        S = get_dir(fdir, 'Short.Axis.ReconSA', pat_id);
    end
    
    S_dcm = dir(fullfile([fdir, S],'*.dcm')); %
    S_dcm = S_dcm(1).name;
    fname = [fdir, S, filesep, S_dcm];

    di_sa = dicominfo(fname);

    %% read original primary reconstruction
    try
        fdir = [fullfile(fdir_base, 'recon_prim_mirirv3') filesep];
        S = get_dir(fdir, '_ReconPrimDS_', pat_id);
    catch
        fdir = [fullfile('/data02/user-storage/y.zezhang/zitong_file/cardiac_trainsmission_less/patient_study/src/sa/dependencies/', 'recon_prim') filesep];
        S = get_dir(fdir, 'ReconPrim', pat_id);
    end
    S_dcm = dir(fullfile([fdir, S],'*.dcm'));
    S_dcm = S_dcm(1).name;
    fname = [fdir, S, filesep, S_dcm];

    di_tx = dicominfo(fname);

    %% filter, align
    if (flag_filter)
        recon_tx = MyButterWorth3D(...
        filter.order, filter.cutoff_freq, recon_tx, filter.type);
    end
    recon_sa = align_in_sa_from_tx_hr(recon_tx, di_sa, di_tx, res_factor);

end
