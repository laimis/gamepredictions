import csv
import os

import numpy as np
import common

def transform_input_to_output(input_f, weeks_to_roll):

	stats = {}
	output = []

	csv_reader = csv.reader(input_f)

	for row in csv_reader:
		winner = row[4]
		losser = row[6]

		winnerPts = int(row[8])
		losserPts = int(row[9])

		if winnerPts == losserPts:
			continue
		
		diff = int(winnerPts) - int(losserPts)

		isHomeWinner = row[5] != "@"

		away = winner
		home = losser
		homeWin = 0

		if isHomeWinner:
			away = losser
			home = winner
			homeWin = 1

		week = int(row[0])
		
		if week > weeks_to_roll:
			features = common.calc_features(stats, home, away, weeks_to_roll)
			output.append([losser,winner,homeWin] + features)
		
		common.add_to_stats(stats, winner, 1, winnerPts, losserPts)
		common.add_to_stats(stats, losser, 0, losserPts, winnerPts)
	
	return output


def transform_csv(rolling_windows, train_or_test, years):

	for weeks_to_roll in rolling_windows:

		output_filename = f"output\\{train_or_test}\\{weeks_to_roll}.csv"

		if os.path.isfile(output_filename):
			os.remove(output_filename)

		with open(output_filename, "a") as output_f:
			output_f.write("away,home,home_win,away_pct,home_pct,away_pts,home_pts,away_diff,home_diff\n")

		for f in years:
			with open(f"input\\{f}.csv", "r") as input_f:
				with open(output_filename, "a", newline='') as output_f:
					output = transform_input_to_output(input_f, weeks_to_roll)
					csv_writer = csv.writer(output_f)
					csv_writer.writerows(output)

if __name__ == '__main__':
	inputs = np.arange(2,7)

	rolling_windows = [2, 3, 4, 5, 6]
	
	transform_csv(rolling_windows, "train", [2013,2014,2015,2016])
	transform_csv(rolling_windows, "test", [2017,2018])
