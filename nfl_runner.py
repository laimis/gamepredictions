import os

import common
import nfl.importer as importer
import train
import evaluate

import json

def get_feature_headers():
	return ["away_pct","home_pct","away_diff","home_diff","away_yards_diff","home_yards_diff"]

def get_output_headers():
	return "year,week,away,home,home_win,away_pct,home_pct,away_diff,home_diff,away_yards_diff,home_yards_diff\n"

def weeks_to_try():
	return [6]

def run_import():
	rolling_windows = weeks_to_try()
	
	years_train = [2013,2014,2015,2016]
	years_test = [2017,2018]

	def call_transform(train_or_test, years, rolling_window, last_week):
		
		output_file = f"output\\nfl\\{train_or_test}\\{rolling_window}.csv"

		if os.path.isfile(output_file):
			os.remove(output_file)

		with open(output_file, "a", newline='') as output_f:
			output_f.write(get_output_headers())
			for year in years:
				input_file = f"input\\nfl\\{year}.csv"
				importer.transform_csv(rolling_window, input_file, output_f, year, last_week)

	for rolling_window in rolling_windows:
		call_transform("train", years_train, rolling_window, 16)
		call_transform("test", years_test, rolling_window, 17)

def run_training():
	models = []

	for f in weeks_to_try():

		file_training = f"output\\nfl\\train\\{f}.csv"
		file_model = f"models\\nfl\\{f}_model.pkl"

		if os.path.isfile(file_model):
			os.remove(file_model)

		_, X, y = common.read_data_from_file(file_training, "home_win", get_column_names_for_removal())
		
		grid = train.train_model(X, y, 10)

		model = grid.best_estimator_

		train.save_model(model, file_model)

		output = [f, grid.best_score_, str(grid.best_params_)]
		
		models.append(output)

	dict = {"data": models}

	with open("output\\nfl\\html\\trainingdata.json", 'w') as summary_file:
		json.dump(dict, summary_file)


def run_evaluations():
	data = []

	test_file = f"output\\nfl\\test\\6.csv"
	model_file = f"models\\nfl\\6_model.pkl"
	output_file = "output\\nfl\\html\\testdata.json"

	model = common.load_model(model_file)
	_, X, y = common.read_data_from_file(test_file, "home_win", get_feature_headers())

	data.append(evaluate.evaluate("6", model, X, y))

	dict = {"data": data}

	with open(output_file, 'w') as summary_file:
		json.dump(dict, summary_file)

	groups = common.read_data_grouped(test_file, ['year'])

	for key in groups:

		X = groups[key][get_feature_headers()]
		y = groups[key]["home_win"]
		
		accuracy, manual_accuracy = evaluate.calculate_accuracy(model, X, y)

		print(f"{key}:{accuracy:.2f}")


if __name__ == '__main__':

	run_import()
	# run_training()
	run_evaluations()