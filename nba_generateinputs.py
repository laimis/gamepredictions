import datetime
import csv

from typing import List

import nba.domain as domain
import nba.database as database

def get_header():
	return "date,away,away_fgm,away_fga,away_tpm,away_tpa,away_ftm,away_fta,away_oreb,away_dreb,away_assists,away_steals,away_blocks,away_turnovers,away_fouls,away_points,home,home_fgm,home_fga,home_tpm,home_tpa,home_ftm,home_fta,home_oreb,home_dreb,home_assists,home_steals,home_blocks,home_turnovers,home_fouls,home_points".split(",")

def generate_stats(year):
	start = datetime.date(year,10,1)
	end = datetime.date(year+1,4,10)
	games:List[domain.Game] = database.get_games_with_daterange(start, end)

	with open(f"input\\nba\\{year}.csv", "w", newline='') as output_f:

		writer = csv.writer(output_f)

		writer.writerow(get_header())
		
		for g in games:

			writer.writerow(g.to_output())

if __name__ == "__main__":
	
	for y in [2014,2015,2016,2017,2018]:
		generate_stats(y)