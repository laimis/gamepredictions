import os
import json
import csv

import nba.importer as importer
import common
import train
import evaluate
import nba.features as features
import nba.strategies as strategies

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

def calibration(data_file:str, model_file:str, feature_columns:List[str]):

	model = common.load_model(model_file)

	data, X, y = common.read_data_from_file(data_file, "home_win", feature_columns)

	predictions = model.predict(X)
	probabilities = model.predict_proba(X)

	calibration_map:Dict = {}

	for idx,val in enumerate(predictions):
		true_outcome = y[idx]
		predicted_outcome = predictions[idx]
		confidence = float(max(probabilities[idx]))

		# calibration bits
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
		# end calibration

	with open("calibration.csv", "w", newline='') as o:
		writer = csv.writer(o)
		writer.writerow(["index","predicted","actual","number_of_games"])
		for pct in calibration_map:
			wins_losses = calibration_map[pct]
			number_of_games = wins_losses[0] + wins_losses[1]
			true_pct = wins_losses[0] / number_of_games
			true_pct = int(true_pct * 100)

			# don't bother with small sample size
			if number_of_games > 20:
				writer.writerow([pct,pct,true_pct,number_of_games])

def daily_evaluation(data_file:str, model_file:str, feature_columns:List[str], summary_file:str):

	model = common.load_model(model_file)

	data, X, y = common.read_data_from_file(data_file, "home_win", feature_columns)

	predictions = model.predict(X)
	probabilities = model.predict_proba(X)

	strat = strategies.all_strategies()

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

		for s in strat:
			s.evaluate(data.iloc[idx])

		add_to_json_summary(summary_file, [date,away,home,winner,predicted_winner,confidence])

	for s in strat:
		s.summary()

def strategy_evaluation(data_file:str, model_file:str, feature_columns:List[str]):

	model = common.load_model(model_file)

	data, X, y = common.read_data_from_file(data_file, "home_win", feature_columns)

	predictions = model.predict(X)
	probabilities = model.predict_proba(X)

	strat = strategies.all_strategies()

	# for idx,val in enumerate(predictions):
	# 	for s in strat:
	# 		s.evaluate(data.iloc[idx])

	for index,row in data.iterrows():
		for s in strat:
			s.evaluate(row)

	for s in strat:
		s.summary()

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

if __name__ == '__main__':

	model_file, feature_columns = common.read_model_definition("nba_model.csv")

	print("running detail analysis with model", model_file, "and features", feature_columns)

	data_file = "output\\nba\\daily.csv"
	run_import([2018], data_file)

	# daily_evaluation(
	# 	input_file,
	# 	model_file,
	# 	feature_columns,
	# 	"output\\nba\\html\\detaildata.json"
	# )

	strategy_evaluation(data_file, model_file, feature_columns)

