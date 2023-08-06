# ========================================
# Source Dags Factory for Stresstest Tasks
# ========================================
# 
# path_in_mask='/data/DB/AIR/APC/FDW/tsk/*.yaml' \
# dag_prefix='tsk' \

/usr/bin/env python3 -m ka_air_dfs.dfs \
\
tenant='DB' \
\
path_in_mask='/data/DB/prj/FDW/PWF/wfl/tsk/str/*.yaml' \
dir_out_dag_src='/data/DB/prj/FDW/AIR/dags/tsk/str' \
\
a_tags='[FDW_TSK]' \
\
sw_cmd_ix=True \
sw_async=False \
sw_debug=False \
\
1>dfs_tsk_str.1 2>dfs_tsk_str.2
