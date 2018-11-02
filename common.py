import pandas as pd
import numpy as np

from sklearn.externals import joblib

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
			if np.max(probabilities[i]) >= level:
				total_count += 1
				if y[i] == predicted[i]:
					correct_count += 1

		return correct_count, total_count, level

	predictions = model.predict(X)
	probabilities = model.predict_proba(X)

	stats = []
	for level in [0.7, 0.75, 0.8, 0.85, 0.9]:
		stat = calc_confidence_stats(y, predictions, probabilities, level)

		if stat[1] == 0:
			stats.append(f"no pred with confidence {stat[2]}")
		else:
			stats.append(f"{stat[2]}: {stat[0]}/{stat[1]}, {(stat[0]/stat[1]):.2f}")

	return stats