import csv
import os

import json

import common
import nba.importer as importer
import nba.parser as parser
import nba.features as features

def predict_games(input_f, model, stats):

	csv_reader = csv.reader(input_f)
	
	predictions = []
	counter = 1
	for row in csv_reader:
		
		game_info = parser.NBAGame(row, counter)
		counter += 1

		away_confidence = 0
		home_confidence = 0
		winner = game_info.home

		calculated_features = [features.calc_features(stats, game_info)]

		predict = model.predict(calculated_features)
		confidence = max(model.predict_proba(calculated_features)[0])
		
		if predict[0] == 0:
			away_confidence = max(away_confidence, confidence)
			winner = game_info.away
		else:
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

model = common.load_model(f"models\\nba\\model.pkl")
_, stats = importer.generate_output_and_stats(2018, f"input\\nba\\2018.csv")

with open(f"input\\nba\\predict.csv", "r") as input_f:
	predictions = predict_games(input_f, model, stats)

	dict = {"data": predictions}

	with open("output\\nba\\html\\predictions.json", 'w') as summary_file:
		json.dump(dict, summary_file)