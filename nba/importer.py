import csv
import os

import nba.parser as parser
import nba.features as features

def generate_output_and_stats(year, file_path):

	stats = {}
	output = []

	with open(file_path, "r") as input_f:
		csv_reader = csv.reader(input_f)

		counter = 1
		for row in csv_reader:
			game_info = parser.NBAGame(counter, row)
			counter += 1

			if counter > 100:
				calculated_features = features.calc_features(stats, game_info)
				output.append([year,game_info.date.strftime("%Y-%m-%d"),game_info.counter,game_info.away,game_info.home,game_info.home_win] + calculated_features)

			features.add_to_stats(stats, game_info)

	return output, stats

def transform_csv(input_file, output_f, year):

	output, _ = generate_output_and_stats(year, input_file)
	csv_writer = csv.writer(output_f)
	csv_writer.writerows(output)