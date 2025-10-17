clear,clc

save_path_base='/data01/user-storage/y.zezhang/2024_false_defect_project/location_test_di';
sa_folder='/data01/user-storage/y.zezhang/data_for_zezhang_mar29/test_data_sa_wd_fix2_48cube';
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
extend_setting={'60'};
serverity_setting={'250'};


rng(76);

hl_patient='hl_patient_list.txt';
def_patient='def_patient_list.txt';

fid = fopen(hl_patient,'rt');
hl_image_select = readlines(hl_patient,"EmptyLineRule","skip");
fclose(fid);

fid = fopen(def_patient,'rt');
def_image_select = readlines(def_patient,"EmptyLineRule","skip");
fclose(fid);

%hl_image_select_number=5;
%def_image_select_number=5;

%hl_image_select=randsample(hl_lines,hl_image_select_number);
%def_image_select=randsample(def_lines,def_image_select_number);

%hl_patient_list='hl_patient_list.txt';
%def_patient_list='def_patient_list.txt';
%writematrix(hl_image_select,hl_patient_list);
%writematrix(def_image_select,def_patient_list);


% Create the full destination file path

%hl_destinationFile = fullfile(save_path_base, hl_patient_list);
%def_destinationFile = fullfile(save_path_base, def_patient_list);

% Copy the file to the destination folder
%copyfile(hl_patient_list, hl_destinationFile);
%copyfile(def_patient_list, def_destinationFile);

%system(['rm ', hl_patient_list]);
%system(['rm ', def_patient_list]);

for i=1:1:length(hl_image_select)
    pat_No=hl_image_select(i);
    pat_folder=fullfile(sa_folder,pat_No);
    pat_filefolder=fullfile(pat_folder,'hl');

    
    mkdir(fullfile(save_path_base,'dose','grey_scale','hl'));
    mkdir(fullfile(save_path_base,'dose','ge','hl'));

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
        lowdose=append('recon_pat',pat_No,'_',dose_cur,'_it8_c30o5.img');
        normaldose=append('recon_pat',pat_No,'_d1_it8_c30o5.img');

        lowdose_file_dir=fullfile(pat_filefolder,lowdose);
        normaldose_file_dir=fullfile(pat_filefolder, normaldose);

        copyfile(lowdose_file_dir);
        copyfile(normaldose_file_dir);
        %

        save_filename_path=fullfile(save_path_base,'dose','grey_scale','hl');
        save_dcm_file_path=fullfile(save_path_base,'dose','grey_scale','hl');


        generate_image_series(lowdose,cur_pri_file_name,save_filename_path,save_dcm_file_path);
        generate_image_series(normaldose,cur_pri_file_name,save_filename_path,save_dcm_file_path);


        lowdose_png=append('recon_pat',pat_No,'_',dose_cur,'_it8_c30o5.png');
        normaldose_png=append('recon_pat',pat_No,'_d1_it8_c30o5.png');
        gif_file=append('recon_pat',pat_No,'_d1_it8_c30o5.gif');
        gif_file_lowddose=append('recon_pat',pat_No,'_',dose_cur,'_it8_c30o5.gif');

        grey_load_filename_path_lowdose=fullfile(save_filename_path,lowdose_png);
        grey_load_filename_path_normaldose=fullfile(save_filename_path,normaldose_png);
        grey_load_filename_path_gif=fullfile(save_filename_path,gif_file);
        grey_load_filename_path_gif_lowddose=fullfile(save_filename_path,gif_file_lowddose);

        ge_save_filename_path_lowdose=fullfile(save_path_base,'dose','ge','hl',lowdose_png);
        ge_save_filename_path_normaldose=fullfile(save_path_base,'dose','ge','hl',normaldose_png);

        GE_converter(grey_load_filename_path_lowdose,GE_file,ge_save_filename_path_lowdose);
        GE_converter(grey_load_filename_path_normaldose,GE_file,ge_save_filename_path_normaldose);

        submission_folder_hl=fullfile(submission_folder,'hl');
        if ~exist(submission_folder_hl, 'dir')
            mkdir(submission_folder_hl);
            disp(['Folder created: ', submission_folder_hl]);
        end

        
        copyfile(grey_load_filename_path_lowdose,submission_folder_hl);
        copyfile(grey_load_filename_path_normaldose,submission_folder_hl);
        copyfile(grey_load_filename_path_gif_lowddose,submission_folder_hl);
        %copyfile(ge_save_filename_path_normaldose,submission_folder_hl);
        copyfile(grey_load_filename_path_gif,submission_folder_hl);



        system(append('rm ',lowdose));
        system(append('rm ',normaldose));
        


        
    end

    system(append('rm ',cur_pri_file_name));

