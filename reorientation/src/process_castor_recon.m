function recon_data = process_castor_recon(recon_data)

  recon_data = permute(recon_data, [2, 1, 3]);
  recon_data = flip(flip(recon_data, 2), 3);
end