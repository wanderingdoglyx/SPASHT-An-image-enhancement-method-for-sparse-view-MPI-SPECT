function aligned_sa_recon = align_in_sa_from_tx_hr(recon_cast, di_sa, di_tx, res_factor)

  %% keep notations
  F = flip(reshape(di_sa.ImageOrientationPatient, 3, 2), 2);
  del_r = di_sa.PixelSpacing(1)/res_factor;
  del_c = di_sa.PixelSpacing(1)/res_factor;
  S_xyz = di_sa.ImagePositionPatient;
  del_s = di_sa.SliceThickness/res_factor;
  num_cols = double(di_sa.Columns) * res_factor;
  num_rows = double(di_sa.Rows) * res_factor;
  nv = cross(F(:,2), F(:,1));
  
  A_transform = eye(4,4);
  
  A_single = [ ...
      F(1,1)*del_r,   F(1,2)*del_c,   del_s * nv(1),    S_xyz(1);
      F(2,1)*del_r,   F(2,2)*del_c,   del_s * nv(2),    S_xyz(2);
      F(3,1)*del_r,   F(3,2)*del_c,   del_s * nv(3),    S_xyz(3);
      0,              0,              0,                1       ];
  
  num_slices = di_sa.NumberOfFrames * res_factor;
  
  [Col_coord, Row_coord] = ...
    meshgrid(0:num_cols-1, 0:num_rows-1);
  ALL_COORD = [
                Row_coord(:)';
                Col_coord(:)';
                zeros(1, numel(Row_coord));
                ones(1, numel(Col_coord));];
  
  %% get coordinates in mm
  ref_coord = [];
  for d = 0:num_slices-1
    A_transform(3, 4) = d;
    A_mod = A_single * A_transform;
    P = A_mod * double(ALL_COORD);
    ref_coord = [ref_coord; P(1:3, :)'];
  end
  
  %% do interpolation
  del_r_tx = di_tx.PixelSpacing(1);
  del_c_tx = di_tx.PixelSpacing(1);
  num_cols_tx = double(di_tx.Columns);
  num_rows_tx = double(di_tx.Rows);
  del_s_tx = di_tx.SliceThickness;
  S_xyz = di_tx.ImagePositionPatient;
  num_slices_tx = double(di_tx.NumberOfFrames);
  [Xq, Yq, Zq] = ...
    meshgrid((0:num_cols_tx-1)*del_c_tx+S_xyz(1), ...
    (0:num_rows_tx-1)*del_r_tx+S_xyz(2), ...
    (0:num_slices_tx-1)*del_s_tx+S_xyz(3));
    size(Xq);
  aligned_sa_recon = interp3(Xq, Yq, Zq, recon_cast, ref_coord(:,1), ref_coord(:,2), ref_coord(:,3), 'linear');
  aligned_sa_recon = reshape(aligned_sa_recon, [num_rows, num_cols, num_slices]);
end
