import os
import json

import nba.importer as importer
import common
import train
import evaluate
import nba.features as features

def add_to_json_summary(summary_file, data):
	if os.path.isfile(summary_file):
		with open(summary_file, 'r') as fh:
			dict = json.load(fh)
	else:
		dict = {"data":[]}

	dict["data"].append(data)

	with open(summary_file, 'w') as fh:
		json.dump(dict, fh)

def run_evaluations(model_name, data_file, summary_file):
	data = []

	model_file = f"models\\nba\\model.pkl"
	
	model = common.load_model(model_file)

	_, X, y = common.read_data_from_file(data_file, "home_win", features.get_feature_column_names())

	eval_results = evaluate.evaluate(f"{model_name}-test", model, X, y)

	add_to_json_summary(summary_file, eval_results)

def run_detail_evaluation(data_file, summary_file):

	model_file = f"models\\nba\\model.pkl"
	
	model = common.load_model(model_file)

	data, X, y = common.read_data_from_file(data_file, "home_win", features.get_feature_column_names())

	predictions = model.predict(X)
	probabilities = model.predict_proba(X)

	for idx,val in enumerate(predictions):
		true_outcome = y[idx]
		predicted_outcome = predictions[idx]
		confidence = float(max(probabilities[idx]))

		away = data.iloc[idx]["away"]
		home = data.iloc[idx]["home"]
		date = data.iloc[idx]["date"]

		if true_outcome == 1:
			winner = home
		else:
			winner = away

		if predicted_outcome == 1:
			predicted_winner = home
		else:
			predicted_winner = away

		correct = "yes"

		add_to_json_summary(summary_file, [date,away,home,winner,predicted_winner,confidence])

def daily_performance(data_file):
	model_file = f"models\\nba\\model.pkl"

	model = common.load_model(model_file)

	groups = common.read_data_groupedby_week(data_file, "home_win", features.get_feature_column_names(), ['year', 'date'])

	evaluate.weekly_breakdown(groups, model)

def run_training(model_name, summary_file):
	
	file_training = f"output\\nba\\train\\train.csv"
	file_model = f"models\\nba\\model.pkl"

	if os.path.isfile(file_model):
		os.remove(file_model)

	_, X, y = common.read_data_from_file(file_training, "home_win", features.get_feature_column_names())
	
	grid = train.train_model(X, y, 10)

	model = grid.best_estimator_

	stats = common.confidence_stats(model, X, y)
		
	train.save_model(model, file_model)

	output = [model_name, f"{grid.best_score_:.4f}", str(grid.best_params_)]
	
	for s in stats:
		output.append(s.label)
	
	add_to_json_summary(summary_file, output)

def run_import(years_train, years_test, years_validate):
	def generate_features(years, train_or_test):

		output_file = f"output\\nba\\{train_or_test}\\train.csv"

		if os.path.isfile(output_file):
			os.remove(output_file)
		
		with open(output_file, "a", newline='') as output_f:
			output_f.write(features.get_data_header() + "\n")

			for year in years:
				input_file = f"input\\nba\\{year}.csv"
				importer.transform_csv(input_file, output_f, year)

	generate_features(years_train, "train")
	generate_features(years_test, "test")
	generate_features(years_validate, "validation")


if __name__ == '__main__':

	def delete_if_needed(filepath):
		if os.path.isfile(filepath):
			os.remove(filepath)

	train_input = "output\\nba\\train\\train.csv"
	test_input = "output\\nba\\test\\train.csv"
	val_input = "output\\nba\\validation\\train.csv"

	train_summary = "output\\nba\\html\\trainingdata.json"
	test_summary = "output\\nba\\html\\testdata.json"
	val_summary = "output\\nba\\html\\valdata.json"
	detail_summary = "output\\nba\\html\\detaildata.json"

	delete_if_needed(train_summary)
	delete_if_needed(test_summary)
	delete_if_needed(val_summary)
	delete_if_needed(detail_summary)

	run_import([2014, 2015, 2016], [2017], [2018])
	run_training("4-5-6", train_summary)
	run_evaluations("4-5-6", test_input, test_summary)
	run_evaluations("4-5-6", val_input, val_summary)

	daily_performance(val_input)

	run_detail_evaluation(val_input, detail_summary)