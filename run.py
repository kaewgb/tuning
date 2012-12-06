import os, subprocess, string
from mako.template import Template

def syscall(cmd):
	print string.join(cmd);
	subprocess.call(cmd);

max_threads_per_block = 1024;
block_dim_list = [4, 8, 16, 32, 64, 128, 256];

# Codegen
for block_dim_y in block_dim_list:
	for block_dim_x in block_dim_list:

		if block_dim_x*block_dim_y > max_threads_per_block:
			continue;

		config = '%d_%d'%(block_dim_x, block_dim_y);

		cmd = ['run/gpu_'+config, 'cell64'];
		syscall(cmd);

		cmd = ['mv', 'cuda_profile_0.log', 'raw/diffterm_'+config];
		syscall(cmd);
