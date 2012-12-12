import sys, re, string

with open(sys.argv[1], 'r') as fin:
	ref = fin.readlines();
with open(sys.argv[2], 'r') as fin:
	match = fin.readlines();

with open(sys.argv[3], 'w') as fout:
	ref = map(lambda r: r.strip().split()[0:7], ref);
	match = map(lambda r: r.strip().split(), match);
	mfloat = map(lambda m: map(float, m[0:7]), match);
	print mfloat[:3];

	domain = zip(match, mfloat);
	for r in ref:
		r = map(float, r);
		for (m, mf) in domain:
			if mf==r:
				print >>fout, string.join(m, ' ');

