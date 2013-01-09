import sys, time
from db import *

x = get_x_from_file(sys.argv[1:]);

start = time.time();
#onepass.dat - 0-999: [419, 31, 227], 1000-1999: [1831, 1016, 1541], 2000-2999: [2346, 2670, 2460]
#simple_shuffled.dat - 0-999: [482, 839, 776], 1000-1999: [1075, 1183, 1855], 2000-2999: [2548, 2182, 2286]
parents = [482, 839, 776];
parms = [set() for i in range(0,7)];

for idx in parents:
	print x[idx];
	for i in range(0,7):
		parms[i].add(x[idx][i]);

for i in range(0,7):
	for x in parms[i]:
		print x,
	print


global_pad = 128;
with open('kcca0.conf', 'w') as fout:
	for block_dim_x in parms[0]:
		for block_dim_y in parms[1]:
			for thread_z in parms[2]:
				for maxrreg in parms[3]:
					for shared_pad in parms[4]:
						for smem in parms[5]:
							for bypass_l1 in parms[6]:
								print>>fout, '%d %d %d %d %d %d %d %d'%(block_dim_x, block_dim_y, thread_z, maxrreg, global_pad, shared_pad, smem, bypass_l1);
