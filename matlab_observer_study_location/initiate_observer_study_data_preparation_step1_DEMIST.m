clear,clc

save_path_base='/data01/user-storage/y.zezhang/2024_false_defect_project/location_test_di/DEMIST';
sa_folder='/data01/user-storage/y.zezhang/data_for_zezhang_mar29/learning/den_3d_v28/pred';
projection_folder='/data01/user-storage/y.zezhang/data_from_zitong_real_patient_project/reg_PriPrj_ScaPrj_RegCT_DICOM';
submission_folder='/data01/user-storage/y.zezhang/2024_false_defect_project/location_test_di/all_submission';

GE_file='GE_MIR.txt';
%defect_setting=['da','di'];
%serverity_setting=[100,175,250];
%extend_setting=[30,45,60,90];
total_projection_files_list=dir(projection_folder);
total_projection_fileNames = [];
% Loop through the list and filter out directories
for i = 1:length(total_projection_files_list)
    % Get the name of the item
    itemName = total_projection_files_list(i).name;

    % Skip the '.' and '..' directories
    if strcmp(itemName, '.') || strcmp(itemName, '..')
        continue;
    end

    total_projection_fileNames = [total_projection_fileNames; string(itemName)];

end

% Display the file names
%disp('Files found in the folder:');
%disp( total_projection_fileNames);


dose={'d1'};
%defect_setting={'da'};
defect_setting={'di'};
%extend_setting={'30'};
extend_setting={'60','90'};
serverity_setting={'250'};
lmbdchdiff_setting={'6'};

rng(76);

hl_patient='hl_patient_list.txt';
def_patient='def_patient_list.txt';

fid = fopen(hl_patient,'rt');
hl_image_select = readlines(hl_patient,"EmptyLineRule","skip");
fclose(fid);

fid = fopen(def_patient,'rt');
def_image_select = readlines(def_patient,"EmptyLineRule","skip");
fclose(fid);



for i=1:1:length(hl_image_select)
    pat_No=hl_image_select(i);
    %pat_folder=fullfile(sa_folder,pat_No);
    pat_filefolder=fullfile(sa_folder,'hl');

    
    mkdir(fullfile(save_path_base,'grey_scale','hl'));
    mkdir(fullfile(save_path_base,'ge','hl'));

    for j=1:1:length(total_projection_fileNames)

        pri_file_cur=total_projection_fileNames(j);
        TF_No =  contains(pri_file_cur, pat_No);
        if TF_No ==1
            TF_PriPrj =  contains(pri_file_cur, 'PriPrj');
            if TF_PriPrj ==1
                pri_file_folder = fullfile(projection_folder,pri_file_cur);

                two_subfile=dir(pri_file_folder);

                for k = 1:length(two_subfile)

                    % Get the name of the item
                    pri_itemName = two_subfile(k).name;
                
                    % Skip the '.' and '..' directories
                    if strcmp( pri_itemName, '.') || strcmp( pri_itemName, '..')
                        continue;
                    end

                    is_pri_file =  contains( pri_itemName, 'dcm');

                    if is_pri_file==1
                        pri_file=fullfile(pri_file_folder, pri_itemName);
                        cur_pri_file_name=pri_itemName;
                        copyfile(pri_file)
                    end
               
                end

            end
        end    

    end


    for dose_index=1:1:length(dose)
        dose_cur=dose{dose_index};

        for lmbdchdiff_index=1:1:length(lmbdchdiff_setting)
            lmbdchdiff=lmbdchdiff_setting{lmbdchdiff_index};
                
            DEMIST_lowdose=append('recon_pat',pat_No,'_hl_',dose_cur,'_it8_b32_lmbdchdiff',lmbdchdiff,'_lmbdmdiff0.img');
           

            DEMIST_lowdose_file_dir=fullfile(pat_filefolder,DEMIST_lowdose);
            

            copyfile(DEMIST_lowdose_file_dir);
            
            %

            save_filename_path=fullfile(save_path_base,'grey_scale','hl');
            save_dcm_file_path=fullfile(save_path_base,'grey_scale','hl');


            generate_image_series(DEMIST_lowdose,cur_pri_file_name,save_filename_path,save_dcm_file_path);
           


            DEMIST_lowdose_png=append('recon_pat',pat_No,'_hl_',dose_cur,'_it8_b32_lmbdchdiff',lmbdchdiff,'_lmbdmdiff0.png');
            gif_file=append('recon_pat',pat_No,'_hl_',dose_cur,'_it8_b32_lmbdchdiff',lmbdchdiff,'_lmbdmdiff0.gif');
    
            grey_load_filename_path_lowdose=fullfile(save_filename_path,DEMIST_lowdose_png);
            grey_load_filename_path_gif=fullfile(save_filename_path,gif_file);
    
            ge_save_filename_path_lowdose=fullfile(save_path_base,'ge','hl',DEMIST_lowdose_png);
         
    
            GE_converter(grey_load_filename_path_lowdose,GE_file,ge_save_filename_path_lowdose);
     
    
            submission_folder_hl=fullfile(submission_folder,'hl');
            if ~exist(submission_folder_hl, 'dir')
                mkdir(submission_folder_hl);
                disp(['Folder created: ', submission_folder_hl]);
            end
    
            copyfile(grey_load_filename_path_lowdose,submission_folder_hl);
            
            %copyfile(ge_save_filename_path_lowdose,submission_folder_hl);
            %copyfile(ge_save_filename_path_normaldose,submission_folder_hl);
            copyfile(grey_load_filename_path_gif,submission_folder_hl);
    

            system(append('rm ',DEMIST_lowdose));
            
       

        end

    end

    system(append('rm ',cur_pri_file_name));

