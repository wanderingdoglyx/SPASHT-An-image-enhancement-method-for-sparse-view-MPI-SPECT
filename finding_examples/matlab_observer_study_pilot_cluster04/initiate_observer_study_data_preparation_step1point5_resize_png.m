clc,clear
% Specify the main directories

mainDir1 = '/datastore01/user-storage/y.zezhang/image_inspect/images/all_submission/def';
mainDir2 = '/datastore01/user-storage/y.zezhang/image_inspect/images/all_submission/hl';

% Specify the target dimensions for resizing (e.g., [width, height])
targetSize = [640, 2400]; % Example: resize to 300x300 pixels

% Get a list of all subfolders in both main directories
allSubfolders1 = genpath(mainDir1);
allSubfolders2 = genpath(mainDir2);

% Combine both lists
allSubfolders = [strsplit(allSubfolders1, pathsep), strsplit(allSubfolders2, pathsep)];

% Loop through each subfolder
for i = 1:length(allSubfolders)
    subfolder = allSubfolders{i};
    if isempty(subfolder)
        continue;
    end
    
    % Get all PNG files in the current subfolder
    pngFiles = dir(fullfile(subfolder, '*.png'));
    for j = 1:length(pngFiles)
        sourceFile = fullfile(subfolder, pngFiles(j).name);
        
        % Read the image
        img = imread(sourceFile);
        
        % Resize the image
        resizedImg = imresize(img, targetSize);
        
        % Save the resized image (overwrite the original file)
        imwrite(resizedImg, sourceFile);
    end
end

disp('All PNG files have been resized successfully.');