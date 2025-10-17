clear,clc

subsample_level={'10'};

save_path_base='/datastore01/user-storage/y.zezhang/image_inspect/images';

%sa_folder='/data01/user-storage/y.zezhang/2024_subsample_project/mod_SA_images';
%projection_folder='/data01/user-storage/y.zezhang/2024_subsample_project/mod_subsample_projection';
%submission_folder='/data01/user-storage/y.zezhang/2024_subsample_project/observer_study/pilot_study/all_submission';

sa_folder_base='/data01/user-storage/y.zezhang/2024_subsample_project/mod_SA_images';
projection_folder_base='/data01/user-storage/y.zezhang/2024_subsample_project/mod_subsample_projection';
submission_folder='/datastore01/user-storage/y.zezhang/image_inspect/images/all_submission';

GE_file='GE_MIR.txt';

nn_version='2s500';

%observer_study_path='/data01/user-storage/y.zezhang/2024_subsample_project/document/observer_study_patient_list';

%hl_patient=append(observer_study_path,'/pat_id_healthy_pilot.txt');
%def_patient=append(observer_study_path,'/pat_id_diseased_pilot_defect_selected.txt');

%observer_study_path='/data01/user-storage/y.zezhang/2024_subsample_project/document/observer_study_patient_list';
observer_study_path='/datastore01/user-storage/y.zezhang/image_inspect/observer_study_patient_list';

hl_patient=append(observer_study_path,'/pat_id_healthy_pilot.txt');
def_patient=append(observer_study_path,'/pat_id_diseased_pilot_defect_selected.txt');

%hl_patient=append(observer_study_path,'/healthy patient pilot.txt');
%def_patient=append(observer_study_path,'/diseased patient pilot.txt');

fid = fopen(hl_patient,'rt');
hl_image_select = readlines(hl_patient,"EmptyLineRule","skip");
fclose(fid);

fid = fopen(def_patient,'rt');
def_image_select = readlines(def_patient,"EmptyLineRule","skip");
fclose(fid);


split_data = split(def_image_select, ' ');

def_pat = split_data(:, 1);  % First column
def_type = split_data(:, 2);  % Second column

%%%%%%%%%%%%%%%%%%%%%%%%%%%%% nn sertting %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

lmbdchdiff_settings={'0','7'};
%lmbdchdiff_settings={'7'};

