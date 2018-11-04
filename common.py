import pandas as pd
import numpy as np

from sklearn.externals import joblib

class ConfidenceStat:

	def __init__(self, conf_range, correct, total):
		self.conf_range = conf_range
		self.correct = correct
		self.total = total

		if self.total == 0:
			self.pct = 0
			self.label = f"{self.conf_range[0]}: N/A"
		else:
			self.pct = self.correct / self.total
			self.label = f"{self.conf_range[0]}: {self.correct}/{self.total}, {self.pct:.2f}"

	def __str__(self):
		return self.label

def read_data_from_file(filepath, y_col, x_cols_to_drop):

	data = pd.read_csv(filepath)

	y = data[y_col]
	X = data.drop(x_cols_to_drop, axis=1, inplace=False)

	return X, y

def read_data_groupedby_week(filepath, y_col, x_cols_to_drop, group_by):

	data = pd.read_csv(filepath)

	grouped = {}
	for name, group in data.groupby(group_by):
		y = group[y_col]
		X = group.drop(x_cols_to_drop, axis=1, inplace=False)

		grouped[name] = (X, y)

	return grouped

def load_model(filepath):

	return joblib.load(filepath)

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
	for level in [(0.50, 0.60), (0.60, 0.75), (0.75, 0.80), (0.80, 0.85), (0.85, 0.90), (0.90, 1.10)]:
		stat = calc_confidence_stats(y, predictions, probabilities, level)
		stats.append(stat)

	return stats