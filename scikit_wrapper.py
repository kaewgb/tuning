import numpy as mp
import StringIO, pydot
from sklearn import svm
from sklearn import tree
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor

def do_gradient_boost(x, y, train_idx):

	x_train = x[train_idx[0]:train_idx[1]];
	y_train = y[train_idx[0]:train_idx[1]];

	clf = GradientBoostingRegressor( \
			n_estimators=100, \
			learn_rate=1.0, \
			max_depth=1, \
			random_state=0, \
			loss='ls');

	clf.fit(x_train, y_train);

	return clf.predict(x);

def do_svm(x, y, train_idx):

	x_train = x[train_idx[0]:train_idx[1]];
	y_train = y[train_idx[0]:train_idx[1]];

#	clf = svm.SVR(	\
#			C=1.0, \
#			cache_size=200, \
#			coef0=0.0, \
#			degree=3, \
#			epsilon=0.1, \
#			gamma=0.0, \
#			kernel='rbf', \
#			probability=False, \
#			shrinking=True, \
#			tol=0.001, \
#			verbose=False);
	clf = svm.SVR(kernel='rbf');
	clf.fit(x_train, y_train);

	return clf.predict(x);

def do_random_forest(x, y, train_idx):

	x_train = x[train_idx[0]:train_idx[1]];
	y_train = y[train_idx[0]:train_idx[1]];

	clf = RandomForestRegressor();
	clf.fit(x_train, y_train);

	return clf.predict(x);

def do_regression_tree(x, y, train_idx):
	x_train = x[train_idx[0]:train_idx[1]];
	y_train = y[train_idx[0]:train_idx[1]];

	clf = tree.DecisionTreeRegressor();
	clf = clf.fit(x_train, y_train);

	dot_data = StringIO.StringIO()
	tree.export_graphviz(clf, out_file=dot_data);
	graph = pydot.graph_from_dot_data(dot_data.getvalue());
	graph.write_pdf("sth.pdf");

	return clf.predict(x);
