from parse import *

def save2D(data, filename):
	with open(filename, 'w') as fout:
		for j in range(0, len(data)):
			for i in range(0, len(data[j])):
				print >>fout, block_dim_list[i], block_dim_list[j], data[j][i]
			print >>fout

max_threads_per_block = 1024;
block_dim_list = [4, 8, 16, 32, 64, 128, 256];

# Codegen
l = len(block_dim_list);
min_cpu_time = gen2Darray(l, l);
avg_cpu_time = gen2Darray(l, l);
max_cpu_time = gen2Darray(l, l);

for j in range(0, l):
	for i in range(0, l):

		block_dim_x = block_dim_list[i];
		block_dim_y = block_dim_list[j];

		if block_dim_x*block_dim_y > max_threads_per_block:
			continue;

		config = '%d_%d'%(block_dim_x, block_dim_y);

		res = parse('raw/diffterm_'+config, 'diffterm_lv1');

		min_cpu_time[j][i] = res[0];
		avg_cpu_time[j][i] = res[1];
		max_cpu_time[j][i] = res[2];

print avg_cpu_time;
save2D(avg_cpu_time, 'diffterm_lv1.dat');

for j in range(0, l):
	for i in range(0, l):

		block_dim_x = block_dim_list[i];
		block_dim_y = block_dim_list[j];

		if block_dim_x*block_dim_y > max_threads_per_block:
			continue;

		config = '%d_%d'%(block_dim_x, block_dim_y);

		res = parse('raw/diffterm_'+config, 'diffterm_lv2');

		min_cpu_time[j][i] = res[0];
		avg_cpu_time[j][i] = res[1];
		max_cpu_time[j][i] = res[2];

print avg_cpu_time;
save2D(avg_cpu_time, 'diffterm_lv2.dat');
