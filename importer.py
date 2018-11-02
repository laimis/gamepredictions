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


def transform_csv(weeks_to_roll, input_file, output_f, year):

	output, _ = generate_output_and_stats(year, input_file, weeks_to_roll)
	csv_writer = csv.writer(output_f)
	csv_writer.writerows(output)

if __name__ == '__main__':
	
	rolling_windows = common.weeks_to_try()
	
	years_train = [2013,2014,2015,2016]
	years_test = [2017,2018]

	def call_transform(train_or_test, years, rolling_window):
		
		output_file = f"output\\nfl\\{train_or_test}\\{rolling_window}.csv"

		if os.path.isfile(output_file):
			os.remove(output_file)

		with open(output_file, "a", newline='') as output_f:
			output_f.write(common.get_feature_headers())
			for year in years:
				input_file = f"input\\nfl\\{year}.csv"
				transform_csv(rolling_window, input_file, output_f, year)

	for rolling_window in rolling_windows:
		call_transform("train", years_train, rolling_window)
		call_transform("test", years_test, rolling_window)