for lmbdchdiff_index=1:1:length(lmbdchdiff_settings)
    lmbdchdiff=lmbdchdiff_settings{lmbdchdiff_index};

    for i=1:1:length(hl_image_select)
        for dose_index=1:1:length(subsample_level)
            subsample_cur=subsample_level{dose_index};

            nn_folder_name=append('subsample_3d_v',nn_version,'_d',subsample_cur,'_lmbdchdiff',lmbdchdiff,'_nn');

            sa_folder=fullfile(sa_folder_base, nn_folder_name);
            projection_folder=fullfile(projection_folder_base,subsample_level);

            pat_No=hl_image_select(i);
            pat_folder=fullfile(sa_folder,'healthy',pat_No);
            pat_filefolder=fullfile(pat_folder,'CTAC','hl');


            nn_save_folder=append(subsample_cur,'_lmbdchdiff',lmbdchdiff,'_nn');

            mkdir(fullfile(save_path_base,nn_save_folder,'grey_scale','hl'));
            mkdir(fullfile(save_path_base,nn_save_folder,'ge','hl'));

            %%%%%%%%%%%% projection %%%%%%%%%%%%%% 

            try
                projection_folder_cur= fullfile(projection_folder,pat_No);
                pri_file=append(pat_No,'.a00');
                pri_file_path=fullfile(projection_folder_cur,pri_file);

                dims=[64,64,str2num(subsample_cur)];

                gif_filename=append('pat',pat_No,'_d',subsample_cur,'_lmbdchdiff',lmbdchdiff,'_nn','.gif');
                gif_file_save_path=fullfile(save_path_base,nn_save_folder,'grey_scale','hl',gif_filename);
                delay_time=0.1*(30/str2num(subsample_cur));

                createGifFromBinary(pri_file_path, dims, gif_file_save_path, delay_time)
            catch
                projection_folder_cur= fullfile(projection_folder,pat_No);
                pri_file=append('orig_proj_hl_',pat_No,'_d1.a00');
                pri_file_path=fullfile(projection_folder_cur,pri_file);

                dims=[64,64,str2num(subsample_cur)];

                gif_filename=append('pat',pat_No,'_d',subsample_cur,'_lmbdchdiff',lmbdchdiff,'_nn','.gif');
                gif_file_save_path=fullfile(save_path_base,nn_save_folder,'grey_scale','hl',gif_filename);
                delay_time=0.1*(30/str2num(subsample_cur));

                createGifFromBinary(pri_file_path, dims, gif_file_save_path, delay_time)
            end

            
            lowdose=append('extended_reoriented_windowed.img');
            lowdose_file_dir=fullfile(pat_filefolder,lowdose);  
            copyfile(lowdose_file_dir);
    

            save_filename_path=fullfile(save_path_base,nn_save_folder,'grey_scale','hl');
            png_save_name=append('pat',pat_No,'_d',subsample_cur,'_lmbdchdiff',lmbdchdiff,'_nn');
            generate_image_series_v2_png_only(lowdose,save_filename_path,png_save_name);
            


            %%%%%%%%%%%% convert to ge %%%%%%%%%%%%%%%%%%%%%%%%% 

            lowdose_png=append(png_save_name,'.png');
        
            grey_load_filename_path_lowdose=fullfile(save_filename_path,lowdose_png);
            ge_save_filename_path_lowdose=fullfile(save_path_base,nn_save_folder,'ge','hl',lowdose_png);


            GE_converter(grey_load_filename_path_lowdose,GE_file,ge_save_filename_path_lowdose);
        

            submission_folder_hl=fullfile(submission_folder,'hl');

            if ~exist(submission_folder_hl, 'dir')
                mkdir(submission_folder_hl);
                disp(['Folder created: ', submission_folder_hl]);
            end

            
            copyfile(grey_load_filename_path_lowdose,submission_folder_hl);
            copyfile(gif_file_save_path,submission_folder_hl);


        end
    end



    for i=1:1:length(def_image_select)
        for dose_index=1:1:length(subsample_level)


            subsample_cur=subsample_level{dose_index};

            nn_folder_name=append('subsample_3d_v',nn_version,'_d',subsample_cur,'_lmbdchdiff',lmbdchdiff,'_nn');

            sa_folder=fullfile( sa_folder_base, nn_folder_name);
            projection_folder=fullfile(projection_folder_base,subsample_level);

            pat_No=def_pat(i);
            pat_folder=fullfile(sa_folder,'diseased',pat_No);
            def_type_cur=def_type{i};
            pat_filefolder=fullfile(pat_folder,'CTAC',def_type_cur);
            
            nn_save_folder=append(subsample_cur,'_lmbdchdiff',lmbdchdiff,'_nn');

            mkdir(fullfile(save_path_base,nn_save_folder,'grey_scale',def_type_cur));
            mkdir(fullfile(save_path_base,nn_save_folder,'ge',def_type_cur))


            %%%%%%%%%%%% projection %%%%%%%%%%%%%% 
            try
                projection_folder_cur= fullfile(projection_folder,pat_No);
                pri_file=append('mod_proj_',def_type_cur,'_obj_',pat_No,'_d1.a00');
                pri_file_path=fullfile(projection_folder_cur,pri_file);

                dims=[64,64,str2num(subsample_cur)];
                
                gif_filename=append('pat',pat_No,'_d',subsample_cur,'_',def_type_cur,'_lmbdchdiff',lmbdchdiff,'_nn','.gif');
                gif_file_save_path=fullfile(save_path_base,nn_save_folder,'grey_scale',def_type_cur,gif_filename);

                delay_time=0.1*(30/str2num(subsample_cur));

                createGifFromBinary(pri_file_path, dims, gif_file_save_path, delay_time)
            catch
                projection_folder_cur= fullfile(projection_folder,pat_No);
                pri_file=append('mod_proj_',def_type_cur,'_obj_',pat_No,'.a00');
                pri_file_path=fullfile(projection_folder_cur,pri_file);

                dims=[64,64,str2num(subsample_cur)];

                gif_filename=append('pat',pat_No,'_d',subsample_cur,'_',def_type_cur,'_lmbdchdiff',lmbdchdiff,'_nn','.gif');
                gif_file_save_path=fullfile(save_path_base,nn_save_folder,'grey_scale',def_type_cur,gif_filename);
                delay_time=0.1*(30/str2num(subsample_cur));

                createGifFromBinary(pri_file_path, dims, gif_file_save_path, delay_time)
            end

                        
            lowdose=append('extended_reoriented_windowed.img');
            lowdose_file_dir=fullfile(pat_filefolder,lowdose);

    
            copyfile(lowdose_file_dir);

            save_filename_path=fullfile(save_path_base,nn_save_folder,'grey_scale',def_type_cur);

            png_save_name=append('pat',pat_No,'_d',subsample_cur,'_',def_type_cur,'_lmbdchdiff',lmbdchdiff,'_nn');
            
            generate_image_series_v2_png_only(lowdose,save_filename_path,png_save_name);

            %%%%%%%%%%%% convert to ge %%%%%%%%%%%%%%%%%%%%%%%%%

            lowdose_png=append(png_save_name,'.png');

            grey_load_filename_path_lowdose=fullfile(save_filename_path,lowdose_png);
            ge_save_filename_path_lowdose=fullfile(save_path_base,nn_save_folder,'ge',def_type_cur,lowdose_png);


            GE_converter(grey_load_filename_path_lowdose,GE_file,ge_save_filename_path_lowdose);
        

            submission_folder_def=fullfile(submission_folder,'def');
            if ~exist(submission_folder_def, 'dir')
                mkdir(submission_folder_def);
                disp(['Folder created: ', submission_folder_def]);
            end

            
            copyfile(grey_load_filename_path_lowdose,submission_folder_def);
            copyfile(gif_file_save_path,submission_folder_def);

            

        end
    end
end
