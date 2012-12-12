import sys, string

with open(sys.argv[1], 'r') as fin:
	lines = fin.readlines();
res = map(lambda l: l.strip().replace('\t', '\t& ') + ' \\\\\n', lines);
with open(sys.argv[2], 'w') as fout:
	fout.writelines(res);
