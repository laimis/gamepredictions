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

def predict_games(input_f, team_record, model, weeks_to_roll):

	csv_reader = csv.reader(input_f)
	
	for row in csv_reader:
		away = row[0]
		home = row[1]

		homeRecord = team_record[home][-weeks_to_roll:]
		homePct = sum(homeRecord) / weeks_to_roll

		awayRecord = team_record[away][-weeks_to_roll:]
		awayPct = sum(awayRecord) / weeks_to_roll

		features = [[homePct, awayPct]]

		predict = model.predict(features)

		outcome = home
		if predict[0] == 0:
			outcome = away
		
		print(f"{away} @ {home}: {outcome}")


from sklearn.externals import joblib

model = joblib.load("best_estimator.pkl")

team_record = {}

with open(f"2018copy.txt", "r") as input_f:
	team_record = load_games(input_f)

with open("predict.txt", "r") as input_f:
	predict_games(input_f, team_record, model, 3)