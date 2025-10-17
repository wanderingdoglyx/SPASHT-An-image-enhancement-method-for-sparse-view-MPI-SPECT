function createGifFromBinary(file_path, dims, gif_filename, delay_time)
    % createGifFromBinary - Create a GIF from a binary file with 3D data
    %
    % Syntax: createGifFromBinary(file_path, dims, gif_filename, delay_time)
    %
    % Inputs:
    %    file_path - Path to the binary file (e.g., 'data.a00')
    %    dims - Dimensions of the 3D data array (e.g., [30, 128, 128])
    %    gif_filename - Name of the output GIF file (e.g., 'output.gif')
    %    delay_time - Delay time between frames in the GIF (e.g., 0.1 seconds)
    %
    % Example usage:
    %    createGifFromBinary('data.a00', [30, 128, 128], 'output.gif', 0.1)
    
    % Open the file in binary mode
    fid = fopen(file_path, 'rb');
    
    % Error handling if the file cannot be opened
    if fid == -1
        error('Cannot open the file: %s', file_path);
    end
    
    % Read the binary file into a 3D array (single precision assumed)
    data = fread(fid, prod(dims), 'single');
    data = reshape(data, dims);
    
    %data = fread(fid,dataShape,dataType);
    % Close the file
    fclose(fid);
    
    % Normalize data for better visualization (optional)
    data = (data - min(data(:))) / (max(data(:)) - min(data(:)));
    
    % Loop through each slice and save as a GIF frame
    for i = 1:dims(3)
        % Extract the 2D slice
        slice = squeeze(data( :, :,i))';
        
        % Convert to an indexed image (8-bit) for GIF
        [imind, cm] = gray2ind(slice, 256);
        
        % Write to the GIF file
        if i == 1
            % Create the GIF file
            imwrite(imind, cm, gif_filename, 'gif', 'Loopcount', inf, 'DelayTime', delay_time);
        else
            % Append to the GIF
            imwrite(imind, cm, gif_filename, 'gif', 'WriteMode', 'append', 'DelayTime', delay_time);
        end
    end
    
    disp(['GIF created: ', gif_filename]);
end