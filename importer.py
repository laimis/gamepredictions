import csv
import os

import numpy as np
import common

def generate_output_and_stats(year, file_path, weeks_to_roll):

	stats = {}
	output = []

	with open(file_path, "r") as input_f:
		csv_reader = csv.reader(input_f)

		for row in csv_reader:
			parsed = common.RowDef(row)

			# WHAT TO DO WITH TIESw
			# if winnerPts == losserPts:
			# 	continue
			
			if parsed.week > weeks_to_roll and parsed.week < 17:
				features = common.calc_features(stats, parsed, weeks_to_roll)
				output.append([year,parsed.week,parsed.away,parsed.home,parsed.homeWin] + features)
			
			common.add_to_stats(stats, parsed)
	
	return output, stats


def transform_csv(rolling_windows, train_or_test, years):

	for weeks_to_roll in rolling_windows:

		output_filename = f"output\\{train_or_test}\\{weeks_to_roll}.csv"

		if os.path.isfile(output_filename):
			os.remove(output_filename)

		with open(output_filename, "a") as output_f:
			output_f.write(common.get_feature_headers())

		for f in years:
			with open(output_filename, "a", newline='') as output_f:
				output, _ = generate_output_and_stats(f, f"input\\{f}.csv", weeks_to_roll)
				csv_writer = csv.writer(output_f)
				csv_writer.writerows(output)

if __name__ == '__main__':
	
	rolling_windows = common.weeks_to_try()
	
	transform_csv(rolling_windows, "train", [2013,2014,2015,2016])
	
	transform_csv(rolling_windows, "test", [2017,2018])
