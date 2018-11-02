import csv
import os

import nba.parser as parser
import nba.features as features

def get_feature_headers():
	return "year,counter,away,home,home_win,away_pct,home_pct,away_diff,home_diff\n"

def generate_output_and_stats(year, file_path):

	stats = {}
	output = []

	with open(file_path, "r") as input_f:
		csv_reader = csv.reader(input_f)

		next(csv_reader, None)

		counter = 1
		for row in csv_reader:
			game_info = parser.NBAGame(row, counter)
			features.add_to_stats(stats, game_info)
			counter += 1

			if counter > 200:
				calculated_features = features.calc_features(stats, game_info)
				output.append([year,game_info.counter,game_info.away,game_info.home,game_info.home_win] + calculated_features)

	return output, stats

def transform_csv(input_file, output_f, year):

	output, _ = generate_output_and_stats(year, input_file)
	csv_writer = csv.writer(output_f)
	csv_writer.writerows(output)