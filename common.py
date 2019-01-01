import pandas as pd
import numpy as np

import csv

from sklearn.externals import joblib

from typing import Tuple
from typing import List

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