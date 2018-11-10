import csv
import os
import datetime

from typing import Tuple
from typing import Dict

import database as database
import features as features

def __get_season_dates__(year:int) -> Tuple[datetime.date, datetime.date]:
	return (datetime.date(2017,10,6), datetime.date(2018,4,9))

def generate_output_and_stats(year:int) -> Dict:

	start, end = __get_season_dates__(year)

	dt = start

	stats:Dict = {}

	while dt < end:
		
		print(dt)
		counter = 1

		games = database.get_games(dt)

		for g in games:

			g.away_stats = database.get_game_stats(g.id, g.away)
			g.home_stats = database.get_game_stats(g.id, g.home)

			counter += 1

			#if counter > 100:
			#	calculated_features = features.calc_features(stats, g)
			# 	output.append([year,game_info.date.strftime("%Y-%m-%d"),game_info.counter,game_info.away,game_info.home,game_info.home_win] + calculated_features)

			features.add_to_stats(stats, g)

		dt = dt + datetime.timedelta(days=1)

	return stats

def transform_csv(output_f, year):

	output, _ = generate_output_and_stats(year)
	csv_writer = csv.writer(output_f)
	csv_writer.writerows(output)