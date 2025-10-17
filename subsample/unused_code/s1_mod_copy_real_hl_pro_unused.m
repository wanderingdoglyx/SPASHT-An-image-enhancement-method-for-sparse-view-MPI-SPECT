 clear; close all;

patient_name_main_Folder = '/data01/user-storage/y.zezhang/data_for_zezhang_mar29/test_data_mirirv3_sa_wd';
real_proj_folder='/data01/user-storage/y.zezhang/reg_PriPrj_ScaPrj_RegCT_DICOM';
outputFolder = '/data01/user-storage/y.zezhang/2024_subsample_project/mod_subsample_projection/30/hl';

% Get list of all subfolders (patient IDs)
patientFolders = dir(patient_name_main_Folder);
patientFolders = patientFolders([patientFolders.isdir]);
patientFolders = patientFolders(~ismember({patientFolders.name}, {'.', '..'}));

% Loop through each patient folder
for i = 1:length(patientFolders)
    patientID = patientFolders(i).name;

    folderName = processPatientDicom(patientID, real_proj_folder)

    patientFolderPath = fullfile(real_proj_folder, folderName);

    % Find the DICOM file in the patient's folder
    dicomFiles = dir(fullfile(patientFolderPath, '**', '*.dcm'));
    if isempty(dicomFiles)
        disp(['No DICOM file found for patient ' patientID]);
        continue;
    end
    
    dicomFilePath = fullfile(dicomFiles(1).folder, dicomFiles(1).name);
    % Read the DICOM file
    dicomData = dicomread(dicomFilePath);

    % Convert the DICOM data to 32-bit real (single-precision floating-point)
    dicomDataSingle = dicomData;

    % Create output file name
    outputFileName = fullfile(outputFolder, [patientID '.a00']);
    
    % Open the output binary file for writing
    fileID = fopen(outputFileName, 'w');
    
    % Write the DICOM data to the binary file as 32-bit real
    %fwrite(fileID, dicomDataSingle, 'uint16');
    fwrite(fileID, dicomDataSingle, 'float32');
    % Close the binary file
    fclose(fileID);
    
    disp(['DICOM data for patient ' patientID ' has been saved to ' outputFileName]);
end

disp('All patient data has been processed.');

% Function to find a folder containing a given patient ID and process the DICOM file

function folderName = processPatientDicom(patientID, real_proj_folder)
    % List all subfolders in the main folder
    subfolders = dir(real_proj_folder);
    subfolders = subfolders([subfolders.isdir]);
    subfolders = subfolders(~ismember({subfolders.name}, {'.', '..'}));

    % Initialize flag to check if folder is found
    folderFound = false;
    folderName = '';

    % Loop through each subfolder to find the one containing the patient ID in its name
    for i = 1:length(subfolders)
        if contains(subfolders(i).name, patientID) && contains(subfolders(i).name, 'PriPrj')
            folderName = subfolders(i).name;
            %patientFolderPath = fullfile(real_proj_folder, folderName);
            folderFound = true;
            break;
        end
    end

    if ~folderFound
        disp(['No folder found containing patient ID: ' patientID]);
        return;
    end

end