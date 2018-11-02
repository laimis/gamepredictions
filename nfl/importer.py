import csv
import os

import numpy as np
import common
import nfl.parser as parser

def get_tracked_stats():
	return ["wins", "points", "allowed", "yards", "yards_allowed"]

def generate_output_and_stats(year, file_path, weeks_to_roll):

	stats = {}
	output = []

	with open(file_path, "r") as input_f:
		csv_reader = csv.reader(input_f)

		for row in csv_reader:
			game_info = parser.NFLGame(row)

			# WHAT TO DO WITH TIESw
			# if winnerPts == losserPts:
			# 	continue
			
			if game_info.week > weeks_to_roll and game_info.week < 17:
				features = common.calc_features(stats, game_info, weeks_to_roll, get_tracked_stats())
				output.append([year,game_info.week,game_info.away,game_info.home,game_info.homeWin] + features)
			
			common.add_to_stats(stats, game_info, get_tracked_stats())
	
	return output, stats


def transform_csv(weeks_to_roll, input_file, output_f, year):

	output, _ = generate_output_and_stats(year, input_file, weeks_to_roll)
	csv_writer = csv.writer(output_f)
	csv_writer.writerows(output)