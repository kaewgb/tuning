import numpy as mp
from sklearn.ensemble import GradientBoostingRegressor

def do_gradient_boost(x, y, train_idx):

	x_train = x[train_idx[0]:train_idx[1]];
	y_train = y[train_idx[0]:train_idx[1]];

	clf = GradientBoostingRegressor( \
			n_estimators=100, \
			learn_rate=1.0, \
			max_depth=1, \
			random_state=0, \
			loss='ls').fit(x_train, y_train);

	return clf.predict(x);
