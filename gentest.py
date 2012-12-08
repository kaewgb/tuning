import sys, os, subprocess, string
from mako.template import Template
from parse import *

def syscall(cmd):
	print string.join(cmd);
	subprocess.call(cmd);

# Initiation
count = 0;
template = Template(filename='simple.mako');
with open(sys.argv[1], 'r') as config_file:
	configs = config_file.readlines();

obj_files = ['test.o', 'util.o', 'util_cpu.o'];
nvcc_flags = ['-arch=sm_20', '--fmad=false', '--ptxas-options=-v', '--disable-warnings'];

fmin = open('simple/min', 'a');
favg = open('simple/avg', 'a');
fmax = open('simple/max', 'a');

# Codegen
for config in configs:

	[block_dim_x, block_dim_y, thread_z, maxrregcount, global_pad, shared_pad, smem, bypass_l1] = \
		config.strip().split(' ');

	config = config.strip().replace(' ', '_');
	target = 'cache/simple_' + config;

	if smem == '16':
		cache_config = 'cudaFuncCachePreferL1';
	else:
		cache_config = 'cudaFuncCachePreferShared';

	n_elements = int(shared_pad)/8;
	shared_pad_string = 'PAD%s(BLOCK_DIM_X+NG+NG)'%shared_pad;

	with open(target+'.cu', 'w') as fout:
		fout.write(template.render( block_dim_x		= block_dim_x,
									block_dim_y		= block_dim_y,
									thread_z 		= thread_z,
									global_pad		= global_pad,
									shared_pad		= shared_pad_string,
									smem			= cache_config));

	this_nvcc_flags = nvcc_flags + ['--maxrregcount', maxrregcount];
	if bypass_l1 == '1':
		this_nvcc_flags.extend(['-Xptxas', '-dlcm=cg']);

	# Compile the 'simple' kernel
	cmd = ['nvcc', '-c', target+'.cu', '-o', target+'.o'] + nvcc_flags
	syscall(cmd);

	# Compile the executable file
	cmd = ['nvcc', '-o', 'run/simple_'+config] + obj_files + [target+'.o']
	syscall(cmd);

	# Run the program
	cmd = ['run/simple_'+config, '128'];
	syscall(cmd);

	# Collect the profiling results
	(res_min, res_avg, res_max) = parse('cuda_profile_0.log', 'simple');

	print >>fmin, config + '|' + string.join(map(str, res_min), ',');
	print >>favg, config + '|' + string.join(map(str, res_avg), ',');
	print >>fmax, config + '|' + string.join(map(str, res_max), ',');

	count = count+1;
	if count > 25:
		cmd = ['rm', 'cache/*', 'run/*'];
		syscall(cmd);


fmin.close();
favg.close();
fmax.close();