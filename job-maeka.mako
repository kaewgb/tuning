bash
export COMPUTE_PROFILE_LOG=${jobid}_profile.log
mpirun -np 1 python gentest.py confs/${jobid}.conf
