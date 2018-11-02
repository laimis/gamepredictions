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