import re, string

def create_db_from_profile(files):
	db = list();
	for filename in files:
		with open(filename, 'r') as f:
			lines = filter(lambda l: l.find('inf') < 0,f.readlines());

			# split with '_', '|', ','
			records = map(lambda l: re.split(r'_|\||,', l.strip())[:9], lines);
			# convert str to float(
			records = map(lambda r: map(float, r), records);
			# remove the global_pad field
			records = map(lambda r: r[:4]+r[5:], records);

			db.extend(records);

	return db;

def get_x_from_file(files):
	db = list();
	for filename in files:
		with open(filename, 'r') as f:
			lines = filter(lambda l: l.find('inf') < 0,f.readlines());
			records = map(lambda l: l.split(), lines);
			records = map(lambda r: r[:7], records);
			records = map(lambda r: map(float, r), records);
			db.extend(records);
	return db;

def db_to_x_y(db):
	x = map(lambda r: r[:-1], db);
	y = map(lambda r: r[-1], db);
	return (x, y);

def create_lookup_db(files, method='gbrt'):
	predicted = 9;
	measured = 7;
	if method == 'rf':
		predicted = 11;
	elif method == 'krr':
		predicted = 7;
		measured = 8;

	db = dict();
	for filename in files:
		with open(filename, 'r') as f:
			lines = f.readlines();

			records = map(lambda l: l.split(), lines);
			for record in records:
				x = map(float, record[:7]); # to deal with 4.0 vs 4
				x = map(str, x);
				y = [float(record[predicted]), float(record[measured])]; #[predicted, measured]
				db[string.join(x, ' ')] = y;

	return db;

def lookup(conf, db):
	conf = map(float, conf); # to deal with 4.0 vs 4
	conf = map(str, conf);
	try:
		return db[string.join(conf, ' ')];
	except:
#		print string.join(conf, ' ');
		return [float('inf'), float('inf')];
