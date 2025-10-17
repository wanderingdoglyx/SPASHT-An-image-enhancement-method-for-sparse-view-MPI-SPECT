function S = get_dir(fdir, substr, pat_id)
  S = dir(fullfile(fdir,'*'));
  S = setdiff({S([S.isdir]).name},{'.','..'});
  S = S(contains(S, substr) & contains(S, pat_id));
  S = S{1};
end