def parse(log, kernel):
	with open(log, 'r') as fin:
		lines = fin.readlines();

	lines = filter(lambda l: l[0]!='#', lines);
	head = lines[0].rstrip().split(',');

	lines = filter(lambda l: l.find(kernel) >= 0, lines);
	str_of_stats = map(lambda l: l.rstrip().split(',')[1:], lines);
	stats = map(lambda l: map(float, l), str_of_stats);

#	print head;
#	print len(head)
#	print stats[:3];

	res_min = list();
	res_avg = list();
	res_max = list();
	for i in range(0, head.index('active_cycles')-1):
		col = map(lambda l: l[i], stats);
		try:
			res_min.append(min(col));
			res_avg.append(sum(col)/len(col));
			res_max.append(max(col));
		except:
			res_min.append(float('inf'));
			res_avg.append(float('inf'));
			res_max.append(float('inf'));

	return (res_min, res_avg, res_max);



