import csv
import os

import json

import common
import nfl.importer as importer
import nfl.parser as parser
import nfl.features as features

def predict_games(input_f, models, tracked_stats):

	csv_reader = csv.reader(input_f)
	
	predictions = []
	for row in csv_reader:
		
		game_info = parser.NFLGame(row)

		away_confidence = 0
		home_confidence = 0
		winner = game_info.home

		votes = {game_info.away: 0, game_info.home: 0}

		for model_def in models:
			model = model_def["model"]
			weeks_to_roll = model_def["weeks"]
			stats = model_def["stats"]

			calculated_features = [features.calc_features(stats, game_info, weeks_to_roll, tracked_stats)]

			predict = model.predict(calculated_features)
			confidence = max(model.predict_proba(calculated_features)[0])
			
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
		
		for f in calculated_features[0]:
			output.append(f"{f:.2f}")
		
		predictions.append(output)
	
	return predictions

models = []
week = 10

for x in [6]:
	
	model = common.load_model(f"models\\nfl\\{x}_model.pkl")
	_, stats = importer.generate_output_and_stats(2018, f"input\\nfl\\2018.csv", x, 17)

	desc = {}
	
	desc["model"] = model
	desc["weeks"] = x
	desc["stats"] = stats

	models.append(desc)

with open(f"input\\nfl\\predict.csv", "r") as input_f:
	predictions = predict_games(input_f, models, importer.get_tracked_stats())

	dict = {"data": predictions}

	with open("output\\nfl\\html\\predictions.json", 'w') as summary_file:
		json.dump(dict, summary_file)