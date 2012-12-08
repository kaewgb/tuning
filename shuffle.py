import sys
import random

with open(sys.argv[1], 'r') as fin:
	lines = fin.readlines();

random.seed();
l = range(0, len(lines));

while len(l) > 0:
	idx = random.randint(0, len(l)-1);
	print lines[l.pop(idx)],