end



for i=1:1:length(def_image_select)
    pat_No=def_image_select(i);
    


    for j=1:1:length(total_projection_fileNames)

        pri_file_cur=total_projection_fileNames(j);
        TF_No =  contains(pri_file_cur, pat_No);
        if TF_No ==1
            TF_PriPrj =  contains(pri_file_cur, 'PriPrj');
            if TF_PriPrj ==1
                pri_file_folder = fullfile(projection_folder,pri_file_cur);

                two_subfile=dir(pri_file_folder);

                for k = 1:length(two_subfile)

                    % Get the name of the item
                    pri_itemName = two_subfile(k).name;
                
                    % Skip the '.' and '..' directories
                    if strcmp( pri_itemName, '.') || strcmp( pri_itemName, '..')
                        continue;
                    end

                    is_pri_file =  contains( pri_itemName, 'dcm');

                    if is_pri_file==1
                        pri_file=fullfile(pri_file_folder, pri_itemName);
                        cur_pri_file_name=pri_itemName;
                        copyfile(pri_file)
                    end
               
                end

            end
        end    

    end

    %dose={'d7'};
   % defect_setting={'da'};
   % serverity_setting=[250];
    %extend_setting=[30];

    for dose_index=1:1:length(dose)
        dose_cur=dose{dose_index};

        for lmbdchdiff_index=1:1:length(lmbdchdiff_setting)
            lmbdchdiff=lmbdchdiff_setting{lmbdchdiff_index};
                
            for defect_setting_index=1:1:length(defect_setting)
                defect_setting_cur=defect_setting{defect_setting_index};

                for extend_setting_index=1:1:length(extend_setting)
                    extend_setting_cur=extend_setting{extend_setting_index};

                    for serverity_setting_index=1:1:length(serverity_setting)
                        serverity_setting_cur=serverity_setting{serverity_setting_index};

                        De_folder_name=append(defect_setting_cur,'21',extend_setting,'s',serverity_setting);
                        DEMIST_lowdose=append('recon_pat',pat_No,'_',De_folder_name,'_',dose_cur,'_it8_b32_lmbdchdiff',lmbdchdiff,'_lmbdmdiff0.img');


                        pat_filefolder=append(sa_folder,'/',defect_setting_cur,'21',extend_setting,'s',serverity_setting);


                        def_folder_name=append(defect_setting_cur,'21',extend_setting,'s',serverity_setting);
                        def_folder_name=def_folder_name{1};

                        mkdir(fullfile(save_path_base,'grey_scale',def_folder_name));
                        mkdir(fullfile(save_path_base,'ge',def_folder_name));
                    
                        DEMIST_lowdose_file_dir=fullfile(pat_filefolder,DEMIST_lowdose);
                        

                        copyfile(DEMIST_lowdose_file_dir);
                    
                      

                        save_filename_path=fullfile(save_path_base,'grey_scale',def_folder_name);
                        save_dcm_file_path=fullfile(save_path_base,'grey_scale',def_folder_name);


                        generate_image_series(DEMIST_lowdose,cur_pri_file_name,save_filename_path,save_dcm_file_path);
                       


                        DEMIST_lowdose_png=append('recon_pat',pat_No,'_',De_folder_name,'_',dose_cur,'_it8_b32_lmbdchdiff',lmbdchdiff,'_lmbdmdiff0.png');
                        gif_file=append('recon_pat',pat_No,'_',De_folder_name,'_',dose_cur,'_it8_b32_lmbdchdiff',lmbdchdiff,'_lmbdmdiff0.gif');
                
                        grey_load_filename_path_lowdose=fullfile(save_filename_path,DEMIST_lowdose_png);
                        grey_load_filename_path_gif=fullfile(save_filename_path,gif_file);
                
                        ge_save_filename_path_lowdose=fullfile(save_path_base,'ge',def_folder_name,DEMIST_lowdose_png);
                       
                        GE_converter(grey_load_filename_path_lowdose,GE_file,ge_save_filename_path_lowdose);
                        
                
                        submission_folder_def=fullfile(submission_folder,'def');
                        if ~exist(submission_folder_def, 'dir')
                            mkdir(submission_folder_def);
                            disp(['Folder created: ', submission_folder_def]);
                        end
                
                        copyfile(grey_load_filename_path_lowdose,submission_folder_def);
                        
                        %copyfile(ge_save_filename_path_lowdose,submission_folder_hl);
                        %copyfile(ge_save_filename_path_normaldose,submission_folder_hl);
                        copyfile(grey_load_filename_path_gif,submission_folder_def);
    
    

                        system(append('rm ',DEMIST_lowdose));                       
                        

                                                    
                    end
                end
            end
        end        
    end
    system(append('rm ',cur_pri_file_name));
end
