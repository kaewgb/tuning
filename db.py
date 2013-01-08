import re, string

def create_db(files):
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

def db_to_x_y(db):
	x = map(lambda r: r[:-1], db);
	y = map(lambda r: r[-1], db);
	return (x, y);

def create_lookup_db(files):
	db = dict();
	for filename in files:
		with open(filename, 'r') as f:
			lines = f.readlines();

			records = map(lambda l: l.split(), lines);
			for record in records:
				x = record[:7];
				y = [float(record[11]), float(record[7])]; # for GBRT [predicted, measured]
				db[string.join(x, ' ')] = y;
	return db;

def lookup(conf, db):
	conf = map(float, conf); # to deal with 4.0 vs 4
	conf = map(str, conf);
	try:
		return db[string.join(conf, ' ')];
	except:
		return [float('inf'), float('inf')];
