clear,clc
% Specify the source directory

sourceDir_def = '/datastore01/user-storage/y.zezhang/image_inspect/images/all_submission/def';
sourceDir_hl = '/datastore01/user-storage/y.zezhang/image_inspect/images/all_submission/hl';
% Specify the target directories for PNG and GIF files
targetDirPng = '/datastore01/user-storage/y.zezhang/image_inspect/images/all_submission/png';
targetDirGif = '/datastore01/user-storage/y.zezhang/image_inspect/images/all_submission/gif';

% Create the target directories if they don't exist
if ~exist(targetDirPng, 'dir')
    mkdir(targetDirPng);
end

if ~exist(targetDirGif, 'dir')
    mkdir(targetDirGif);
end



% Split the list of subfolders into individual folder paths
subfolderList = {sourceDir_def,sourceDir_hl};

% Loop through each subfolder
for i = 1:length(subfolderList)
    subfolder = subfolderList{i};
    if isempty(subfolder)
        continue;
    end
    
    % Get all PNG files in the current subfolder
    pngFiles = dir(fullfile(subfolder, '*.png'));
    for j = 1:length(pngFiles)
        sourceFile = fullfile(subfolder, pngFiles(j).name);
        
        copyfile(sourceFile, targetDirPng);
    end
    
    % Get all GIF files in the current subfolder
    gifFiles = dir(fullfile(subfolder, '*.gif'));
    for j = 1:length(gifFiles)
        sourceFile = fullfile(subfolder, gifFiles(j).name);
        
        copyfile(sourceFile, targetDirGif);
    end
end

disp('Files have been moved successfully.');