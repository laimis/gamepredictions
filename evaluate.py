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

		if max(y_probs[index]) < 0.60 and winner == 0:
			winner = 1

		if y.values[index] == winner:
			correct+=1
		
	manual_accuracy = correct/total

	accuracy = accuracy_score(y, y_predicted)

	return accuracy, manual_accuracy

def evaluate(result_name, model, X, y):

	accuracy, manual_accuracy = calculate_accuracy(model, X, y)

	output = [result_name, f"{accuracy:.4f}", "{}"]

	return output