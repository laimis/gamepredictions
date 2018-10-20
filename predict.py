import csv
import os

import json

def load_games(input_f):

	stats = {}
	
	csv_reader = csv.reader(input_f)
	
	for row in csv_reader:
		winner = row[4]
		losser = row[6]

		winnerPts = int(row[8])
		losserPts = int(row[9])

		diff = int(winnerPts) - int(losserPts)

		isHomeWinner = row[5] != "@"

		if winner not in stats:
			stats[winner] = {"wins":[], "points":[], "diff":[], "allowed":[]}
		
		if losser not in stats:
			stats[losser] = {"wins":[], "points":[], "diff":[], "allowed":[]}

		if row[7] != "preview":
			stats[winner]["wins"].append(1)
			stats[winner]["points"].append(winnerPts)
			stats[winner]["diff"].append(diff)
			stats[winner]["allowed"].append(-losserPts)

			stats[losser]["wins"].append(0)
			stats[losser]["points"].append(losserPts)
			stats[losser]["diff"].append(-diff)
			stats[losser]["allowed"].append(-winnerPts)

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

			homePct = sum(stats[home]["wins"][-weeks_to_roll:]) / weeks_to_roll
			homePts = sum(stats[home]["points"][-weeks_to_roll:]) / weeks_to_roll
			homeDiff = sum(stats[home]["diff"][-weeks_to_roll:])
			homeAllowed = sum(stats[home]["allowed"][-weeks_to_roll:]) / weeks_to_roll

			awayPct = sum(stats[away]["wins"][-weeks_to_roll:]) / weeks_to_roll
			awayPts = sum(stats[away]["points"][-weeks_to_roll:]) / weeks_to_roll
			awayDiff = sum(stats[away]["diff"][-weeks_to_roll:])
			awayAllowed = sum(stats[away]["allowed"][-weeks_to_roll:]) / weeks_to_roll

			features = [[awayPct, homePct, awayPts, homePts, awayAllowed, homeAllowed]]

			predict = model.predict(features)
			confidence = max(model.predict_proba(features)[0])
			
			if predict[0] == 0:
				votes[away]+=1
				away_confidence = max(away_confidence, confidence)
			else:
				votes[home]+=1
				home_confidence = max(home_confidence, confidence)
		
		predictions.append(
			# [
			# 	away,home,f"{awayPct:.2f}",f"{homePct:.2f}",f"{awayPts:.2f}",f"{homePts:.2f}",awayDiff,homeDiff,votes[away],votes[home],f"{away_confidence:.2f}",f"{home_confidence:.2f}"
			# ]

			[
				away,home,f"{awayPct:.2f}",f"{homePct:.2f}",f"{awayPts:.2f}",f"{homePts:.2f}",awayDiff,homeDiff,f"{away_confidence:.2f}",f"{home_confidence:.2f}"
			]
		)
	
	return predictions


from sklearn.externals import joblib

models = []

for x in [6]:
	
	desc = {}
	desc["model"] = joblib.load(f"models\\{x}_model.pkl")
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