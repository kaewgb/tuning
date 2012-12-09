def split_records(records, predictor_var_idx, splitting_val):
	a = filter(lambda r: r[predictor_var_idx] <= splitting_val, records);
	b = filter(lambda r: r[predictor_var_idx] >  splitting_val, records);
	return (a, b);

def mean_square(records):
	try:
		gputimes = map(lambda r: r[-1], records);
		ybar = sum(gputimes)/len(gputimes);
		sqr = map(lambda y: (y-ybar)**2, gputimes);
		return sum(sqr);
	except:
		return float('inf');

def simple_gen_splitting_conditions():

	block_dim_choices 	= [4, 8, 16, 32, 64, 128, 256];
	thread_z_choices 	= [4, 8, 16, 32, 64];
	maxrreg_choices		= [16, 20, 24, 28, 32];
	pad_choices			= [32, 128, 256];
	smem_choices		= [16, 48];
	bypass_l1_choices	= [0, 1];

	predictor_vals = [				\
		block_dim_choices[:-1],		\
		block_dim_choices[:-1],		\
		thread_z_choices[:-1],		\
		maxrreg_choices[:-1],		\
		pad_choices[:-1],			\
		smem_choices[:-1],			\
		bypass_l1_choices[:-1]		\
	];

	cond = list();
	for i in range(0, len(predictor_vals)):
		for val in predictor_vals[i]:
			cond.append((i, val));

	return cond;

def build_regression_tree(db, splitting_conditions, lv, max_lv):
	if len(db) > 0:
		min_score = float('inf');
		for (idx, val) in splitting_conditions:
			(a, b) = split_records(db, idx, val);
			score = mean_square(a) + mean_square(b);
			if score < min_score:
				min_score = score;
				min_score_splitter = (idx, val);

		print 'minimum score: %lf'%min_score;
		print 'splitting condition: %d %d'%min_score_splitter;
