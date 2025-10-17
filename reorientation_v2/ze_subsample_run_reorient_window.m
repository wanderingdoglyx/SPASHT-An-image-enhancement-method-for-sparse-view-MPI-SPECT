clear,clc

%ext_arr = [30,60,90];
%sev_arr = [175,375];
%loc_arr = {'da','di','dl'};
%AC_arr = {'CTAC','NAC','ScatLAC_rec'};

sample_slices=30;
ext_arr = [30,60,90];
sev_arr = {'s500','s100','s175','s250'};
loc_arr = {'da','di'};
AC_arr = {'CTAC'};


subsample= {'5','10','15','30'};
for subsample_idx = 1:length(subsample)
    sample_slices=subsample(subsample_idx);
    sample_slices=sample_slices{1};
%% healthy patient


def_name = ['hl'];
for AC_method_id = 1:length(AC_arr)
    AC_method = AC_arr{AC_method_id};

    file_path=['/data01/user-storage/y.zezhang/2024_subsample_project/mod_reconstruction/',num2str(sample_slices),'/',AC_method];
    patient_list_path='/data01/user-storage/y.zezhang/2024_subsample_project/mod_subsample_projection/30/def';
    patient_list = split(ls(patient_list_path));
    patient_list = patient_list(1:end-1);

    ze_subsample_s1_reorient_func(patient_list,def_name, AC_method,'healthy',num2str(sample_slices))

end


%% disease patient
for location_idx = 1:length(loc_arr)
    location_index=loc_arr{location_idx};
    %loc_prefix = loc_arr{location};
    for def_ext = ext_arr 
        for severity_idx = 1:length(sev_arr)
            severity_index=sev_arr(severity_idx);

            def_name = append(location_index,'21',num2str(def_ext),severity_index);
            def_name=def_name{1};

            for AC_method_id = 1:length(AC_arr)
                AC_method = AC_arr{AC_method_id};

                %file_path=['/data01/user-storage/y.zezhang/2024_subsample_project/reconstruction/',AC_method,'/10'];
                file_path=['/data01/user-storage/y.zezhang/2024_subsample_project/mod_reconstruction/',num2str(sample_slices),'/',AC_method];
                patient_list_path='/data01/user-storage/y.zezhang/2024_subsample_project/mod_subsample_projection/30/def';
                patient_list = split(ls(patient_list_path));
                %patient_list = split(ls(file_path));
                patient_list = patient_list(1:end-1);

                ze_subsample_s1_reorient_func(patient_list,def_name, AC_method, 'diseased',num2str(sample_slices))

            end
        end
    end
end

for c = {'healthy','diseased'}

    %file_path=['/data01/user-storage/y.zezhang/2024_subsample_project/SA_images/',c{1},'/10'];
    file_path=['/data01/user-storage/y.zezhang/2024_subsample_project/mod_SA_images/',num2str(sample_slices),'/',c{1}];
    patient_list_path='/data01/user-storage/y.zezhang/2024_subsample_project/mod_subsample_projection/30/def';
    patient_list = split(ls(patient_list_path));
    %atient_list = split(ls(file_path));
    patient_list = patient_list(1:end-1);

    for AC_method_id = 1:length(AC_arr)
        AC_method = AC_arr{AC_method_id}; 

        for  ind_pat =1:length(patient_list)     
            ze_subsample_s2_window_process_data(c{1},AC_method,ind_pat,patient_list,num2str(sample_slices));
        end
    end

end 


end