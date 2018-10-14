import csv
import os

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

		teamRecord[winner].append(1)
		teamRecord[losser].append(0)
		
		print(row)
		print(isHomeWinner)

		winnerRecord = teamRecord[winner][-weeks_to_roll:]
		winnerPct = sum(winnerRecord) / weeks_to_roll

		losserRecord = teamRecord[losser][-weeks_to_roll:]
		losserPct = sum(losserRecord) / weeks_to_roll

		week = int(row[0])
		
		if week < weeks_to_roll + 1:
			continue

		result = []

		if isHomeWinner:
			result = [winnerPct, losserPct, 1]
		else:
			result = [losserPct, winnerPct, 0]

		csv_writer.writerow(result)

files = ["2014", "2015", "2016", "2017", "2018"]

output_filename = "processed.txt"

os.remove(output_filename)

with open(output_filename, "a") as output_f:
	output_f.write("home_pct,away_pct,home_win\n")

for f in files:
	with open(f"{f}.txt", "r") as input_f:
		with open(output_filename, "a", newline='') as output_f:
			transform_input_to_output(input_f, output_f, 3)