import csv
import os

import json
import datetime

import common
import nba.importer as importer
import nba.parser as parser
import nba.features as features
import nba.scraper as scraper

def generate_summary(games, predictions, confidences):

	summary = []
	for idx,val in enumerate(games):
		
		away_confidence = 0
		home_confidence = 0
		winner = val.home

		confidence = max(confidences[idx])
		
		if predictions[idx] == 0:
			away_confidence = max(away_confidence, confidence)
			winner = val.away
		else:
			home_confidence = max(home_confidence, confidence)
			winner = val.home
		
		output = [f"{val.away} @ {val.home}", winner]

		confidence = max(away_confidence, home_confidence)

		output.append(f"{confidence:.2f}")
		
		summary.append(output)
	
	return summary

stats = importer.generate_stats(f"input\\nba\\2018.csv")

model = common.load_model(f"models\\nba\\model.pkl")

data = []
games = []

dt = datetime.datetime.now()

for g in scraper.get_games(dt):

	game_info = parser.NBAGame(1, date = dt)
	game_info.away = g[0]
	game_info.home = g[1]

	games.append(game_info)
	data.append(importer.generate_output_row(2018, stats, game_info))

import pandas as pd

df = pd.DataFrame(data, columns=features.get_data_header().split(","))

X = df[features.get_feature_column_names()]

predictions = model.predict(X)
confidences = model.predict_proba(X)

summary = generate_summary(games, predictions, confidences)

dict = {"data": summary}

with open("output\\nba\\html\\predictions.json", 'w') as summary_file:
	json.dump(dict, summary_file)