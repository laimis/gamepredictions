import os
import json
import csv

import nba.importer as importer
import common
import train
import evaluate
import nba.features as features

from typing import List
from typing import Dict

def add_to_json_summary(summary_file, data):
	if os.path.isfile(summary_file):
		with open(summary_file, 'r') as fh:
			dict = json.load(fh)
	else:
		dict = {"data":[]}

	dict["data"].append(data)

	with open(summary_file, 'w') as fh:
		json.dump(dict, fh)

def run_evaluations(model_file:str, model_name:str, data_file:str, feature_columns:List[str], summary_file:str):
	
	model = common.load_model(model_file)

	_, X, y = common.read_data_from_file(data_file, "home_win", feature_columns)

	eval_results = evaluate.evaluate(f"{model_name}", model, X, y)

	add_to_json_summary(summary_file, eval_results)
	
	accuracy = evaluate.calculate_accuracy(model, X, y)

	return accuracy

def detail_evaluation(data_file:str, model_file:str, feature_columns:List[str], summary_file:str):

	model = common.load_model(model_file)

	data, X, y = common.read_data_from_file(data_file, "home_win", feature_columns)

	predictions = model.predict(X)
	probabilities = model.predict_proba(X)

	calibration_map:Dict = {}

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

		calibration_key = int(confidence * 100)
		calibration_key = calibration_key - (calibration_key%5)

		if calibration_key not in calibration_map:
			calibration_map[calibration_key] = (0, 0)
		
		wins_losses = calibration_map[calibration_key]
		if predicted_outcome == true_outcome:
			wins_losses = (wins_losses[0] + 1, wins_losses[1])
		else:
			wins_losses = (wins_losses[0], wins_losses[1] + 1)
		calibration_map[calibration_key] = wins_losses

		add_to_json_summary(summary_file, [date,away,home,winner,predicted_winner,confidence])

	delete_if_needed("calibration.csv")

	with open("calibration.csv", "w", newline='') as o:
		writer = csv.writer(o)
		writer.writerow(["index","real","model","number_of_games"])
		for pct in calibration_map:
			wins_losses = calibration_map[pct]
			number_of_games = wins_losses[0] + wins_losses[1]
			true_pct = wins_losses[0] / number_of_games
			true_pct = int(true_pct * 100)

			# don't bother with small sample size
			if number_of_games > 20:
				writer.writerow([pct,pct,true_pct,number_of_games])

def run_training(
	training_csv_path:str,
	model_name:str,
	feature_columns:List[str],
	model_output_path:str,
	summary_file:str,
	model,
	param_grid):
	
	_, X, y = common.read_data_from_file(training_csv_path, "home_win", feature_columns)
	
	grid = train.train_model(X, y, 10, model, param_grid)

	model = grid.best_estimator_

	train.save_model(model, model_output_path)

	output = [model_name, f"{grid.best_score_:.4f}", str(grid.best_params_)]
	
	add_to_json_summary(summary_file, output)

def run_import(years, output_file):
	delete_if_needed(output_file)

	with open(output_file, "a", newline='') as output_f:
		output_f.write(features.get_data_header() + "\n")

		for year in years:
			input_file = f"input\\nba\\{year}.csv"
			importer.transform_csv(input_file, output_f, year)

def delete_if_needed(filepath):
	if os.path.isfile(filepath):
		os.remove(filepath)

def run_train_test_validate():
	feature_set = {
		"pct": ["away_pct", "home_pct"],
		"pct-streak": ["away_pct", "home_pct", "away_streak", "home_streak"],
		"pct-pts": ["away_pct", "home_pct", "away_diff", "home_diff"],
		"pct-3pt": ["away_pct", "home_pct", "away_tpm", "home_tpm"],
		"pct-pts-streak": ["away_pct", "home_pct", "away_diff", "home_diff", "away_streak", "home_streak"],
		"pct-3pt-streak": ["away_pct", "home_pct", "away_tpm", "home_tpm", "away_streak", "home_streak"],
		"pct-pts-3pt": ["away_pct", "home_pct", "away_diff", "home_diff", "away_tpm", "home_tpm"],
		"pct-pts-to": ["away_pct", "home_pct", "away_diff", "home_diff", "away_todiff", "home_todiff"],
		"pct-pts-rebs": ["away_pct", "home_pct", "away_diff", "home_diff", "away_rebs", "home_rebs"],
		"pct-pts-3pt-to": ["away_pct", "home_pct", "away_diff", "home_diff", "away_tpm", "home_tpm", "away_todiff", "home_todiff"],
		"pct-pts-3pt-to-rebs": ["away_pct", "home_pct", "away_diff", "home_diff", "away_tpm", "home_tpm", "away_todiff", "home_todiff", "away_rebs", "home_rebs"]
	}

	train_input = "output\\nba\\train\\train.csv"
	run_import([2014, 2015, 2016], train_input)

	test_input 	= "output\\nba\\test\\test.csv"
	run_import([2017], test_input)

	val_input 	= "output\\nba\\validation\\validate.csv"
	run_import([2018], val_input)

	train_summary 	= "output\\nba\\html\\trainingdata.json"
	test_summary 	= "output\\nba\\html\\testdata.json"
	val_summary 	= "output\\nba\\html\\valdata.json"

	max_val_accuracy = 0
	max_val_model = ""
	max_val_columns:List[str] =  []

	delete_if_needed(train_summary)
	delete_if_needed(test_summary)
	delete_if_needed(val_summary)
	
	for s in feature_set:

		feature_columns = feature_set[s]

		models_grids = train.get_model_and_grid()
		for k in models_grids:
			print("training",k,feature_columns)

			model = models_grids[k]["model"]
			param_grid = models_grids[k]["param_grid"]
			name = f"5-6-7-{k}-{s}"
			model_output_path = f"models\\nba\\{name}.pkl"
			delete_if_needed(model_output_path)

			run_training(train_input, name, feature_columns, model_output_path, train_summary, model, param_grid)
			run_evaluations(model_output_path, f"{name}", test_input, feature_columns, test_summary)
			acc = run_evaluations(model_output_path, f"{name}", val_input, feature_columns, val_summary)
			if acc > max_val_accuracy:
				max_val_model = model_output_path
				max_val_columns = feature_columns
				max_val_accuracy = acc

	print("Train-Test-Eval Summary")
	print("Selected Model: ", max_val_model)
	print("Accuracy: ", max_val_accuracy)
	print("Features: ", max_val_columns)

	with open("nba_model.csv", "w", newline='') as o:
		writer = csv.writer(o)
		writer.writerow([max_val_accuracy, max_val_model, ",".join(max_val_columns)])

def run_daily_analysis():

	model_file, feature_columns = common.read_model_definition("nba_model.csv")

	print("running detail analysis with model", model_file, "and features", feature_columns)

	input_file = "output\\nba\\daily.csv"
	run_import([2017], input_file)

	detail_summary = "output\\nba\\html\\detaildata.json"
	delete_if_needed(detail_summary)
	detail_evaluation(input_file, model_file, feature_columns, detail_summary)

if __name__ == '__main__':

	run_daily_analysis()
	# run_train_test_validate()