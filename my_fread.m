function out = my_fread(filename, dataShape, dataType)

fid = fopen(filename,'rb');
out = fread(fid,dataShape,dataType);
fclose(fid);

end