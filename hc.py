import sys, re, string, random

# Simple
#block_dim_choices 	= [4, 8, 16, 32, 64, 128, 256];
#thread_z_choices 	= [4, 8, 16, 32, 64];
#maxrreg_choices		= [16, 20, 24, 28, 32];
#pad_choices			= [32, 128, 256];
#smem_choices		= [16, 48];
#bypass_l1_choices	= [0, 1];

# Onepass
block_dim_x_choices = [4, 8, 16, 32, 64, 128, 256];
block_dim_y_choices = [4, 8, 16, 20, 24, 32, 40, 64, 80, 96, 128, 256];
thread_z_choices 	= [4, 8, 16, 32, 48, 64];
maxrreg_choices		= [32, 40, 48, 52, 64];
pad_choices			= [32, 128, 256];
smem_choices		= [16, 48];
bypass_l1_choices	= [0, 1];

def db_to_lookup_db(db):
	x = map(lambda r: r[:-1], db);
	y = map(lambda r: r[-1], db);
	return [string.join(x, ' '), y];

def lookup(conf, db):
	conf = map(float, conf); # to deal with 4.0 vs 4
	conf = map(str, conf);
	try:
		return db[string.join(conf, ' ')];
	except:
		return [float('inf'), float('inf')];

db = dict();
for filename in sys.argv[1:]:
	with open(filename, 'r') as f:
		lines = f.readlines();
        records = map(lambda l: l.split(), lines);
        for record in records:
			x = record[:7];
			y = [float(record[11]), float(record[7])]; # for GBRT [predicted, measured]
			db[string.join(x, ' ')] = y;


# Simple
#choices = [block_dim_choices, block_dim_choices, thread_z_choices, maxrreg_choices, pad_choices, smem_choices, bypass_l1_choices];
# Onepass
choices = [block_dim_x_choices, block_dim_y_choices, thread_z_choices, maxrreg_choices, pad_choices, smem_choices, bypass_l1_choices];

random.seed();
for i in range(0, 1000):
	# Simple
	#best_conf = [16, 16, 8, 32, 32, 48, 0];
	# Onepass
	best_conf = [16, 16, 8, 64, 32, 48, 0];
	ymin = lookup(best_conf, db);
	#print ymin;

	for i in range(0, 75):
		test_conf = best_conf;
		for j in range(0, len(best_conf)):
			if random.random() <= 0.25:
				idx = random.randint(0, len(choices[j])-1);
				test_conf[j] = choices[j][idx];
		y = lookup(test_conf, db);
		#print test_conf, y;
		if y[0]	< ymin[0]:
			ymin = y;
			best_conf = test_conf;

	print ymin[1];
