import pandas as pd
import numpy as np

from sklearn.externals import joblib

def read_data_from_file(filepath, y_col, x_cols_to_drop):

	data = pd.read_csv(filepath)

	y = data[y_col]
	X = data.drop(x_cols_to_drop, axis=1, inplace=False)

	return X, y

def read_data_groupedby_week(filepath, y_col, x_cols_to_drop, group_by):

	data = pd.read_csv(filepath)

	grouped = {}
	for name, group in data.groupby(group_by):
		y = group[y_col]
		X = group.drop(x_cols_to_drop, axis=1, inplace=False)

		grouped[name] = (X, y)

	return grouped

def add_to_stats(stats, rd, tracked_stats):

	def add_to_stats_internal(stats, team, to_add):

		if team not in stats:
			stats[team] = dict([(x,[]) for x in tracked_stats])
			
		for idx,s in enumerate(tracked_stats):
			stats[team][s].append(to_add[idx])

	add_to_stats_internal(stats, rd.home, [rd.homeWin, rd.homePts, rd.awayPts, rd.homeYards, rd.awayYards])
	add_to_stats_internal(stats, rd.away, [1 - rd.homeWin, rd.awayPts, rd.homePts, rd.awayYards, rd.homeYards])

def calc_features(stats, game_info, weeks_to_roll, tracked_stats):

	home_pct, home_pts, home_allowed, home_yards, home_yards_allowed = calc_stats(stats, game_info.home, weeks_to_roll, tracked_stats)
	away_pct, away_pts, away_allowed, away_yards, away_yards_allowed = calc_stats(stats, game_info.away, weeks_to_roll, tracked_stats)

	return [
		away_pct,
		home_pct,
		away_pts - away_allowed,
		home_pts - home_allowed,
		away_yards,
		home_yards,
	]

def calc_stats(stats, team, weeks_to_roll, tracked_stats):
 
	def do_calculation(team_stats, stat, length):
		return sum(team_stats[stat][-weeks_to_roll:]) / len(team_stats[stat][-weeks_to_roll:])

	team_stats = stats[team]

	return tuple([do_calculation(team_stats, x, weeks_to_roll) for x in tracked_stats])


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