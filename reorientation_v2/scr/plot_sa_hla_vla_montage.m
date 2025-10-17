function plot_sa_hla_vla_montage(recon_cast_sa, fname)
  close all;
  % recon_cast_sa = 48 x 48 x 32
  

  %% imp params
  num_slices = 20;
  region_size = 32;
  
  %% set up figure
  fh = figure('visible','off');
  fh.Units = 'normalized';
  fh.Position = [0 0 1 0.7];

  t = figure;
  % t.OuterPosition = [0 0 1 .5];
  % t.TileSpacing = 'tight';
  % t.Padding = 'tight';
  
  %% sa
  center_slice = 16;
  start_slice = center_slice - num_slices/2;
  end_slice = center_slice - 1 + num_slices/2;
  
  center_row = 24;
  start_row = center_row - region_size/2;
  end_row = center_row + region_size/2 - 1;
  
  center_col = 24;
  start_col = center_col - region_size/2;
  end_col = center_col + region_size/2 - 1;
  
  k = 1;
  for ind_slice = start_slice:end_slice
    % nexttile
    A = squeeze(recon_cast_sa(start_row:end_row, start_col:end_col, ind_slice));    
    subplot(4, num_slices/2,k);
    k = k + 1;
    imagesc(A);
    colormap gray; axis off; axis image;
    
    % 
    if ind_slice == start_slice
      text(region_size-region_size/2.5, region_size/10, 'Apex','Color','red','FontSize',14)
    end
    if ind_slice == end_slice
      text(region_size-region_size/2.5, region_size/10, 'Base','Color','red','FontSize',14)
    end
  end
  
  %% vla
  num_cols = 10;

  center_slice = 16;
  start_slice = center_slice - region_size/2+1;
  end_slice = center_slice  + region_size/2;
  
  center_row = 24;
  start_row = center_row - region_size/2;
  end_row = center_row + region_size/2 - 1;
  
  center_col = 24;
  start_col = center_col - num_cols/2;
  end_col = center_col + num_cols/2 - 1;

  sz = size(recon_cast_sa);
  recon_cast_sa_for_vla = recon_cast_sa;
  for ind_col = start_col:end_col
    % nexttile
    A = squeeze(recon_cast_sa_for_vla(start_row:end_row, ind_col, start_slice:end_slice));
    A = fliplr(A);
    subplot(4, num_slices/2,k);
    k = k + 1;
    imagesc(A);
    colormap gray; axis off; axis image;
    if ind_col == start_col
      text(region_size-region_size/2.5, region_size/10, 'Septal','Color','red','FontSize',14)
    end
    if ind_col == end_col
      text(region_size-region_size/2.5, region_size/10, 'Lateral','Color','red','FontSize',14)
    end
  end
%   cb = colorbar;
%   cb.Layout.Tile = 'east';
%   cb.FontSize = 20;
%   A = squeeze(recon_cast_sa(start_row:end_row, start_col:end_col, start_slice:end_slice));
%   A = flip(permute(A, [1,3,2]),2);
%   figure(5); imshow3D(A);
% figure(1)
  %% hla
  
  num_rows = 10;
  center_slice = 16;
  start_slice = center_slice - region_size/2 + 1;
  end_slice = center_slice + region_size/2;
  
  center_row = 24;
  start_row = center_row - num_rows/2;
  end_row = center_row + num_rows/2-1;
  
  center_col = 24;
  start_col = center_col - region_size/2;
  end_col = center_col + region_size/2 - 1;
  
%   fh = figure('visible','on');
%   fh.Units = 'normalized';
%   fh.Position = [0 0 0.8 0.4];

%   t = tiledlayout(1, num_rows);
%   %t.OuterPosition = [0 0 1 .5];
%   t.TileSpacing = 'tight';
%   t.Padding = 'tight';
  sz = size(recon_cast_sa);
  recon_cast_sa_for_hla = recon_cast_sa;
  for ind_row = end_row:-1:start_row
    % nexttile
    A = squeeze(recon_cast_sa_for_hla(ind_row, start_col:end_col, start_slice:end_slice));   
    A = fliplr(rot90(A,-1));
    subplot(4, num_slices/2,k);
    k = k + 1;
    imagesc(A);
    colormap gray; axis off; axis image;
    if ind_row == end_row
      text(region_size-region_size/2.5, region_size/10, 'Inferior','Color','red','FontSize',14)
    end
    if ind_row == start_row
      text(region_size-region_size/2.5, region_size/10, 'Anterior','Color','red','FontSize',14)
    end
  end
  % cb = colorbar;
  % cb.Layout.Tile = 'east';
  % cb.FontSize = 20;
 
  
  
  saveas(gcf, fname, 'png');
end