from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score

import pandas as pd

import common

def evaluate(weeks_to_roll):

	X, y = common.read_data_from_file(f"output\\test\\{weeks_to_roll}.csv")

	model = common.load_model(f"models\\{weeks_to_roll}_model.pkl")

	y_predicted = model.predict(X)

	accuracy = accuracy_score(y, y_predicted)

	print(f"{weeks_to_roll} accuracy: {accuracy}")

evaluate(2)
evaluate(3)
evaluate(4)
evaluate(5)
evaluate(6)