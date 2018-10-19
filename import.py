import csv
import os

import numpy as np

def transform_input_to_output(input_f, output_f, weeks_to_roll):

	teamRecord = {}

	csv_reader = csv.reader(input_f)
	csv_writer = csv.writer(output_f)

	for row in csv_reader:
		winner = row[4]
		losser = row[6]

		isHomeWinner = row[5] != "@"

		if winner not in teamRecord:
			teamRecord[winner] = []
		
		if losser not in teamRecord:
			teamRecord[losser] = []
		
		winnerRecord = teamRecord[winner][-weeks_to_roll:]
		winnerPct = sum(winnerRecord) / weeks_to_roll

		losserRecord = teamRecord[losser][-weeks_to_roll:]
		losserPct = sum(losserRecord) / weeks_to_roll

		week = int(row[0])
		
		if week > weeks_to_roll:
			result = []

			if isHomeWinner:
				result = [losser, winner, losserPct, winnerPct, 1]
			else:
				result = [winner, losser, winnerPct, losserPct, 0]

			csv_writer.writerow(result)
		
		teamRecord[winner].append(1)
		teamRecord[losser].append(0)

files = np.arange(start=2014, stop=2019)

files = [2018]

rolling_windows = [2, 3, 4, 5, 6]


for weeks_to_roll in rolling_windows:

	output_filename = f"output\\{weeks_to_roll}trainingdata.csv"

	if os.path.isfile(output_filename):
		os.remove(output_filename)

	with open(output_filename, "a") as output_f:
		output_f.write("away,home,away_pct,home_pct,home_win\n")

	for f in files:
		with open(f"input\\{f}.csv", "r") as input_f:
			with open(output_filename, "a", newline='') as output_f:
				transform_input_to_output(input_f, output_f, weeks_to_roll)