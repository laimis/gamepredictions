import csv
import os

import json
import datetime
import pandas as pd

import common
import nba.importer as importer
import nba.features as features
import nba.scraper as scraper
import nba.domain as domain

def generate_summary(df:pd.DataFrame, games, predictions, confidences, line_index:domain.GameLineIndex):

	summary = []
	for idx,val in enumerate(games):
		
		game_prediction = domain.GamePrediction(val, predictions[idx], confidences[idx])
		line = line_index.get(datetime.datetime.now().date(), val.away, val.home)
		

		output = []

		output.append(f"{val.away} @ {val.home}")

		if line != None:
			output.append(f"{line.team} {line.spread}")
		else:
			output.append("")
		
		output.append(game_prediction.winner)
		output.append(f"{game_prediction.confidence:.2f}")
		output.append(f"{df.iloc[idx]['away_streak']:.2f}")
		output.append(f"{df.iloc[idx]['home_streak']:.2f}")
		output.append(f"{df.iloc[idx]['away_pct']:.2f}")
		output.append(f"{df.iloc[idx]['home_pct']:.2f}")
		output.append(f"{df.iloc[idx]['away_diff']:.2f}")
		output.append(f"{df.iloc[idx]['home_diff']:.2f}")
		
		summary.append(output)
	
	return summary

stats = importer.generate_stats(f"input\\nba\\2018.csv")

model_file, feature_columns = common.read_model_definition("nba_model.csv")

model = common.load_model(model_file)

data = []
games = []

dt = datetime.datetime.now()

lines = scraper.get_gameday_lines(dt)
index = domain.GameLineIndex(lines)

for g in scraper.get_games(dt):

	game_info = domain.NBAGame(1, date = dt)
	game_info.away = g[0]
	game_info.home = g[1]

	games.append(game_info)
	data.append(importer.generate_output_row(2018, stats, game_info))

df = pd.DataFrame(data, columns=features.get_data_header().split(","))

X  = df[feature_columns]

predictions = model.predict(X)
confidences = model.predict_proba(X)

summary = generate_summary(df, games, predictions, confidences, index)

dict = {"data": summary}

with open("output\\nba\\html\\predictions.json", 'w') as summary_file:
	json.dump(dict, summary_file)

# for g in games:
# 	print(f"'{g.home}',")
# 	print(f"'{g.away}',")