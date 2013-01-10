import sys, re, time, random
from db import *


kernel = 'onepass'
method = 'rf' #method = 'gbrt'|'rf'|'krr'
input_file = 'sorted.dat';
if method == 'krr':
	input_file = 'krr_sorted.dat';

if kernel == 'simple':
	# Simple
	block_dim_choices 	= [4, 8, 16, 32, 64, 128, 256];
	thread_z_choices 	= [4, 8, 16, 32, 64];
	maxrreg_choices		= [16, 20, 24, 28, 32];
	pad_choices			= [32, 128, 256];
	smem_choices		= [16, 48];
	bypass_l1_choices	= [0, 1];

	choices = [block_dim_choices, block_dim_choices, thread_z_choices, maxrreg_choices, pad_choices, smem_choices, bypass_l1_choices];

else:
	# Onepass
	block_dim_x_choices = [4, 8, 16, 32, 64, 128, 256];
	block_dim_y_choices = [4, 8, 16, 20, 24, 32, 40, 64, 80, 96, 128, 256];
	thread_z_choices 	= [4, 8, 16, 32, 48, 64];
	maxrreg_choices		= [32, 40, 48, 52, 64];
	pad_choices			= [32, 128, 256];
	smem_choices		= [16, 48];
	bypass_l1_choices	= [0, 1];

	choices = [block_dim_x_choices, block_dim_y_choices, thread_z_choices, maxrreg_choices, pad_choices, smem_choices, bypass_l1_choices];


db = create_lookup_db([input_file], method=method);
random.seed();

avg = 0.0;
for i in range(0, 1000):
	random.seed();
	start = time.time();
	if kernel == 'simple':
		# Simple
		best_conf = [16, 16, 8, 32, 32, 48, 0];
#		best_conf = [4, 8, 16, 28, 256, 48, 0];
	else:
		# Onepass
		best_conf = [16, 16, 8, 64, 32, 48, 0];
#		best_conf = [4, 8, 16, 28, 256, 48, 0];

	ymin = lookup(best_conf, db);
	#print ymin;
#	fname = '%s%d.conf'%(method, i);
#	with open(fname, 'w') as fout:
	if True:
		for i in range(0, 75):
			count = 0;
			#y = (float('inf'), float('inf'));
			#while y[1] == float('inf'):
			test_conf = best_conf;
			for j in range(0, len(best_conf)):
				if random.random() <= 0.25:
					idx = random.randint(0, len(choices[j])-1);
					test_conf[j] = choices[j][idx];
			y = lookup(test_conf, db);
#				count = count+1;

#			print test_conf, y;
			if y[0]	< ymin[0]:
				ymin = y;
				best_conf = test_conf;

			# print out test configurations
#			for t in test_conf[:4]:
#				print>>fout, t,
#			print>>fout, '128',
#			for t in test_conf[4:]:
#				print>>fout, t,
#			print>>fout
#			print count

	#print ymin[1];
	#print 'time:', time.time()-start;

	avg = avg + ymin[1];

print avg/1000.0;
