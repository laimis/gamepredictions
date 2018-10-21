from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score

import pandas as pd

import common

def test_file(weeks_to_roll):
	return f"output\\test\\{weeks_to_roll}.csv"

def model_file(weeks_to_roll):
	return f"models\\{weeks_to_roll}_model.pkl"

def evaluate(weeks_to_roll):

	X, y = common.read_data_from_file(test_file(weeks_to_roll))

	model = common.load_model(model_file(weeks_to_roll))

	y_predicted = model.predict(X)

	accuracy = accuracy_score(y, y_predicted)

	print(f"{weeks_to_roll} accuracy: {accuracy}")

for w in common.weeks_to_try():
	evaluate(w)

print("by week")

groups = common.read_data_groupedby_week(test_file(6))
model = common.load_model(model_file(6))

for key in groups:
	
	X, y = groups[key]

	y_predicted = model.predict(X)
	
	accuracy = accuracy_score(y, y_predicted)

	print(key,accuracy)
