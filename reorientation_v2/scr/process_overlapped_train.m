function recon_sa = process_overlapped_train(recon_sa, lv_mask, cp)

  %% max val
  % max_val = max(recon_sa .* lv_mask, [], 'all');
  % recon_sa(recon_sa > max_val) = max_val;
  
  %% first window
  Nx = 48; 
  Ny = 48;
  %Nz = 32; original setting
  Nz = 48;
  %% 
  recon_sa = recon_sa(cp(2)-Ny/2:cp(2)+Ny/2-1, ...
                      cp(1)-Nx/2:cp(1)+Nx/2-1, ...
                      cp(3)-Nz/2:cp(3)+Nz/2-1);
  
  % if 0
  %   lv_mask = lv_mask(cp(2)-Ny/2:cp(2)+Ny/2-1, ...
  %                       cp(1)-Nx/2:cp(1)+Nx/2-1, ...
  %                       cp(3)-Nz/2:cp(3)+Nz/2-1);

  %   figure;
  %   set(gcf, 'Units', 'normalized', 'Position', [0,0,1,1]);
  %   tl = tiledlayout(6,6);
  %   for i = 1:Nz
  %     nexttile;
  %     imagesc(recon_sa(:,:,i)); colorbar;
  %     hold on;
  %     contour(lv_mask(:,:,i), [0.5, 0.5], 'r');
  %   end
  %   colormap viridis; axis off;
  % end
end