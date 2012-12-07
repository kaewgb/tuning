import os, subprocess, string
from run import syscall
from mako.template import Template

# Initiation
diffterm = Template(filename='hypterm3.mako');

obj_files = ['onepass.o', 'util.o', 'util_cpu.o'];
nvcc_flags = ['-arch=sm_20', '--fmad=false', '--ptxas-options=-v', '--disable-warnings'];

ng = 4;
max_threads_per_block = 1024;
block_dim_list = [4, 8, 16, 32, 64, 128, 256];

# Codegen
for block_dim_y in block_dim_list:
	for block_dim_x in block_dim_list:

		if block_dim_x*block_dim_y > max_threads_per_block:
			continue;

		shared_dim_x = block_dim_x + ng + ng;
		shared_dim_y = block_dim_y + ng + ng;

		config = '%d_%d'%(block_dim_x, block_dim_y);
		target = 'cache/hypterm3_' + config;

		with open(target+'.cu', 'w') as fout:
			fout.write(diffterm.render(block_dim_x=str(block_dim_x),
										block_dim_y=str(block_dim_y),
										shared_dim_x=str(shared_dim_x),
										shared_dim_y=str(shared_dim_y)));


		cmd = ['nvcc', '-c', target+'.cu', '-o', target+'.o'] + nvcc_flags
		syscall(cmd);

		cmd = ['nvcc', '-o', 'run/gpu_'+config] + obj_files + [target+'.o']
		syscall(cmd);
