import database
import datetime

import csv

from typing import List

import domain

def generate_stats(year):
	start = datetime.date(year,10,1)
	end = datetime.date(year+1,4,10)
	games:List[domain.Game] = database.get_games_with_daterange(start, end)

	with open(f"{year}.csv", "w", newline='') as output_f:

		writer = csv.writer(output_f)
		
		for g in games:

			writer.writerow(g.to_output())

if __name__ == "__main__":
	
	for y in [2015,2016,2017,2018]:
		generate_stats(y)