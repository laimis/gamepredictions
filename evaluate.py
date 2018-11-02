from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix

import pandas as pd
import numpy as np

import json

import seaborn as sns
import matplotlib.pyplot as plt

import common


def show_confusion(y, y_predicted):
	mat = confusion_matrix(y_true=y, y_pred=y_predicted)
	sns.heatmap(mat.T, annot=True, fmt='d')
	plt.show()

def calculate_accuracy(model, X, y):
	
	y_predicted = model.predict(X)
	y_probs = model.predict_proba(X)

	total = 0
	correct = 0

	for index,_ in enumerate(y_predicted):
		total+=1
		winner = np.argsort(y_probs[index])[-1]

		if max(y_probs[index]) < 0.55 and winner == 0:
			winner = 1

		if y.values[index] == winner:
			correct+=1
		
	manual_accuracy = correct/total

	accuracy = accuracy_score(y, y_predicted)

	return accuracy, manual_accuracy

def weekly_breakdown(groups, model):
	print("by week")

	for key in groups:
		
		X, y = groups[key]

		accuracy, manual_accuracy = calculate_accuracy(model, X, y)

		stats = common.confidence_stats(model, X, y.values)

		print(f"{key}:{accuracy:.2f} {' '.join(stats)}")


def evaluate(result_name, model, X, y):

	accuracy, manual_accuracy = calculate_accuracy(model, X, y)

	stats = common.confidence_stats(model, X, y)

	output = [weeks_to_roll, accuracy, "{}"]

	for s in stats:
		output.append(s)

	return output

data = []

test_file = f"output\\test\\nfl\\6.csv"
model_file = f"models\\nfl\\6_model.pkl"
output_file = "output\\html\\testdata.json"

model = common.load_model(model_file)
X, y = common.read_data_from_file(test_file)

data.append(evaluate(w, model, X, y))

dict = {"data": data}

with open(output_file, 'w') as summary_file:
	json.dump(dict, summary_file)

groups = common.read_data_groupedby_week(test_file)

weekly_breakdown(groups, model)