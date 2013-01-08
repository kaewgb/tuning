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


