import os
import json

import nba.importer as importer
import common
import train
import evaluate

def get_feature_headers():
	return "year,counter,away,home,home_win,away_pct,home_pct,away_diff,home_diff\n"

def get_column_names_for_removal():
	return ["year", "counter", "home_win", "home", "away"]

def run_evaluations():
	data = []

	test_file = f"output\\nba\\test\\train.csv"
	model_file = f"models\\nba\\model.pkl"
	output_file = "output\\nba\\html\\testdata.json"

	model = common.load_model(model_file)
	X, y = common.read_data_from_file(test_file, "home_win", get_column_names_for_removal())

	data.append(evaluate.evaluate("model", model, X, y))

	dict = {"data": data}

	with open(output_file, 'w') as summary_file:
		json.dump(dict, summary_file)

def run_training():
	models = []

	file_training = f"output\\nba\\train\\train.csv"
	file_model = f"models\\nba\\model.pkl"

	if os.path.isfile(file_model):
		os.remove(file_model)

	X, y = common.read_data_from_file(file_training, "home_win", get_column_names_for_removal())
	
	grid = train.train_model(X, y, 10)

	model = grid.best_estimator_

	stats = common.confidence_stats(model, X, y)
		
	train.save_model(model, file_model)

	output = ["model", grid.best_score_, str(grid.best_params_)]
	
	for s in stats:
		output.append(s)
	
	models.append(output)

	dict = {"data": models}

	with open("output\\nba\\html\\trainingdata.json", 'w') as summary_file:
		json.dump(dict, summary_file)

def run_import():
	def generate_features(years, train_or_test):

		output_file = f"output\\nba\\{train_or_test}\\train.csv"

		if os.path.isfile(output_file):
			os.remove(output_file)
		
		with open(output_file, "a", newline='') as output_f:
			output_f.write(get_feature_headers())

			for year in years:
				input_file = f"input\\nba\\{year}.csv"
				importer.transform_csv(input_file, output_f, year)

	years_train = [2015, 2016]
	years_test = [2017, 2018]

	generate_features(years_train, "train")
	generate_features(years_test, "test")


if __name__ == '__main__':

	run_import()
	run_training()
	run_evaluations()