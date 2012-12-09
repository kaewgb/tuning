import sys, re, string
from regression import *
from gradientboost import *
from sklearn.metrics import mean_squared_error

def db_to_x_y(db):
	x = map(lambda r: r[:-1], db);
	y = map(lambda r: r[-1], db);
	return (x, y);

db = list();
for filename in sys.argv[1:]:
	with open(filename, 'r') as f:
		lines = filter(lambda l: l.find('inf') < 0,f.readlines());

		# split with '_', '|', ','
		records = map(lambda l: re.split(r'_|\||,', l.strip())[:9], lines);
		# convert str to float(
		records = map(lambda r: map(float, r), records);
		# remove the global_pad field
		records = map(lambda r: r[:4]+r[5:], records);

		db.extend(records);

#print db;
(x, y) = db_to_x_y(db);

ntrain = 1000;
train_idcs = [(i*ntrain, i*ntrain+ntrain) for i in range(0, len(db)/ntrain)];
print 'total: %d, ntrain: %d, num_parts: %d'%(len(db), ntrain, len(db)/ntrain);

gbst = do_gradient_boost(x, y, train_idcs[0]);
gbst_avg = do_gradient_boost(x, y, train_idcs[0]);
for train_idx in train_idcs[1:]:
	temp = do_gradient_boost(x, y, train_idx);
	gbst_avg = map(lambda (x, y): x+y, zip(gbst_avg, temp));

gbst_avg = map(lambda x: x/len(train_idcs), gbst_avg);
sorted_list = zip(x, y, gbst, gbst_avg);
to_be_sorted = zip(y, sorted_list);
to_be_sorted.sort();
dummy, sorted_list = zip(*to_be_sorted);

with open('onepass/data.dat', 'w') as fout:
	for (X, Y, G, Gavg) in sorted_list:
		print >>fout, string.join(map(lambda i: str(i), X), '\t')+'\t%lf\t%lf\t%lf'%(Y, G, Gavg);

print 'Meansqr\n', mean_squared_error(y, gbst);
print mean_squared_error(y, gbst_avg);
improvement = mean_squared_error(y, gbst) - mean_squared_error(y, gbst_avg);
print 'improved = ', improvement;
print 'percent = ', improvement/mean_squared_error(y, gbst) * 100;

#splitting_conds = simple_gen_splitting_conditions();
#build_regression_tree(db, splitting_conds, 0, 1);
