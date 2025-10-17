clear
close all;
addpath(genpath('/data01/user-storage/zitong/matlab_third_toolbox'))

%% files

for dataset = {'test/'}
    root_path = ['../../data/SPIE/'];
    for diag = {'healthy','diseased'}
        t = diag{1};
        cur_data_path = [root_path,dataset{1},'/',t,'/'];
        file_list = split(ls(cur_data_path));
        file_list = file_list(1:end-1);

        target_path = [root_path,dataset{1},'/',t,'_SA/'];

        for p_id = 1:length(file_list)
            pat_id = file_list(p_id);
            pat_id = pat_id{1}
            % if ~isfolder([target_path,'/',pat_id])
                system(['mkdir ',target_path,'/',pat_id]);
                system(['mkdir ',target_path,'/',pat_id,'/CTAC_rec']);
                system(['mkdir ',target_path,'/',pat_id,'/ScatLAC_rec']);
                system(['mkdir ',target_path,'/',pat_id,'/NAC_rec']);
            % end
            for l = {'da','di'}
                for e = [30,60,90]
                    for s = [175,375]
                        cur_file = [cur_data_path,'/',pat_id,'/CTAC_rec/',l{1},'_',num2str(e),'_',num2str(s),'/reoriented_windowed_HO.img'];
                        target_folder = [target_path,'/',pat_id,'/CTAC_rec/',l{1},'_',num2str(e),'_',num2str(s)];
                        if ~isfolder(target_folder)
                            system(['mkdir ',target_folder]);
                        end
                        system(['rm ',target_folder,'/*']);
                        system(['cp ',cur_file,' ',target_folder]);

                        cur_file = [cur_data_path,'/',pat_id,'/ScatLAC_rec/',l{1},'_',num2str(e),'_',num2str(s),'/reoriented_windowed_HO.img'];
                        target_folder = [target_path,'/',pat_id,'/ScatLAC_rec/',l{1},'_',num2str(e),'_',num2str(s)];
                        if ~isfolder(target_folder)
                            system(['mkdir ',target_folder]);
                        end
                        system(['rm ',target_folder,'/*']);
                        system(['cp ',cur_file,' ',target_folder]);

                        cur_file = [cur_data_path,'/',pat_id,'/NAC_rec/',l{1},'_',num2str(e),'_',num2str(s),'/reoriented_windowed_HO.img'];
                        target_folder = [target_path,'/',pat_id,'/NAC_rec/',l{1},'_',num2str(e),'_',num2str(s)];
                        if ~isfolder(target_folder)
                            system(['mkdir ',target_folder]);
                        end
                        system(['rm ',target_folder,'/*']);
                        system(['cp ',cur_file,' ',target_folder]);

                    end
                end
            end
        end
    end
end