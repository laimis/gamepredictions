import os

import pandas as pd
import numpy as np

from sklearn.externals import joblib
from sklearn.ensemble import AdaBoostClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier

def get_model_and_grid():

	# model = AdaBoostClassifier()
	# param_grid = {
	# 	"learning_rate": [0.01, 0.1, 0.5, 1, 10],
	# 	"n_estimators": [1, 10, 50, 100]
	# }

	# model = GaussianNB()
	# param_grid = {}

	# model = SVC(probability=True)
	# param_grid = {
	# 	"C": [0.001, 0.01, 0.1, 1, 10]
	# }

	model = MLPClassifier(max_iter=500)
	param_grid = {
		"alpha": [0.0001, 0.001, 0.01],
		"hidden_layer_sizes": [(10), (100), (200), (100, 100)]
	}
	
	return model, param_grid

def train_model(X, y, cv):

	model, param_grid = get_model_and_grid()

	grid = GridSearchCV(model, param_grid, cv=cv, return_train_score=True, verbose=0)

	grid.fit(X, y)

	return grid

def save_model(model, output_path):

	joblib.dump(model, output_path)

def confidence_stats(y, predicted, confidence, interval):

	correct_count = 0
	total_count = 0

	for i,_ in enumerate(predicted):
		conf = confidence[i]
		if np.max(conf) >= interval:
			total_count += 1
			if y[i] == predicted[i]:
				correct_count += 1

	return correct_count, total_count, interval

def render_confidence(stats):

	if stats[1] == 0:
		print("no correct pred with confidence ",stats[2])
	else:
		print(stats[2], stats[0], stats[1], stats[0]/stats[1])

def train_save_and_evaluate(input_path, model_path):

	data = pd.read_csv(input_path)

	print("processing", input_path)
	print("data shape", data.shape)

	y = data.home_win
	X = data.drop(["home_win", "home", "away"], axis=1, inplace=False)

	grid = train_model(X, y, 10)

	print("Best score:", grid.best_score_)
	print("Best params:", grid.best_params_)

	model = grid.best_estimator_

	save_model(model, model_path)

	predictions = model.predict(X)
	confidence = model.predict_proba(X)

	for level in [0.6, 0.7, 0.9]:
		stats = confidence_stats(y, predictions, confidence, level)
		render_confidence(stats)

inputs = np.arange(2,7)

filenames = [(f"output\\{x}trainingdata.csv", f"models\\{x}_model.pkl") for x in inputs]

for f in filenames:
	if os.path.isfile(f[1]):
		os.remove(f[1])

	train_save_and_evaluate(f[0], f[1])