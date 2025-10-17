function [short_axis, long_axis, sagittal] = generate_image_series(filename,dcm_file_name,save_filename_path,save_dcm_file_path)

    dataType='float32';
    dataShape=Inf;
    
    raw_data = my_fread(filename, dataShape, dataType);

    % Replace NaN with 0 in numeric matrix
    raw_data(isnan(raw_data)) = 0;

    short_axis=reshape(raw_data,[48,48,48]);
    
    %slice_sample=short_axis(:,:,26);
    %imshow(imgseries)
    
    slice_number=15;
    dia=size(short_axis);
    short_axis_slice_index=dia(3);
    
    slice_index1=linspace(short_axis_slice_index/2-slice_number+1,short_axis_slice_index/2,slice_number);
    slice_index1=floor(slice_index1);
    slice_index2=linspace(short_axis_slice_index/2,short_axis_slice_index/2+slice_number,slice_number);
    slice_index2=floor(slice_index2);
    
    imgseries1 = imgseries_for_one_line(short_axis,slice_index1);
    imgseries2 = imgseries_for_one_line(short_axis,slice_index2);
    
    
    %direction = [1 0 0];
    %angle=90;
    long_axis = imrotate3(short_axis,90,[0 1 0],"nearest","loose");
    slice_index3=linspace(short_axis_slice_index/2-slice_number/2+1,short_axis_slice_index/2+slice_number/2,slice_number);
    slice_index3=floor(slice_index3);
    imgseries3 = imgseries_for_one_line(long_axis,slice_index3);
    
    
    %direction = [1 0 0];
    %angle=90;
    sagittal = imrotate3(short_axis,90,[1 0 0],"nearest","loose");
    slice_index4=linspace(short_axis_slice_index/2-slice_number/2+1,short_axis_slice_index/2+slice_number/2,slice_number);
    slice_index4=floor(slice_index4);
    imgseries4 = imgseries_for_one_line(sagittal,slice_index4);
    
    imgseries=[imgseries1; imgseries2; imgseries3; imgseries4];
    %imgseries_test=reshape(imgseries,[1,48*48*30]);
    %imgseries_test=reshape(imgseries_test,[2*48,48*15]);
    %sliceViewer(short_axis)
    png_file_name = strsplit(filename,'.');
    png_file_name=png_file_name{1};
    png_file_name=strcat(save_filename_path,'/',png_file_name,'.png');
    


    imwrite(imgseries,png_file_name,'png');
    
    
    dcm_file=dicomread(dcm_file_name);
    dcm_file=double(dcm_file);
    
    %dcm_dimension=size(dcm_file);
    %dcm_slices=dcm_dimension(4);
    
    
    data=dcm_file;
    
    % Define the filename for the GIF
    %dcm_filename = 'output.gif';
    
    dcm_filename = strsplit(filename,'.');
    dcm_filename=dcm_filename{1};
    dcm_filename=strcat(dcm_filename,'.gif');
    
    
    % Define the delay time between frames (in seconds)
    delayTime = 0;
    
    % Normalize the data to be in the range [0, 255] for GIF format
    data_min = min(data(:));
    data_max = max(data(:));
    normalizedData = uint8(((data - data_min) / (data_max)) * 255);
    %normalizedData=data;
    
    % Create the GIF
    for i = 1:size(normalizedData, 4)
        % Extract the i-th slice
        slice = normalizedData(:, :, i);
        %slice_min = min(slice(:));
        %slice_max = max(slice(:));
        %slice =  uint8(((slice - slice_min)/slice_max)* 255);
        % Convert the slice to an indexed image
        [indexedSlice, cmap] = gray2ind(slice, 256);
        
        % Write the frame to the GIF file
        save_dcm_file_name=fullfile(save_dcm_file_path,dcm_filename);

        if i == 1
            imwrite(indexedSlice, cmap, save_dcm_file_name, 'gif', 'LoopCount', Inf, 'DelayTime', delayTime);
        else
            imwrite(indexedSlice, cmap, save_dcm_file_name, 'gif', 'WriteMode', 'append', 'DelayTime', delayTime);
        end
    end
    
    disp(['GIF created successfully: ' save_dcm_file_name]);

end