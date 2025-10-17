function GE_image = GE_converter(Greyscale_image,GE_file,save_name)

    fid = fopen(GE_file,'rt');
    lines = readlines(GE_file,"EmptyLineRule","skip");
    fclose(fid);
    img=imread(Greyscale_image);
    [im_x,im_y]=size(img);

    GE_image=zeros(im_x,im_y,3);
    img_r=zeros(im_x,im_y);
    img_g=zeros(im_x,im_y);
    img_b=zeros(im_x,im_y);
    
    for i=1:im_x
        for j=1:im_y
            img_pixel=img(i,j);
            pixel_converter_value=lines(img_pixel+1);
            pixel_converter_value=sscanf(pixel_converter_value,'%d');
            ge_r=pixel_converter_value(1);
            ge_g=pixel_converter_value(2);
            ge_b=pixel_converter_value(3);
    
            img_r(i,j)=ge_r;
            GE_image(i,j,1)=ge_r;
            img_g(i,j)=ge_g;
            GE_image(i,j,2)=ge_g;
            img_b(i,j)=ge_b;
            GE_image(i,j,3)=ge_b;
            
        end
    end
    GE_image=GE_image/255;
    imwrite(GE_image,save_name);
   


end