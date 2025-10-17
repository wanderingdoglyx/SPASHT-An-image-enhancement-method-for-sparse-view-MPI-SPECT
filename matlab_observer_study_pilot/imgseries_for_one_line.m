function imgseries = imgseries_for_one_line(image,slice_index)

    imgseries=[];
    for ind = slice_index
        slice_sample=image(:,:,ind);
        img=slice_sample;
        img=(img-min(img(:)))/max(img(:));
        imgseries=[imgseries img];      
    end

end