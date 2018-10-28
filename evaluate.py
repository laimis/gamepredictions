from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix

import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt

import common

def test_file(weeks_to_roll):
	return f"output\\test\\{weeks_to_roll}.csv"

def model_file(weeks_to_roll):
	return f"models\\{weeks_to_roll}_model.pkl"

def show_confusion(y, y_predicted):
	mat = confusion_matrix(y_true=y, y_pred=y_predicted)
	sns.heatmap(mat.T, annot=True, fmt='d')
	plt.show()

def calculate_accuracy(y, y_predicted, y_probs):
	
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

def weekly_breakdown(weeks_to_roll):
	print("by week")

	groups = common.read_data_groupedby_week(test_file(weeks_to_roll))
	model = common.load_model(model_file(weeks_to_roll))

	for key in groups:
		
		X, y = groups[key]

		y_predicted = model.predict(X)
		y_probabilities = model.predict_proba(X)

		accuracy, manual_accuracy = calculate_accuracy(y, y_predicted, y_probabilities)

		correct_guesses = 0
		total_guesses = 0
		threshold = 0.8

		for index,_ in enumerate(y_predicted):
			prob = max(y_probabilities[index])
			if prob >= threshold:
				total_guesses += 1
				if y_predicted[index] == y.values[index]:
					correct_guesses += 1

		pct = 0
		if total_guesses > 0:
			pct = correct_guesses / total_guesses

		print(f"{key} {accuracy:.2f} {manual_accuracy:.2f}, above {threshold}: {correct_guesses}/{total_guesses}")

		# show_confusion(y, y_predicted)

def evaluate(weeks_to_roll):

	X, y = common.read_data_from_file(test_file(weeks_to_roll))

	model = common.load_model(model_file(weeks_to_roll))

	y_predicted = model.predict(X)

	y_probs = model.predict_proba(X)

	accuracy, manual_accuracy = calculate_accuracy(y, y_predicted, y_probs)

	print(f"{weeks_to_roll} accuracy: {accuracy}, manual {manual_accuracy:.2f}")

for w in common.weeks_to_try():
	evaluate(w)

weekly_breakdown(6)