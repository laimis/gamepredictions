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
	return [6]

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

def get_tracked_stats():
	return ["wins", "points", "allowed", "yards", "yards_allowed"]

def add_to_stats(stats, rd):

	def add_to_stats_internal(stats, team, to_add):

		if team not in stats:
			stats[team] = dict([(x,[]) for x in get_tracked_stats()])
			
		for idx,s in enumerate(get_tracked_stats()):
			stats[team][s].append(to_add[idx])

	add_to_stats_internal(stats, rd.home, [rd.homeWin, rd.homePts, rd.awayPts, rd.homeYards, rd.awayYards])
	add_to_stats_internal(stats, rd.away, [1 - rd.homeWin, rd.awayPts, rd.homePts, rd.awayYards, rd.homeYards])

def calc_features(stats, row_def, weeks_to_roll):

	home_pct, home_pts, home_allowed, home_yards, home_yards_allowed = calc_stats(stats, row_def.home, weeks_to_roll)
	away_pct, away_pts, away_allowed, away_yards, away_yards_allowed = calc_stats(stats, row_def.away, weeks_to_roll)

	return [
		away_pct,
		home_pct,
		away_pts - away_allowed,
		home_pts - home_allowed,
		away_yards - away_yards_allowed,
		home_yards - home_yards_allowed,
	]

def get_feature_headers():
	return "year,week,away,home,home_win,away_pct,home_pct,away_diff,home_diff,away_yards_diff,home_yards_diff\n"

def calc_stats(stats, team, weeks_to_roll):
 
	def do_calculation(team_stats, stat, length):
		return sum(team_stats[stat][-weeks_to_roll:]) / len(team_stats[stat][-weeks_to_roll:])

	team_stats = stats[team]

	return tuple([do_calculation(team_stats, x, weeks_to_roll) for x in get_tracked_stats()])


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
	for level in [0.65, 0.7, 0.75, 0.8, 0.9]:
		stat = calc_confidence_stats(y, predictions, probabilities, level)

		if stat[1] == 0:
			stats.append(f"no pred with confidence {stat[2]}")
		else:
			stats.append(f"{stat[2]}: {stat[0]}/{stat[1]}, {(stat[0]/stat[1]):.2f}")

	return stats