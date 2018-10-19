import csv
import os

import numpy as np

def transform_input_to_output(input_f, weeks_to_roll):

	teamRecord = {}
	points = {}
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

		if winner not in teamRecord:
			teamRecord[winner] = []
			points[winner] = []
		
		if losser not in teamRecord:
			teamRecord[losser] = []
			points[losser] = []
		
		winnerRecord = teamRecord[winner][-weeks_to_roll:]
		winnerPct = sum(winnerRecord) / weeks_to_roll
		winnerAvgPts = sum(points[winner][-weeks_to_roll:]) / weeks_to_roll

		losserRecord = teamRecord[losser][-weeks_to_roll:]
		losserPct = sum(losserRecord) / weeks_to_roll
		losserAvgPts = sum(points[losser][-weeks_to_roll:]) / weeks_to_roll

		week = int(row[0])
		
		if week > weeks_to_roll:
			result = []

			if isHomeWinner:
				output.append([losser, winner, losserPct, winnerPct, losserAvgPts, winnerAvgPts, 1])
			else:
				output.append([winner, losser, winnerPct, losserPct, winnerAvgPts, losserAvgPts, 0])
		
		teamRecord[winner].append(1)
		teamRecord[losser].append(0)

		points[winner].append(winnerPts)
		points[losser].append(losserPts)
	
	return output

files = np.arange(start=2014, stop=2019)

# files = [2018]

rolling_windows = [2, 3, 4, 5, 6]


for weeks_to_roll in rolling_windows:

	output_filename = f"output\\{weeks_to_roll}trainingdata.csv"

	if os.path.isfile(output_filename):
		os.remove(output_filename)

	with open(output_filename, "a") as output_f:
		output_f.write("away,home,away_pct,home_pct,away_pts,home_pts,home_win\n")

	for f in files:
		with open(f"input\\{f}.csv", "r") as input_f:
			with open(output_filename, "a", newline='') as output_f:
				output = transform_input_to_output(input_f, weeks_to_roll)
				csv_writer = csv.writer(output_f)
				csv_writer.writerows(output)