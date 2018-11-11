import database
import datetime

import csv

from typing import List

import domain

if __name__ == "__main__":
	
	year = 2015

	start = datetime.date(2015,10,1)
	end = datetime.date(2016,4,10)
	games:List[domain.Game] = database.get_games_with_daterange(start, end)

	with open(f"{year}.csv", "w", newline='') as output_f:

		writer = csv.writer(output_f)
		
		for g in games:

			writer.writerow(g.to_output())