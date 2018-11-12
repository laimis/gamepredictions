import csv
import os

import json
import datetime

import common
import nba.importer as importer
import nba.parser as parser
import nba.features as features
import nba.scraper as scraper

def predict_games(date, games, model, stats):

	predictions = []
	counter = 1
	for g in games:
		
		game_info = parser.NBAGame(counter, date = date)
		game_info.away = g[0]
		game_info.home = g[1]

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

model = common.load_model(f"models\\nba\\model.pkl")
_, stats = importer.generate_output_and_stats(2018, f"input\\nba\\2018.csv")

dt = datetime.datetime.now()

games = scraper.get_games(dt)

predictions = predict_games(dt, games, model, stats)

dict = {"data": predictions}

with open("output\\nba\\html\\predictions.json", 'w') as summary_file:
	json.dump(dict, summary_file)