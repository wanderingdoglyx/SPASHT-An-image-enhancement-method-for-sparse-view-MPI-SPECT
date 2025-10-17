function my_fwrite(filename, data, dataType)

fid = fopen(filename,'wb');
fwrite(fid, data, dataType);
fclose(fid);

end
