clear,clc

save_path_base='/data01/user-storage/y.zezhang/2024_false_defect_project/pilot_study';

rng(76);

hl_patient='test_pat_list_hl.txt';
def_patient='test_pat_list.txt';

fid = fopen(hl_patient,'rt');
hl_lines = readlines(hl_patient,"EmptyLineRule","skip");
fclose(fid);

fid = fopen(def_patient,'rt');
def_lines = readlines(def_patient,"EmptyLineRule","skip");
fclose(fid);

hl_image_select_number=15;
def_image_select_number=15;

hl_image_select=randsample(hl_lines,hl_image_select_number);
def_image_select=randsample(def_lines,def_image_select_number);

hl_patient_list='hl_patient_list.txt';
def_patient_list='def_patient_list.txt';
writematrix(hl_image_select,hl_patient_list);
writematrix(def_image_select,def_patient_list);


% Create the full destination file path
hl_destinationFile = fullfile(save_path_base, hl_patient_list);
def_destinationFile = fullfile(save_path_base, def_patient_list);

% Copy the file to the destination folder
copyfile(hl_patient_list, hl_destinationFile);
copyfile(def_patient_list, def_destinationFile);