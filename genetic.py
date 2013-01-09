import sys, time
from db import *

db = create_db(sys.argv[1:]);
(x, y) = db_to_x_y(db);

start = time.time();
parents = [1, 2, 3];
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
with open('kcca.conf', 'w') as fout:
	for block_dim_x in parms[0]:
		for block_dim_y in parms[1]:
			for thread_z in parms[2]:
				for maxrreg in parms[3]:
					for shared_pad in parms[4]:
						for smem in parms[5]:
							for bypass_l1 in parms[6]:
								print>>fout, '%d %d %d %d %d %d %d %d'%(block_dim_x, block_dim_y, thread_z, maxrreg, global_pad, shared_pad, smem, bypass_l1);
