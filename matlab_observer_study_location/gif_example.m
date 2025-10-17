% Define the 3D matrix (example: 100x100x10 matrix)
data = rand(100, 100, 10);

% Define the filename for the GIF
filename = 'output.gif';

% Define the delay time between frames (in seconds)
delayTime = 0.5;

% Normalize the data to be in the range [0, 255] for GIF format
data_min = min(data(:));
data_max = max(data(:));
normalizedData = uint8((data - data_min) / (data_max - data_min) * 255);

% Create the GIF
for i = 1:size(normalizedData, 3)
    % Extract the i-th slice
    slice = normalizedData(:, :, i);
    
    % Convert the slice to an indexed image
    [indexedSlice, cmap] = gray2ind(slice, 256);
    
    % Write the frame to the GIF file
    if i == 1
        imwrite(indexedSlice, cmap, filename, 'gif', 'LoopCount', Inf, 'DelayTime', delayTime);
    else
        imwrite(indexedSlice, cmap, filename, 'gif', 'WriteMode', 'append', 'DelayTime', delayTime);
    end
end

disp(['GIF created successfully: ' filename]);