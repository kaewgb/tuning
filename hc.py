import sys, re, time, random
from db import *

kernel = 'simple'

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


db = create_lookup_db(sys.argv[1:]);
random.seed();

for i in range(0, 3):#1000):

	start = time.time();
	if kernel == 'simple':
		# Simple
		best_conf = [16, 16, 8, 32, 32, 48, 0];
	else:
		# Onepass
		best_conf = [16, 16, 8, 64, 32, 48, 0];

	ymin = lookup(best_conf, db);
	#print ymin;

	for i in range(0, 75):
		test_conf = best_conf;
		for j in range(0, len(best_conf)):
			if random.random() <= 0.25:
				idx = random.randint(0, len(choices[j])-1);
				test_conf[j] = choices[j][idx];
		y = lookup(test_conf, db);
		#print test_conf, y;
		if y[0]	< ymin[0]:
			ymin = y;
			best_conf = test_conf;

	print ymin[1];
	print 'time:', time.time()-start;
