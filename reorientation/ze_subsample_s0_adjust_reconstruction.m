clear;
close all;
clc;


% Set paths
% process_all_img_files - Process all .img files in a folder to switch x and y axes
% 
% Syntax: process_all_img_files(folder_path, dims)
%
% Inputs:
%    folder_path - Path to the folder containing .img files
%    dims - Dimensions of the 3D array in the format [x, y, z]

file_path='/data01/user-storage/y.zezhang/2024_subsample_project/reconstruction/CTAC/10';
patient_list = split(ls(file_path));
patient_list = patient_list(1:end-1);



for ind_pat = 1:length(patient_list)

    pat_id = patient_list{ind_pat};
    cur_folder=fullfile(file_path, pat_id);

    % Get a list of all .img files in the folder
    img_files = dir(fullfile(cur_folder, '*.img'));

    % Loop through each file and process it
    for i = 1:length(img_files)
        
        input_file = fullfile(cur_folder, img_files(i).name);
        %output_file = fullfile(folder_path, ['switched_', img_files(i).name]);
        output_file = fullfile(cur_folder, img_files(i).name);
        
        fprintf('Processing %s...\n', img_files(i).name);
        
        % Call the function to switch x and y axes
        switch_xy_in_binary(input_file, output_file, [64,64,64]);
        
        fprintf('Saved switched data to %s\n', ['switched_', img_files(i).name]);
    end

end



function switch_xy_in_binary(input_file, output_file, dims)
    % switch_xy_in_binary - Read a 3D binary file, switch x and y axes, and save the result
    % 
    % Syntax: switch_xy_in_binary(input_file, output_file, dims)
    %
    % Inputs:
    %    input_file - Path to the input binary file
    %    output_file - Path to save the output binary file
    %    dims - Dimensions of the 3D array in the format [x, y, z]
    
    % Open the input file for reading
    fid_in = fopen(input_file, 'rb');
    if fid_in == -1
        error('Could not open input file.');
    end
    
    % Read the binary data
    data = fread(fid_in, prod(dims), 'float');
    
    % Close the input file
    fclose(fid_in);
    
    % Reshape the data into a 3D array
    data = reshape(data, dims);
    
    % Switch the x and y axes
    data_switched = permute(data, [2, 1, 3]);

    % Flip the data upside down along the z-axis
    data_flipped = flip(data_switched, 2);
    
    % Open the output file for writing
    fid_out = fopen(output_file, 'wb');
    if fid_out == -1
        error('Could not open output file.');
    end
    
    % Write the switched data to the output file
    fwrite(fid_out, data_flipped, 'float');
    
    % Close the output file
    fclose(fid_out);
end


