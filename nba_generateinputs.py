import datetime
import csv

from typing import List

import nba.domain as domain
import nba.database as database

def generate_stats(year):
	start = datetime.date(year,10,1)
	end = datetime.date(year+1,4,10)
	games:List[domain.Game] = database.get_games_with_daterange(start, end)

	with open(f"input\\nba\\{year}.csv", "w", newline='') as output_f:

		writer = csv.writer(output_f)
		
		for g in games:

			writer.writerow(g.to_output())

if __name__ == "__main__":
	
	for y in [2014,2015,2016,2017,2018]:
		generate_stats(y)