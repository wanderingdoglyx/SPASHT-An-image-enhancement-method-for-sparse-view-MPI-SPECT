function resultImg = MyButterWorth3D(grade, cutoff_freq, img, type)

[rows, cols, slices] = size(img);
img_double = double(img);
FImg = fftshift(fftn(img_double)); %Fast Fourier transform 2D and shift it to Center 

% compute distance to center with consider image size
x_arr = linspace(-0.5,0.5,cols+1); 
y_arr = linspace(0.5,-0.5,rows+1);
z_arr = linspace(0.5,-0.5,slices+1);
[X,Y,Z]= meshgrid(x_arr(1:end-1), y_arr(1:end-1), z_arr(1:end-1));
radius = sqrt(X.^2 + Y.^2 + Z.^2); 

% create filter
Filter = 1 ./ (1.0 + (radius ./ cutoff_freq).^(2*grade));

% change filter type low pass or high
if (strcmp(type, 'hpf'))
    Filter = 1 - Filter;
end

%applay filter
resultFImg = FImg .* Filter;

resultImg = real(ifftn(ifftshift(resultFImg)));

end