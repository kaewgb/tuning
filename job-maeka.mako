bash
export COMPUTE_PROFILE_LOG=${jobid}_profile.log
mpirun -np 1 --bind-to-core python genone.py confs/${jobid}.conf
