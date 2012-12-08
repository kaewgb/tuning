import sys, math
from mako.template import Template

if len(sys.argv) == 1:
	print "usage: %s config_filename lines_per_file"%(sys.argv[0]);
	exit();

template = Template(filename='job.mako');
maeka = Template(filename='job-maeka.mako');
with open(sys.argv[1], 'r') as fin:
	lines = fin.readlines();

lines_per_file = int(sys.argv[2]);
ranges = map(lambda x: (x*lines_per_file, (x+1)*lines_per_file), range(0,int(math.ceil(len(lines)/lines_per_file))))

count=1;
for r in ranges:
	filename = sys.argv[1].split('.')[0]+'_'+str(count);
	with open('confs/'+filename+'.conf', 'w') as fout:
		for i in range(max(0, r[0]), min(len(lines),r[1])):
			print >>fout, lines[i],

	# Dirac
#	with open('jobs/job-'+filename, 'w') as fout:
#		fout.write(template.render(jobid=filename));

	# Maeka
	with open('jobs/job-maeka-'+filename+'.sh', 'w') as fout:
		fout.write(maeka.render(jobid=filename));

	count = count+1;
