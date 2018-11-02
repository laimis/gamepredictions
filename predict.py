import csv
import os

import json

import common
import importer
import nfl

def predict_games(input_f, models):

	csv_reader = csv.reader(input_f)
	
	predictions = []
	for row in csv_reader:
		
		game_info = nfl.NFLGame(row)

		away_confidence = 0
		home_confidence = 0
		winner = game_info.home

		votes = {game_info.away: 0, game_info.home: 0}

		for model_def in models:
			model = model_def["model"]
			weeks_to_roll = model_def["weeks"]
			stats = model_def["stats"]

			features = [common.calc_features(stats, game_info, weeks_to_roll)]

			predict = model.predict(features)
			confidence = max(model.predict_proba(features)[0])
			
			if predict[0] == 0:
				votes[game_info.away]+=1
				away_confidence = max(away_confidence, confidence)
				winner = game_info.away
			else:
				votes[game_info.home]+=1
				home_confidence = max(home_confidence, confidence)
				winner = game_info.home
		
		output = [f"{game_info.away} @ {game_info.home}", winner]

		confidence = max(away_confidence, home_confidence)

		output.append(f"{confidence:.2f}")
		
		for f in features[0]:
			output.append(f"{f:.2f}")
		
		predictions.append(output)
	
	return predictions

models = []
week = 9

for x in [6]:
	
	model = common.load_model(f"models\\nfl\\{x}_model.pkl")
	_, stats = importer.generate_output_and_stats(2018, f"input\\nfl\\2018.csv", x)

	desc = {}
	
	desc["model"] = model
	desc["weeks"] = x
	desc["stats"] = stats

	models.append(desc)

team_record = {}

with open(f"input\\nfl\\predict_{week}.csv", "r") as input_f:
	predictions = predict_games(input_f, models)

	dict = {"data": predictions}

	with open("output\\nfl\\html\\predictions.json", 'w') as summary_file:
		json.dump(dict, summary_file)