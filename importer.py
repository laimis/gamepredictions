import csv
import os

import numpy as np

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

		if winner not in stats:
			stats[winner] = {"wins":[], "points":[], "diff":[], "allowed":[]}
		
		if losser not in stats:
			stats[losser] = {"wins":[], "points":[], "diff":[], "allowed":[]}
		
		winnerPct = sum(stats[winner]["wins"][-weeks_to_roll:]) / weeks_to_roll
		winnerAvgPts = sum(stats[winner]["points"][-weeks_to_roll:]) / weeks_to_roll
		winnerDiff = sum(stats[winner]["diff"][-weeks_to_roll:])
		winnerAllowed = sum(stats[winner]["allowed"][-weeks_to_roll:]) / weeks_to_roll

		losserPct = sum(stats[losser]["wins"][-weeks_to_roll:]) / weeks_to_roll
		losserAvgPts = sum(stats[losser]["points"][-weeks_to_roll:]) / weeks_to_roll
		losserDiff = sum(stats[losser]["diff"][-weeks_to_roll:])
		losserAllowed = sum(stats[losser]["allowed"][-weeks_to_roll:]) / weeks_to_roll

		week = int(row[0])
		
		if week > weeks_to_roll:
			result = []

			if isHomeWinner:
				output.append(
					# [losser, winner, losserPct, winnerPct, losserAvgPts, winnerAvgPts, losserDiff, winnerDiff, losserAllowed, winnerAllowed, 1]
					# [losser, winner, losserPct, winnerPct, losserAvgPts, winnerAvgPts, losserDiff, winnerDiff, 1]
					[losser, winner, losserPct, winnerPct, losserAvgPts, winnerAvgPts, losserAllowed, winnerAllowed, 1]
				)
			else:
				output.append(
					# [winner, losser, winnerPct, losserPct, winnerAvgPts, losserAvgPts, winnerDiff, losserDiff, winnerAllowed, losserAllowed, 0]
					# [winner, losser, winnerPct, losserPct, winnerAvgPts, losserAvgPts, winnerDiff, losserDiff, 0]
					[winner, losser, winnerPct, losserPct, winnerAvgPts, losserAvgPts, winnerAllowed, losserAllowed, 0]
				)
		
		stats[winner]["wins"].append(1)
		stats[winner]["points"].append(winnerPts)
		stats[winner]["diff"].append(diff)
		stats[winner]["allowed"].append(-losserPts)

		stats[losser]["wins"].append(0)
		stats[losser]["points"].append(losserPts)
		stats[losser]["diff"].append(-diff)
		stats[losser]["allowed"].append(-winnerPts)
	
	return output


	def generate_training_data(rolling_windows, years):

		for weeks_to_roll in rolling_windows:

		output_filename = f"output\\{weeks_to_roll}trainingdata.csv"

		if os.path.isfile(output_filename):
			os.remove(output_filename)

		with open(output_filename, "a") as output_f:
			output_f.write("away,home,away_pct,home_pct,away_pts,home_pts,away_diff,home_diff,home_win\n")

		for f in files:
			with open(f"input\\{f}.csv", "r") as input_f:
				with open(output_filename, "a", newline='') as output_f:
					output = transform_input_to_output(input_f, weeks_to_roll)
					csv_writer = csv.writer(output_f)
					csv_writer.writerows(output)

if __name__ == '__main__':
	inputs = np.arange(2,7)

	files = np.arange(start=2014, stop=2019)
	# files = [2018]
	rolling_windows = [2, 3, 4, 5, 6]

	generate_training_data(rolling_windows, files)