function [act_pat_id_arr, pat_id_arr, study_date_arr] = get_pat_list(fname)

  pat_id_date_arr = load(fname);
  fld = fieldnames(pat_id_date_arr);
  pat_id_date_arr = pat_id_date_arr.(fld{1});

  act_pat_id_arr = pat_id_date_arr(:, 1);
  pat_id_arr = pat_id_date_arr(:, 2);
  study_date_arr = pat_id_date_arr(:, 3);
end