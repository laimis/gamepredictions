import csv
import os

import json

import common
import importer

def predict_games(input_f, models):

	csv_reader = csv.reader(input_f)
	
	predictions = []
	for row in csv_reader:
		
		row_def = common.RowDef(row)

		away_confidence = 0
		home_confidence = 0

		votes = {row_def.away: 0, row_def.home: 0}

		for model_def in models:
			model = model_def["model"]
			weeks_to_roll = model_def["weeks"]
			stats = model_def["stats"]

			features = [common.calc_features(stats, row_def, weeks_to_roll)]

			predict = model.predict(features)
			confidence = max(model.predict_proba(features)[0])
			
			if predict[0] == 0:
				votes[row_def.away]+=1
				away_confidence = max(away_confidence, confidence)
			else:
				votes[row_def.home]+=1
				home_confidence = max(home_confidence, confidence)
		
		output = [row_def.away, row_def.home]

		for f in features[0]:
			output.append(f"{f:.2f}")
		
		output.append(votes[row_def.away])
		output.append(votes[row_def.home])
		output.append(f"{away_confidence:.2f}")
		output.append(f"{home_confidence:.2f}")
		
		predictions.append(output)
	
	return predictions

models = []

for x in [6]:
	
	desc = {}
	desc["model"] = common.load_model(f"models\\{x}_model.pkl")
	desc["weeks"] = x
	
	with open(f"input\\2018.csv", "r") as input_f:
		_, stats = importer.transform_input_to_output(2018, input_f, x)
		desc["stats"] = stats

	models.append(desc)

team_record = {}

with open("input\\predict_7.csv", "r") as input_f:
	predictions = predict_games(input_f, models)

	dict = {"data": predictions}

	with open("output\\html\\predictions.json", 'w') as summary_file:
		json.dump(dict, summary_file)