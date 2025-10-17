function ze_subsample_s2_window_process_data(category, AC_method, ind_pat, patient_list,slice_number)

    maxNumCompThreads(1);
    
    addpath('src/')
    %%
    seg_dir = '/data01/user-storage/y.zezhang/data_from_zitong_real_patient_project/sa_v3_copy/dependencies'; 
    
    
    pat_id_arr = patient_list;

    pat_range = 1:length(pat_id_arr);
    
    base_res_dir  = ['/data01/user-storage/y.zezhang/2024_subsample_project/mod_SA_images/',slice_number,'/',category,'/'];
    
    
    %%
    N = 128;
    num_pat = length(pat_range);
    res_factor_seg = 4;
    res_factor_reorient = 2;

    %%
    sev_arr = [100,175,250,500];
    ext_arr = [30,60,90];
    loc_arr = {'da'; 'di'};

    
    [X, Y] = meshgrid(1:128);
    %for ind_pat = 1:92%pat_range
    pat_id = pat_id_arr{ind_pat};
    tStart = tic;
    
    if strcmp(category,'healthy')
        try
        last_version = '3';
        load(['center_point_and_mask_test_updated' last_version '.mat'], 'st');
        center_point_arr = st.cp;
        center_slice_arr = st.cs;
        rad_arr = st.R;
        pat_arr = st.pat;
    
        [X, Y] = meshgrid(1:128);
        ind_pat_arr = find(strcmp(pat_arr, string(pat_id)));
        c_LV = center_point_arr(ind_pat_arr, :);
        lv_mask = (X-c_LV(1)).^2 + (Y-c_LV(2)).^2 < rad_arr(ind_pat_arr)^2;
        catch
        fold = [seg_dir '/def_segments/' pat_id];
        fname = [fold, '/_SA_seg_.mat'];
        load(fname);
        c_LV = regionprops(lv_mask, 'centroid');
        c_LV = round(c_LV.Centroid);
        c_LV(3) = c_LV(3) * res_factor_reorient;
        c_LV(2) = c_LV(2) * res_factor_reorient / res_factor_seg;
        c_LV(1) = c_LV(1) * res_factor_reorient / res_factor_seg;
        c_LV = round(c_LV);
    
        lv_mask = imresize3(lv_mask, [N, N, size(lv_mask, 3)*res_factor_reorient], 'Method', 'linear');
        se = strel('square', 4);
        lv_mask = imdilate(lv_mask, se);
        lv_mask = lv_mask > 0;
        end
    

            
        %def_name = append(def_loc,'21', num2str(def_ext) ,'s',num2str(def_sev));
    
        def_name='hl';
        %% read sa 3d image
        fname = fullfile(base_res_dir, pat_id, AC_method, def_name, 'reoriented.img');
        recon_sa = my_fread(fname, inf, 'float32');
        num_slices = length(recon_sa)/N^2;
        recon_sa = reshape(recon_sa, [N, N, num_slices]);

        fname = [seg_dir,'/def_center/',pat_id,'/def_centroid_','dl2130','_mod.bin'];

        f = fopen(fname);
        if f < 0
            fname = [seg_dir,'/def_center/',pat_id,'/def_centroid_','da2130','_mod.bin'];
            f = fopen(fname);
        end

        %%%%%%%%%%%%%%%%%%%%%%

        
        assert(f > 0);
        def_c = fread(f,'float32');
        fclose(f);

        recon_sa = process_overlapped_train(recon_sa, lv_mask, c_LV);

        cur_fold = fullfile(base_res_dir, pat_id, AC_method, def_name);
        if ~isfolder(cur_fold); mkdir(cur_fold); end

        fname = fullfile(cur_fold, ...
                        ['reoriented_windowed.img']);
        my_fwrite(fname, recon_sa, 'float32');
        
        %% first window
        Nx = 32; 
        Ny = 32;
        Nz = 32;

        
        zero_pad = 5;
        recon_sa = padarray(recon_sa,[zero_pad zero_pad zero_pad],0);
        recon_sa = recon_sa(def_c(2)-Ny/2+1+zero_pad:def_c(2)+Ny/2+zero_pad, ...
                            def_c(1)-Nx/2+1+zero_pad:def_c(1)+Nx/2+zero_pad, ...
                            def_c(3)-Nz/2+1+zero_pad:def_c(3)+Nz/2+zero_pad);


        fname = fullfile(cur_fold, ['reoriented_windowed_MO.img']);
        my_fwrite(fname, recon_sa, 'float32');
            

    
    else

        fold = [seg_dir '/def_segments/' pat_id];
        fname = [fold, '/_SA_seg_.mat'];
        load(fname);
        c_LV = regionprops(lv_mask, 'centroid');
        c_LV = round(c_LV.Centroid);
        c_LV(3) = c_LV(3) * res_factor_reorient;
        c_LV(2) = c_LV(2) * res_factor_reorient / res_factor_seg;
        c_LV(1) = c_LV(1) * res_factor_reorient / res_factor_seg;
        c_LV = round(c_LV);
        
        lv_mask = imresize3(lv_mask, [N, N, size(lv_mask, 3)*res_factor_reorient], 'Method', 'linear');
        se = strel('square', 4);
        lv_mask = imdilate(lv_mask, se);
        lv_mask = lv_mask > 0;
        
        for ind_loc = 1:length(loc_arr)
            def_loc = loc_arr{ind_loc};
            for def_ext = ext_arr
            for def_sev = sev_arr
                %def_name = [def_loc '_' num2str(def_ext) '_' num2str(def_sev)];
                def_name = append(def_loc,'21', num2str(def_ext) ,'s',num2str(def_sev));
                %% read sa 3d image
                fname = fullfile(base_res_dir, pat_id, AC_method, def_name, 'reoriented.img');
                recon_sa = my_fread(fname, inf, 'float32');
                num_slices = length(recon_sa)/N^2;
                recon_sa = reshape(recon_sa, [N, N, num_slices]);
        
                fname = [seg_dir,'/def_center/',pat_id,'/def_centroid_',def_loc,'21',num2str(def_ext),'_mod.bin'];
                f = fopen(fname);
                if f < 0
                fname = [seg_dir,'/def_center/',pat_id,'/def_centroid_',def_loc,'21',num2str(def_ext),'.bin'];
                f = fopen(fname);
                end
                def_c = fread(f,'float32');
                fclose(f);
        
                recon_sa = process_overlapped_train(recon_sa, lv_mask, c_LV);
        
                cur_fold = fullfile(base_res_dir, pat_id, AC_method, def_name);
        
                fname = fullfile(cur_fold, ...
                                ['reoriented_windowed.img']);
                my_fwrite(fname, recon_sa, 'float32');
                
                %% first window 
                Nx = 32; 
                Ny = 32;
                Nz = 32;
 
                
                zero_pad = 5;
                %zero_pad = 8;
              
                recon_sa = padarray(recon_sa,[zero_pad zero_pad zero_pad],0);
                recon_sa = recon_sa(def_c(2)-Ny/2+1+zero_pad:def_c(2)+Ny/2+zero_pad, ...
                                    def_c(1)-Nx/2+1+zero_pad:def_c(1)+Nx/2+zero_pad, ...
                                    def_c(3)-Nz/2+1+zero_pad:def_c(3)+Nz/2+zero_pad);
        
                fname = fullfile(cur_fold, ['reoriented_windowed_MO.img']);
                my_fwrite(fname, recon_sa, 'float32');
                
                
            end
            end
        end
    end
    fprintf('Progress: %d/%d || pat: %s || AC: %s || ET: %.4f\n', ind_pat, num_pat, pat_id,AC_method,toc(tStart));
        
    
    % %% calculate centroid
    % % if str2num(pat_id) >= 41571338 && strcmp(category,'healthy')
    % % if strcmp(category,'healthy')
      
    %   last_version = '3';
    %   load(['center_point_and_mask_test_updated' last_version '.mat'], 'st');
    %   center_point_arr = st.cp;
    %   center_slice_arr = st.cs;
    %   rad_arr = st.R;
    %   pat_arr = st.pat;
    
    %   [X, Y] = meshgrid(1:128);
    %   ind_pat_arr = find(strcmp(pat_arr, string(pat_id)));
    %   c_LV = center_point_arr(ind_pat_arr, :);
    %   lv_mask = (X-c_LV(1)).^2 + (Y-c_LV(2)).^2 < rad_arr(ind_pat_arr)^2;
    
    
    
    %   % [X, Y] = meshgrid(1:128);
    
    %   % c_LV = center_point_arr(ind_pat, :);
    
    %   % lv_mask = (X-c_LV(1)).^2 + (Y-c_LV(2)).^2 < rad_arr(ind_pat)^2;
    %   try
    %     fold = [seg_dir '/def_segments/' pat_id];
    %     fname = [fold, '/_SA_seg_.mat'];
    %     load(fname);
    %     lv_mask = imresize3(lv_mask, [N, N, size(lv_mask, 3)*res_factor_reorient], 'Method', 'linear');
    %     se = strel('square', 4);
    %     lv_mask = imdilate(lv_mask, se);
    %     lv_mask = lv_mask > 0;
    %   catch
    %     [X, Y] = meshgrid(1:128);
    %     ind_pat_arr = find(strcmp(pat_arr, string(pat_id)));
    %     c_LV = center_point_arr(ind_pat_arr, :);
    %     lv_mask = (X-c_LV(1)).^2 + (Y-c_LV(2)).^2 < rad_arr(ind_pat_arr)^2;
    %   end
    
    
    %   c_def_matrix = zeros(3,4);
    %   k = 1;
    %   for ind_loc = 1:length(loc_arr)
    %     def_loc = loc_arr{ind_loc};
    %     for def_ext = ext_arr
    %       fname = ['/data01/user-storage/zitong/data/cardiac_trainsmission_less/patient_study/src/sa_v3/dependencies/def_center/',pat_id,'/def_centroid_',def_loc,'21',num2str(def_ext),'_mod_again5.bin'];
    %       f = fopen(fname);
    %       if f < 0
    %         fname = ['/data01/user-storage/zitong/data/cardiac_trainsmission_less/patient_study/src/sa_v3/dependencies/def_center/',pat_id,'/def_centroid_',def_loc,'21',num2str(def_ext),'_mod_apr3.bin'];
    %         f = fopen(fname);
    %       end
    %       assert(f > 0);
    %       def_c = fread(f,'float32')'-1;
    %       fclose(f);
    %       % c_def = [def_c(1),def_c(2),0]-[23,23,0]+c_def;
    %       c_def_matrix(:,k) = round(def_c);
    %       k = k + 1;
    %     end
    %   end

    
    % else 
    
    %   fold = [seg_dir '/def_segments/' pat_id];
    %   fname = [fold, '/_SA_seg_.mat'];
    %   load(fname);
    %   c_def = regionprops(lv_mask, 'centroid');
    %   c_def = round(c_def.Centroid);
    %   c_def(3) = c_def(3) * res_factor_reorient;
    %   c_def(2) = c_def(2) * res_factor_reorient / res_factor_seg;
    %   c_def(1) = c_def(1) * res_factor_reorient / res_factor_seg;
    %   c_def = round(c_def);
    
    %   lv_mask = imresize3(lv_mask, [N, N, size(lv_mask, 3)*res_factor_reorient], 'Method', 'linear');
    %   se = strel('square', 4);
    %   lv_mask = imdilate(lv_mask, se);
    %   lv_mask = lv_mask > 0;
    
    %   c_def_matrix = zeros(3,4);
    %   k = 1;
    %   loc_arr_ = {'Ant'; 'Inf';};
    %   for ind_loc = 1:length(loc_arr_)
    %     def_loc = loc_arr_{ind_loc};
    %     for def_ext = ext_arr
    
    %       fold = [seg_dir '/def_segments_mirirv3/' pat_id];
    %       fname = [fold, '/_SA_def_',def_loc,'Z21D',num2str(def_ext),'_.mat'];
    %       load(fname);
    %       c_def = regionprops(def_mask, 'centroid');
    %       c_def = round(c_def.Centroid);
    %       c_def(3) = c_def(3) * res_factor_reorient;
    %       c_def(2) = c_def(2) * res_factor_reorient / res_factor_seg;
    %       c_def(1) = c_def(1) * res_factor_reorient / res_factor_seg;
    %       c_def = round(c_def);
    %       c_def_matrix(:,k) = c_def;
    %       k = k + 1;
    %     end
    %   end
    % end
    
    % k = 1;
    % for ind_loc = 1:length(loc_arr)
    %   def_loc = loc_arr{ind_loc};
    %   for def_ext = ext_arr
    %     for def_sev = sev_arr
    %       def_name = [def_loc '_' num2str(def_ext) '_' num2str(def_sev)];
    %       %% read sa 3d image
    %       try
    %         fname = fullfile(base_res_dir, pat_id, AC_method, def_name, 'reoriented.img');
    %         recon_sa = my_fread(fname, inf, 'float32');
    %         num_slices = length(recon_sa)/N^2;
    %         recon_sa = reshape(recon_sa, [N, N, num_slices]);
    %       catch
    %         fprintf('reorientation failed: %s\n', fname);
    %         continue;
    %       end
          
    %       %% select center slice
    %       c_def = c_def_matrix(:,k);
    %       recon_sa = process_overlapped_train(recon_sa, lv_mask, c_def);
    %       cur_fold = fullfile(base_res_dir, pat_id, AC_method, def_name);
    %       if ~isfolder(cur_fold); mkdir(cur_fold); end
    %       fname = fullfile(cur_fold, ...
    %                       ['reoriented_windowed_MO.img']);
    %       my_fwrite(fname, recon_sa, 'float32');
          
    %     end
    %     k = k + 1;
    %   end
    % end
    
    end
                  
    