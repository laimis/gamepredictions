import pandas as pd
import numpy as np

import csv

from sklearn.externals import joblib

from typing import Tuple
from typing import List

class ConfidenceStat:

	def __init__(self, conf_range, correct, total, money):
		self.conf_range = conf_range
		self.correct = correct
		self.total = total
		self.money = money

		losses = self.total - self.correct
		
		if self.total == 0:
			self.pct = 0
			self.label = f"[{self.conf_range[0]}: N/A]"
		else:
			self.pct = self.correct / self.total
			self.label = f"[{self.conf_range[0]}: {self.pct:.2f} - {self.correct}/{self.total - self.correct} ${self.money}]"

	def __str__(self):
		return self.label

def read_data_from_file(filepath, y_col, x_col):

	data = pd.read_csv(filepath)

	y = data[y_col]
	X = data[x_col]

	return data, X, y

def read_data_grouped(filepath, group_by):

	data = pd.read_csv(filepath)

	grouped = {}
	for name, group in data.groupby(group_by):
		grouped[name] = group

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

def get_money_amount_from_line(spread:float) -> Tuple[int,int]:
	if (spread >= -1):
		return (5,5)
	if (spread >= -3):
		return (3,5)
	if (spread >= -5):
		return (1,5)
	if (spread >= -8):
		return (1, 8)
	if (spread >= -10):
		return (1, 10)
	return (1,15)

def confidence_stats(model, X, y, line_data=None) -> List[ConfidenceStat]:

	def calc_confidence_stats(y, predicted, probabilities, level):
		correct_count = 0
		total_count = 0
		money = 0

		for i,_ in enumerate(predicted):
			if np.max(probabilities[i]) >= level[0] and np.max(probabilities[i]) < level[1]:
				money_amount = get_money_amount_from_line(line_data[i])
				total_count += 1
				if y[i] == predicted[i]:
					correct_count += 1
					money += money_amount[0]
				else:
					money -= money_amount[1]

		return ConfidenceStat(level, correct_count, total_count, money)

	predictions = model.predict(X)
	probabilities = model.predict_proba(X)

	stats = []
	for level in __levels__:
		stat = calc_confidence_stats(y, predictions, probabilities, level)
		stats.append(stat)

	return stats