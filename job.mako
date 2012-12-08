#PBS -q dirac_small
#PBS -l nodes=1:ppn=1:fermi
#PBS -l walltime=06:00:00
#PBS -N job-${jobid}
#PBS -j oe
#PBS -o job-${jobid}.out
#PBS -V

cd $PBS_O_WORKDIR
mpirun -np 1 python gentest.py simple/${jobid}.conf
