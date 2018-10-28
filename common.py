import pandas as pd
import numpy as np

from sklearn.externals import joblib

class RowDef:
	def __init__(self, row):
		self.week = int(row[0])
		winner = row[4]
		losser = row[6]
		winnerPts = int(row[8])
		losserPts = int(row[9])
		winnerYards = int(row[10])
		losserYards = int(row[12])

		isHomeWinner = row[5] != "@"

		self.away = winner
		self.awayPts = winnerPts
		self.awayYards = winnerYards
		self.home = losser
		self.homePts = losserPts
		self.homeYards = losserYards
		self.homeWin = 0

		if isHomeWinner:
			self.away = losser
			self.awayPts = losserPts
			self.awayYards = losserYards
			self.home = winner
			self.homePts = winnerPts
			self.homeYards = winnerYards
			self.homeWin = 1

def weeks_to_try():
	return [5,6]

def read_data_from_file(filepath):

	data = pd.read_csv(filepath)

	y = data.home_win
	X = data.drop(["year", "week", "home_win", "home", "away"], axis=1, inplace=False)

	return X, y

def read_data_groupedby_week(filepath):

	data = pd.read_csv(filepath)

	grouped = {}
	for name, group in data.groupby(['year', 'week']):
		y = group.home_win
		X = group.drop(["year", "week", "home_win", "home", "away"], axis=1, inplace=False)

		grouped[name] = (X, y)

	return grouped

def add_to_stats(stats, row_def):

	def add_to_stats_internal(stats, team, win_or_loss, pts, allowed, yards):
		if team not in stats:
			stats[team] = {"wins":[], "points":[], "allowed":[], "yards":[]}
			
		stats[team]["wins"].append(win_or_loss)
		stats[team]["points"].append(pts)
		stats[team]["allowed"].append(allowed)
		stats[team]["yards"].append(yards)

	add_to_stats_internal(stats, row_def.home, row_def.homeWin, row_def.homePts, row_def.awayPts, row_def.homeYards)
	add_to_stats_internal(stats, row_def.away, 1 - row_def.homeWin, row_def.awayPts, row_def.homePts, row_def.awayYards)

def calc_features(stats, row_def, weeks_to_roll):

	homePct, homePts, homeAllowed, homeYards = calc_stats(stats, row_def.home, weeks_to_roll)
	awayPct, awayPts, awayAllowed, awayYards = calc_stats(stats, row_def.away, weeks_to_roll)

	return [awayPct, homePct, awayPts - awayAllowed, homePts - homeAllowed, awayYards, homeYards]

def get_feature_headers():
	return "year,week,away,home,home_win,away_pct,home_pct,away_diff,home_diff,away_yards,home_yards\n"

def calc_stats(stats, team, weeks_to_roll):
 
	pct = sum(stats[team]["wins"][-weeks_to_roll:]) / len(stats[team]["wins"][-weeks_to_roll:])
	avgPts = sum(stats[team]["points"][-weeks_to_roll:]) / len(stats[team]["points"][-weeks_to_roll:])
	allowed = sum(stats[team]["allowed"][-weeks_to_roll:]) / len(stats[team]["allowed"][-weeks_to_roll:])
	yards = sum(stats[team]["yards"][-weeks_to_roll:]) / len(stats[team]["yards"][-weeks_to_roll:]) / 100

	return pct, avgPts, allowed, yards


def load_model(filepath):

	return joblib.load(filepath)

def confidence_stats(model, X, y):

	def calc_confidence_stats(y, predicted, probabilities, level):
		correct_count = 0
		total_count = 0

		for i,_ in enumerate(predicted):
			if np.max(probabilities[i]) >= level:
				total_count += 1
				if y[i] == predicted[i]:
					correct_count += 1

		return correct_count, total_count, level

	predictions = model.predict(X)
	probabilities = model.predict_proba(X)

	stats = []
	for level in [0.7, 0.8, 0.9]:
		stat = calc_confidence_stats(y, predictions, probabilities, level)

		if stat[1] == 0:
			stats.append(f"no correct pred with confidence {stat[2]}")
		else:
			stats.append(f"{stat[2]}: {stat[0]}/{stat[1]}, {stat[0]/stat[1]:2f}")

	return stats