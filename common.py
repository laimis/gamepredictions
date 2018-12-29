import pandas as pd
import numpy as np

import csv

from sklearn.externals import joblib

class ConfidenceStat:

	def __init__(self, conf_range, correct, total):
		self.conf_range = conf_range
		self.correct = correct
		self.total = total

		losses = self.total - self.correct
		self.moneys = 3 * self.correct - 10 * losses

		if self.total == 0:
			self.pct = 0
			self.label = f"[{self.conf_range[0]}: N/A]"
		else:
			self.pct = self.correct / self.total
			self.label = f"[{self.conf_range[0]}: {self.pct:.2f} - {self.correct}/{self.total - self.correct} ${self.moneys}]"

	def __str__(self):
		return self.label

def read_data_from_file(filepath, y_col, x_col):

	data = pd.read_csv(filepath)

	y = data[y_col]
	X = data[x_col]

	return data, X, y

def read_data_grouped(filepath, y_col, x_col, group_by):

	data = pd.read_csv(filepath)

	grouped = {}
	for name, group in data.groupby(group_by):
		y = group[y_col]
		X = group[x_col]

		grouped[name] = (X, y)

	return grouped

def read_model_definition(definition_file):
	model_file = ""
	feature_columns = []

	with open(definition_file, "r") as i:
		reader = csv.reader(i)

		for r in reader:
			model_file = r[1]
			feature_columns = r[2].split(",")

	return model_file, feature_columns

def load_model(filepath):

	return joblib.load(filepath)

__levels__ =  [
	(0.60, 0.70),
	(0.70, 0.80),
	(0.80, 0.90),
	(0.90, 1.10),
	(0.60, 1.10),
	(0.70, 1.10),
	(0.80, 1.10)
]

def confidence_stats(model, X, y):

	def calc_confidence_stats(y, predicted, probabilities, level):
		correct_count = 0
		total_count = 0

		for i,_ in enumerate(predicted):
			if np.max(probabilities[i]) >= level[0] and np.max(probabilities[i]) < level[1]:
				total_count += 1
				if y[i] == predicted[i]:
					correct_count += 1

		return ConfidenceStat(level, correct_count, total_count)

	predictions = model.predict(X)
	probabilities = model.predict_proba(X)

	stats = []
	for level in __levels__:
		stat = calc_confidence_stats(y, predictions, probabilities, level)
		stats.append(stat)

	return stats