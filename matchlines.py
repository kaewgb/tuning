import sys, re

with open(sys.argv[1], 'r') as fin:
	in_lines = fin.readlines();
with open(sys.argv[2], 'r') as fconf:
	conf_lines = fconf.readlines();

with open('processed/'+sys.argv[1], 'w') as fout:
	i = 0;
	for conf_line in conf_lines:
		config = conf_line.strip().split(' ');
		in_config = re.split('_|\||,', in_lines[i])[:8];
		while in_config != config:
			i = i+1;
			try:
				in_config = re.split('_|\||,', in_lines[i])[:8];
			except:
				print "Error!";
				exit();
		print >>fout, in_lines[i],

