clear,clc

submission_folder='/datastore01/user-storage/y.zezhang/image_inspect/images/all_submission';

% Get the main folder path from the user
mainFolderPath = submission_folder;

% Define the names of the subfolders
subfolders = {'def', 'hl'};

% Initialize cell arrays to hold the old and new names
oldNames = {};
newNames = {};

% Loop over each subfolder

for j = 1:length(subfolders)
    % Get the full path of the current subfolder
    subfolderPath = fullfile(mainFolderPath, subfolders{j});
    
    % Get a list of all files in the subfolder
    fileList = dir(fullfile(subfolderPath, '*'));
    
    % Filter out directories from the list
    fileList = fileList(~[fileList.isdir]);
        
    % Separate .png and .gif files
    pngFiles = fileList(endsWith({fileList.name}, '.png'));
    gifFiles = fileList(endsWith({fileList.name}, '.gif'));
    

    % Loop over each file in the subfolder
    for i = 1:length(pngFiles)
        % Get the current file name
        oldName = pngFiles(i).name;
        oldName_gif = gifFiles(i).name;

        % Define the new file name (you can customize the renaming pattern here)
        [~, name, ext] = fileparts(oldName);
        [~, name_gif, ext_gif] = fileparts(oldName_gif);

        TF_def =  contains(subfolders(j), 'def');
        TF_hl =  contains(subfolders(j), 'hl');

        

        if TF_def==1
            
            newName = sprintf('h1_img%d%s',i, ext);
            newName_gif = sprintf('h1_img%d%s',i, ext_gif);
            
        end

        if TF_hl ==1
            
            newName = sprintf('h2_img%d%s',i, ext);
            newName_gif = sprintf('h2_img%d%s',i, ext_gif);

        end
        % Define the new file name (you can customize the renaming pattern here)
        % For example, rename files to 'file1.ext', 'file2.ext', etc.
        
        %newName = sprintf('file_%s_%d%s', subfolders{1}, 1, ext);
        
        % Get full file paths
        oldFullPath = fullfile(subfolderPath, oldName);
        newFullPath = fullfile(subfolderPath, newName);
        % Get full file paths
        oldFullPath_gif = fullfile(subfolderPath, oldName_gif);
        newFullPath_gif = fullfile(subfolderPath, newName_gif);
        
        % Check if the old name is different from the new name
        if ~strcmp(oldFullPath, newFullPath)
            % Rename the file
            movefile(oldFullPath, newFullPath);
            movefile(oldFullPath_gif, newFullPath_gif);
            % Record the name change
            oldNames{end+1, 1} = oldName;
            newNames{end+1, 1} = newName;
        end
      
    end
end

disp('Files in both subfolders have been renamed successfully.');


% Write the name changes to an Excel file
T = table(oldNames, newNames, 'VariableNames', {'OldName', 'NewName'});
writetable(T, fullfile(mainFolderPath, 'name_changes.xlsx'));

disp('Files in both subfolders have been renamed successfully and changes recorded in name_changes.xlsx.');