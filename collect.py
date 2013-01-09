import sys, re, string, time
from db import *
from regression import *
from scikit_wrapper import *
from sklearn.metrics import mean_squared_error

db = create_db_from_profile(sys.argv[1:]);
(x, y) = db_to_x_y(db);

ntrain = 1000;
train_idcs = [(i*ntrain, i*ntrain+ntrain) for i in range(0, len(db)/ntrain)];
print 'total: %d, ntrain: %d, num_parts: %d'%(len(db), ntrain, len(db)/ntrain);

#do_regression_tree(x, y, train_idcs[0]);

start = time.time();
gbst = do_gradient_boost(x, y, train_idcs[0]);
print "gradient boost time", time.time()-start;
gbst_avg = do_gradient_boost(x, y, train_idcs[0]);
for train_idx in train_idcs[1:]:
	temp = do_gradient_boost(x, y, train_idx);
	gbst_avg = map(lambda (x, y): x+y, zip(gbst_avg, temp));

gbst_avg = map(lambda x: x/len(train_idcs), gbst_avg);

start = time.time();
rf = do_random_forest(x, y, train_idcs[0]);
print "random forest", time.time()-start;
rf_avg = do_random_forest(x, y, train_idcs[0]);
for train_idx in train_idcs[1:]:
	temp = do_random_forest(x, y, train_idx);
	rf_avg = map(lambda (x, y): x+y, zip(rf_avg, temp));

rf_avg = map(lambda x: x/len(train_idcs), rf_avg);

sorted_list = zip(x, y, gbst, gbst_avg, rf, rf_avg);
to_be_sorted = zip(y, sorted_list);
to_be_sorted.sort();
dummy, sorted_list = zip(*to_be_sorted);

with open('sorted.dat', 'w') as fout:
	for (xval, yval, g, gavg, r, ravg) in sorted_list:
		print >>fout, string.join(map(lambda i: str(i), xval), '\t')+'\t%lf\t%lf\t%lf\t%lf\t%lf'%(yval, g, gavg, r, ravg);

#print 'Meansqr\n', mean_squared_error(y, gbst);
#print mean_squared_error(y, gbst_avg);
#improvement = mean_squared_error(y, gbst) - mean_squared_error(y, gbst_avg);
#print 'improved = ', improvement;
#print 'percent = ', improvement/mean_squared_error(y, gbst) * 100;

#splitting_conds = simple_gen_splitting_conditions();
#build_regression_tree(db, splitting_conds, 0, 1);
