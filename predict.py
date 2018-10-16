import csv
import os

def load_games(input_f):

	team_record = {}

	csv_reader = csv.reader(input_f)
	
	for row in csv_reader:
		winner = row[4]
		losser = row[6]

		isHomeWinner = row[5] != "@"

		if winner not in team_record:
			team_record[winner] = []
		
		if losser not in team_record:
			team_record[losser] = []

		if row[7] != "preview":
			team_record[winner].append(1)
			team_record[losser].append(0)

	return team_record

def predict_games(input_f, team_record, models):

	csv_reader = csv.reader(input_f)
	
	for row in csv_reader:
		away = row[0]
		home = row[1]

		away_confidence = 0
		home_confidence = 0

		votes = {away: 0, home: 0}

		for model_def in models:
			model = model_def["model"]
			weeks_to_roll = model_def["weeks"]

			homeRecord = team_record[home][-weeks_to_roll:]
			homePct = sum(homeRecord) / weeks_to_roll

			awayRecord = team_record[away][-weeks_to_roll:]
			awayPct = sum(awayRecord) / weeks_to_roll

			features = [[homePct, awayPct]]

			predict = model.predict(features)
			confidence = max(model.predict_proba(features)[0])
			
			if predict[0] == 0:
				votes[away]+=1
				away_confidence = max(away_confidence, confidence)
			else:
				votes[home]+=1
				home_confidence = max(home_confidence, confidence)
		
		print(f"{away},{home},{votes[away]},{votes[home]},{away_confidence},{home_confidence}")


from sklearn.externals import joblib

models = []

for x in range(2,7):
	
	desc = {}
	desc["model"] = joblib.load(f"models\\{x}_model.pkl")
	desc["weeks"] = x

	models.append(desc)

team_record = {}

with open(f"input\\2018.csv", "r") as input_f:
	team_record = load_games(input_f)

with open("input\\predict_7.csv", "r") as input_f:
	predict_games(input_f, team_record, models)