end



for i=1:1:length(def_image_select)
    pat_No=def_image_select(i);
    pat_folder=fullfile(sa_folder,pat_No);
    


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



    for defect_setting_index=1:1:length(defect_setting)
        defect_setting_cur=defect_setting{defect_setting_index};

        for extend_setting_index=1:1:length(extend_setting)
            extend_setting_cur=extend_setting{extend_setting_index};

            for serverity_setting_index=1:1:length(serverity_setting)
                serverity_setting_cur=serverity_setting{serverity_setting_index};

                

                pat_filefolder=append(pat_folder,'/',defect_setting_cur,'21',extend_setting_cur,'s',serverity_setting_cur);

                def_folder_name=append(defect_setting_cur,'21',extend_setting_cur,'s',serverity_setting_cur);
                %def_folder_name=def_folder_name{1};

                mkdir(fullfile(save_path_base,'dose','grey_scale',def_folder_name));
                mkdir(fullfile(save_path_base,'dose','ge',def_folder_name));

                for dose_index=1:1:length(dose)
                    dose_cur=dose{dose_index};
                    lowdose=append('recon_pat',pat_No,'_',dose_cur,'_it8_c30o5.img');
                    normaldose=append('recon_pat',pat_No,'_d1_it8_c30o5.img');

                    lowdose_file_dir=fullfile(pat_filefolder,lowdose);
                    normaldose_file_dir=fullfile(pat_filefolder, normaldose);

                    copyfile(lowdose_file_dir);
                    copyfile(normaldose_file_dir);
                    %

                    save_filename_path=fullfile(save_path_base,'dose','grey_scale',def_folder_name);
                    save_dcm_file_path=fullfile(save_path_base,'dose','grey_scale',def_folder_name);


                    generate_image_series(lowdose,cur_pri_file_name,save_filename_path,save_dcm_file_path);
                    generate_image_series(normaldose,cur_pri_file_name,save_filename_path,save_dcm_file_path);


                    lowdose_png=append('recon_pat',pat_No,'_',dose_cur,'_it8_c30o5.png');
                    normaldose_png=append('recon_pat',pat_No,'_d1_it8_c30o5.png');
                    gif_file=append('recon_pat',pat_No,'_d1_it8_c30o5.gif');
                    gif_file_lowddose=append('recon_pat',pat_No,'_',dose_cur,'_it8_c30o5.gif');


                    grey_load_filename_path_lowdose=fullfile(save_filename_path,lowdose_png);
                    grey_load_filename_path_normaldose=fullfile(save_filename_path,normaldose_png);
                    grey_load_filename_path_gif=fullfile(save_filename_path,gif_file);
                    grey_load_filename_path_gif_lowddose=fullfile(save_filename_path,gif_file_lowddose);

            
                    ge_save_filename_path_lowdose=fullfile(save_path_base,'dose','ge',def_folder_name,lowdose_png);
                    ge_save_filename_path_normaldose=fullfile(save_path_base,'dose','ge',def_folder_name,normaldose_png);
            
                    GE_converter(grey_load_filename_path_lowdose,GE_file,ge_save_filename_path_lowdose);
                    GE_converter(grey_load_filename_path_normaldose,GE_file,ge_save_filename_path_normaldose);
            
                    submission_folder_def=fullfile(submission_folder,'def');
                    if ~exist(submission_folder_def, 'dir')
                        mkdir(submission_folder_def);
                        disp(['Folder created: ', submission_folder_def]);
                    end
            
                    copyfile(grey_load_filename_path_lowdose,submission_folder_def);
                    copyfile(grey_load_filename_path_normaldose,submission_folder_def);
                    copyfile(grey_load_filename_path_gif_lowddose,submission_folder_def);
                    %copyfile(ge_save_filename_path_normaldose,submission_folder_hl);
                    copyfile(grey_load_filename_path_gif,submission_folder_def);


                    system(append('rm ',lowdose));
                    system(append('rm ',normaldose));
                    


                    
                end
            end
        end
    end
    system(append('rm ',cur_pri_file_name));
end



