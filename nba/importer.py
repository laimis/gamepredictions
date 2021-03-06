import csv
import os

import nba.domain as domain
import nba.features as features

def generate_stats(file_path):
	stats = {}
	
	with open(file_path, "r") as input_f:
		csv_reader = csv.reader(input_f)

		next(csv_reader, None)

		counter = 1
		for row in csv_reader:
			game_info = domain.NBAGame(counter, row)
			counter += 1
			features.add_to_stats(stats, game_info)

	return stats

def generate_output_row(year, stats, game_info:domain.NBAGame):
	calculated_features = features.calc_features(stats, game_info)

	game_features = [year,game_info.date.strftime("%Y-%m-%d"),game_info.counter,game_info.away,game_info.home,game_info.home_win]
	
	if (hasattr(game_info, "line_team")):
		spread_features = [game_info.line_team,game_info.line_spread,game_info.spread_correct,game_info.spread_covered]
	else:
		spread_features = ["",0,False,False]

	return game_features + calculated_features + spread_features

def generate_output_and_stats(year, file_path):

	stats = {}
	output = []

	with open(file_path, "r") as input_f:
		csv_reader = csv.reader(input_f)

		next(csv_reader, None)

		counter = 1
		for row in csv_reader:
			game_info = domain.NBAGame(counter, row)
			counter += 1

			if counter > 100:
				output_row = generate_output_row(year, stats, game_info)
				output.append(output_row)

			features.add_to_stats(stats, game_info)

	return output, stats

def transform_csv(input_file, output_f, year):

	output, _ = generate_output_and_stats(year, input_file)
	csv_writer = csv.writer(output_f)
	csv_writer.writerows(output)