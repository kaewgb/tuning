def parse(log, kernel):
	with open(log, 'r') as fin:
		lines = fin.readlines();

	lines = filter(lambda x: x[0]!='#', lines);
	head = lines[0].rstrip().split(',');
	idx = dict();
	for i in range(0, len(head)):
		idx[head[i]] = i;

	l = list();
	for line in lines[1:]:
		val = line.rstrip().split(',');
		if val[idx['method']].find(kernel) < 0:
			continue;
		l.append(val);

	stats=dict();
	keys = ['gputime', 'cputime'];
	for key in keys:
		stats[key] = map(lambda x: float(x[idx[key]]), l);

#	for key in keys:
#		print '%s\t%lf\t%lf\t%lf'%( key, min(stats[key]), sum(stats[key])/len(stats[key]), max(stats[key]));

	key = 'cputime';
	try:
		return (min(stats[key]), sum(stats[key])/len(stats[key]), max(stats[key]));
	except:
		return (float('inf'), float('inf'), float('inf'));

def gen2Darray(dim_x, dim_y):
	array = [];
	for i in range(0, dim_y):
		array.append([float('inf') for i in range(0, dim_x)]);
	return array;

