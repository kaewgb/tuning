import sys, os, subprocess, string, time
from mako.template import Template
from parse import *

def syscall(cmd):
	print string.join(cmd);
	subprocess.call(cmd);

# Initiation
kernel = 'onepass' #'simple'|'onepass'
if kernel == onepass:
	template = Template(filename='hypterm3.mako');
	obj_files = ['onepass.o', 'util.o', 'util_cpu.o'];
else
	template = Template(filename='simple.mako');
	obj_files = ['test.o', 'util.o', 'util_cpu.o'];

count = 0;

with open(sys.argv[1], 'r') as config_file:
	configs = config_file.readlines();

nvcc_flags = ['-arch=sm_20', '--fmad=false', '--ptxas-options=-v', '--disable-warnings'];

suffix = sys.argv[1].split('.')[0];		# Remove trailing file extension
suffix = suffix.split('/')[-1];			# Remove preceding directory path

processed = list();

# Codegen
for config in configs:

	start = time.time();

	[block_dim_x, block_dim_y, thread_z, maxrregcount, global_pad, shared_pad, smem, bypass_l1] = \
		config.strip().split(' ');

	config = config.strip().replace(' ', '_');
	target = 'cache/hypterm3_' + config;

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

	# Compile the 'hypterm3' kernel
	cmd = ['nvcc', '-c', target+'.cu', '-o', target+'.o'] + nvcc_flags
	syscall(cmd);

	# Compile the executable file
	cmd = ['nvcc', '-o', 'run/one_'+config] + obj_files + [target+'.o']
	syscall(cmd);

	# Run the program
	cmd = ['run/one_'+config, '64'];
	syscall(cmd);

	processed.extend([target+'.cu', target+'.o', 'run/one_'+config]);
	if len(processed) >= (5*3)-1:
		cmd = ['rm'] + processed;
		syscall(cmd);
		processed = [];

	print 'running time:', time.time()-start;

