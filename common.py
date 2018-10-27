import pandas as pd

from sklearn.externals import joblib

class RowDef:
	def __init__(self, row):
		self.week = int(row[0])
		winner = row[4]
		losser = row[6]
		winnerPts = int(row[8])
		losserPts = int(row[9])

		isHomeWinner = row[5] != "@"

		self.away = winner
		self.awayPts = winnerPts
		self.home = losser
		self.homePts = losserPts
		self.homeWin = 0

		if isHomeWinner:
			self.away = losser
			self.awayPts = losserPts
			self.home = winner
			self.homePts = winnerPts
			self.homeWin = 1

def weeks_to_try():
	return [4,5,6]

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

	def add_to_stats_internal(stats, team, win_or_loss, pts, allowed):
		if team not in stats:
			stats[team] = {"wins":[], "points":[], "allowed":[]}
			
		stats[team]["wins"].append(win_or_loss)
		stats[team]["points"].append(pts)
		stats[team]["allowed"].append(allowed)

	add_to_stats_internal(stats, row_def.home, row_def.homeWin, row_def.homePts, row_def.awayPts)
	add_to_stats_internal(stats, row_def.away, 1 - row_def.homeWin, row_def.awayPts, row_def.homePts)

def calc_features(stats, row_def, weeks_to_roll):

	homePct, homePts, homeAllowed = calc_stats(stats, row_def.home, weeks_to_roll)
	awayPct, awayPts, awayAllowed = calc_stats(stats, row_def.away, weeks_to_roll)

	# return [awayPct, homePct, awayPts, homePts, awayAllowed, homeAllowed]
	# return [awayPct, homePct, awayPts]
	return [awayPct, homePct, awayPts - awayAllowed, homePts - homeAllowed]

def get_feature_headers():
	# return "away,home,home_win,away_pct,home_pct,away_pts,home_pts,away_diff,home_diff\n"
	# return "away,home,home_win,away_pct,home_pct\n"
	return "year,week,away,home,home_win,away_pct,home_pct,away_diff,home_diff\n"

def calc_stats(stats, team, weeks_to_roll):

		pct = sum(stats[team]["wins"][-weeks_to_roll:]) / len(stats[team]["wins"][-weeks_to_roll:])
		avgPts = sum(stats[team]["points"][-weeks_to_roll:]) / len(stats[team]["points"][-weeks_to_roll:])
		allowed = sum(stats[team]["allowed"][-weeks_to_roll:]) / len(stats[team]["allowed"][-weeks_to_roll:])

		return pct, avgPts, allowed


def load_model(filepath):

	return joblib.load(filepath)