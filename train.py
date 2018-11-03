import os

import common

import pandas as pd
import numpy as np

from sklearn.externals import joblib
from sklearn.ensemble import AdaBoostClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier

import json

def get_model_and_grid():

	# model = AdaBoostClassifier()
	# param_grid = {
	# 	"learning_rate": [0.01, 0.1, 0.5, 1, 10],
	# 	"n_estimators": [1, 10, 50, 100]
	# }

	model = GaussianNB()
	param_grid = {}

	# model = RandomForestClassifier()
	# param_grid = {
	# 	"n_estimators": [1, 10, 50, 100]
	# }

	# model = SVC(probability=True)
	# param_grid = {
	# 	"C": [0.001, 0.01, 0.1, 1, 10]
	# }

	# model = MLPClassifier(max_iter=500)
	# param_grid = {
	# 	"alpha": [0.0001, 0.001, 0.01],
	# 	"hidden_layer_sizes": [(10), (50), (10, 10), (10, 100), (10, 10, 10), (100, 100, 10)],
	# }
	
	return model, param_grid

def train_model(X, y, cv):

	model, param_grid = get_model_and_grid()

	grid = GridSearchCV(model, param_grid, cv=cv, return_train_score=True, verbose=0)

	grid.fit(X, y)

	return grid

def save_model(model, output_path):

	joblib.dump(model, output_path)