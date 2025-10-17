#!/bin/bash

prev_version=${1}
new_version=${2}

mv train_3Dden_AR_v${prev_version}_custom_loop.py train_3Dden_AR_v${new_version}_custom_loop.py
#mv train_3Dden_AR_v${prev_version}_custom_loop_simp.py train_3Dden_AR_v${new_version}_custom_loop_simp.py
mv retrain_3Dden_AR_v${prev_version}_custom_loop.py retrain_3Dden_AR_v${new_version}_custom_loop.py
mv test_3Dden_AR_v${prev_version}.py test_3Dden_AR_v${new_version}.py
mv test_3Dden_AR_v${prev_version}_hl.py test_3Dden_AR_v${new_version}_hl.py
mv test_3Dden_AR_v${prev_version}_def_mirirv3.py test_3Dden_AR_v${new_version}_def_mirirv3.py
mv test_3Dden_AR_v${prev_version}_ZT.py test_3Dden_AR_v${new_version}_ZT.py
mv test_3Dden_AR_v${prev_version}_hl_ZT.py test_3Dden_AR_v${new_version}_hl_ZT.py

mv test_3Dden_AR_CZT_v${prev_version}.py test_3Dden_AR_CZT_v${new_version}.py
mv test_3Dden_AR_CZT_v${prev_version}_hl.py test_3Dden_AR_CZT_v${new_version}_hl.py
mv test_3Dden_AR_NaI_v${prev_version}.py test_3Dden_AR_NaI_v${new_version}.py
mv test_3Dden_AR_NaI_v${prev_version}_hl.py test_3Dden_AR_NaI_v${new_version}_hl.py
#mv Den3D_Model_AR_v${prev_version}_Loop.py Den3D_Model_AR_v${new_version}_Loop.py

