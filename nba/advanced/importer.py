import csv
import os
import datetime

from typing import Tuple

import database

def __get_season_dates__(year:int) -> Tuple[datetime.date, datetime.date]:
	return (datetime.date(2017,10,6), datetime.date(2018,4,9))

def generate_output_and_stats(year:int):

	start, end = __get_season_dates__(year)

	dt = start

	while dt < end:
		
		counter = 1

		games = database.get_games(dt)

		for g in games:

			g.away_stats = database.get_game_stats(g.id, g.away)
			g.home_stats = database.get_game_stats(g.id, g.home)

			
			None
			# game_info = parser.NBAGame(row, counter)
			# counter += 1

			# if counter > 100:
			# 	calculated_features = features.calc_features(stats, game_info)
			# 	output.append([year,game_info.date.strftime("%Y-%m-%d"),game_info.counter,game_info.away,game_info.home,game_info.home_win] + calculated_features)

			# features.add_to_stats(stats, game_info)

def transform_csv(input_file, output_f, year):

	output, _ = generate_output_and_stats(year, input_file)
	csv_writer = csv.writer(output_f)
	csv_writer.writerows(output)