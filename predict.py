import csv
import os

import json

import common

def load_games(input_f):

	stats = {}
	
	csv_reader = csv.reader(input_f)
	
	for row in csv_reader:
		winner = row[4]
		losser = row[6]

		winnerPts = int(row[8])
		losserPts = int(row[9])

		common.add_to_stats(stats, winner, 1, winnerPts, losserPts)
		common.add_to_stats(stats, losser, 0, losserPts, winnerPts)

	return stats

def predict_games(input_f, stats, models):

	csv_reader = csv.reader(input_f)
	
	predictions = []
	for row in csv_reader:
		away = row[0]
		home = row[1]

		away_confidence = 0
		home_confidence = 0

		votes = {away: 0, home: 0}

		for model_def in models:
			model = model_def["model"]
			weeks_to_roll = model_def["weeks"]

			features = [common.calc_features(stats, home, away, weeks_to_roll)]

			predict = model.predict(features)
			confidence = max(model.predict_proba(features)[0])
			
			if predict[0] == 0:
				votes[away]+=1
				away_confidence = max(away_confidence, confidence)
			else:
				votes[home]+=1
				home_confidence = max(home_confidence, confidence)
		
		f = features[0]

		predictions.append(
			[
				away,home,f"{f[0]:.2f}",f"{f[1]:.2f}",f"{f[2]:.2f}",f"{f[3]:.2f}",f"{f[4]:.2f}",f"{f[5]:.2f}",f"{away_confidence:.2f}",f"{home_confidence:.2f}"
			]
		)
	
	return predictions

models = []

for x in [6]:
	
	desc = {}
	desc["model"] = common.load_model(f"models\\{x}_model.pkl")
	desc["weeks"] = x

	models.append(desc)

team_record = {}

with open(f"input\\2018.csv", "r") as input_f:
	stats = load_games(input_f)

with open("input\\predict_7.csv", "r") as input_f:
	predictions = predict_games(input_f, stats, models)

	dict = {"data": predictions}

	with open("output\\html\\predictions.json", 'w') as summary_file:
		json.dump(dict, summary_file)