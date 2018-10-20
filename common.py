import pandas as pd

from sklearn.externals import joblib

def read_data_from_file(filepath):

	data = pd.read_csv(filepath)

	y = data.home_win
	X = data.drop(["home_win", "home", "away"], axis=1, inplace=False)

	return X, y

def add_to_stats(stats, team, win_or_loss, pts, diff, allowed):

	if team not in stats:
		stats[team] = {"wins":[], "points":[], "diff":[], "allowed":[]}
		
	stats[team]["wins"].append(win_or_loss)
	stats[team]["points"].append(pts)
	stats[team]["diff"].append(diff)
	stats[team]["allowed"].append(allowed)

def calc_features(stats, home, away, weeks_to_roll):

	homePct, homePts, homeDiff, homeAllowed = calc_stats(stats, home, weeks_to_roll)
	awayPct, awayPts, awayDiff, awayAllowed = calc_stats(stats, away, weeks_to_roll)

	return [awayPct, homePct, awayPts, homePts, awayAllowed, homeAllowed]

def calc_stats(stats, team, weeks_to_roll):

		pct = sum(stats[team]["wins"][-weeks_to_roll:]) / weeks_to_roll
		avgPts = sum(stats[team]["points"][-weeks_to_roll:]) / weeks_to_roll
		diff = sum(stats[team]["diff"][-weeks_to_roll:])
		allowed = sum(stats[team]["allowed"][-weeks_to_roll:]) / weeks_to_roll

		return pct, avgPts, diff, allowed


def load_model(filepath):

	return joblib.load(filepath)