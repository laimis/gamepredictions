import pandas as pd

from sklearn.externals import joblib

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

def add_to_stats(stats, team, win_or_loss, pts, allowed):

	if team not in stats:
		stats[team] = {"wins":[], "points":[], "allowed":[]}
		
	stats[team]["wins"].append(win_or_loss)
	stats[team]["points"].append(pts)
	stats[team]["allowed"].append(allowed)

def calc_features(stats, home, away, weeks_to_roll):

	homePct, homePts, homeAllowed = calc_stats(stats, home, weeks_to_roll)
	awayPct, awayPts, awayAllowed = calc_stats(stats, away, weeks_to_roll)

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