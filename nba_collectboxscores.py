import nba.scraper as scraper
import nba.database as database
import nba.domain as domain
import datetime
import time
import csv

from typing import List

def get_season_box_scores():
	dt = datetime.date(2018,10,17)
	end = datetime.date(2018,11,12)

	while dt < end:
		
		print(datetime.datetime.now(),"processing",dt)

		get_box_scores_for_date(dt)

		dt = dt + datetime.timedelta(days=1)

def get_season_lines():
	dt = datetime.date(2016,11,21)
	end = datetime.date(2017,4,10)

	while dt < end:
		
		print(datetime.datetime.now(),"processing",dt)

		get_lines(dt)

		dt = dt + datetime.timedelta(days=1)

		time.sleep(1)

def get_box_scores_for_date(dt:datetime.date):

	print("    processing",dt)

	links = scraper.get_boxscore_links(dt.year, dt.month, dt.day)

	print("    ",datetime.datetime.now(),"received ",len(links))

	for l in links:
		print("    ",datetime.datetime.now(),"getting ",l)

		game = scraper.get_boxscore_details(dt.year, dt.month, dt.day, l)

		print("    ",datetime.datetime.now(),"saving ",game)

		database.insert_box_score(game)

def get_lines(dt:datetime.date):

	lines:List[scraper.ESPNGameLine] = scraper.get_lines(dt)

	for l in lines:
		database.insert_line(dt, l.team, l.spread)

def update_aggregate_stats():

	database.update_aggregate_stats()

def generate_stats():

	def generate_stats_for_year(year):
		header = "date,away,away_fgm,away_fga,away_tpm,away_tpa,away_ftm,away_fta,away_oreb,away_dreb,away_assists,away_steals,away_blocks,away_turnovers,away_fouls,away_points,home,home_fgm,home_fga,home_tpm,home_tpa,home_ftm,home_fta,home_oreb,home_dreb,home_assists,home_steals,home_blocks,home_turnovers,home_fouls,home_points,line_team,line_spread".split(",")

		start = datetime.date(year,10,1)
		end = datetime.date(year+1,4,10)
		games:List[domain.Game] = database.get_games_with_daterange(start, end)
		lines:List[scraper.ESPNGameLine] = database.get_lines_with_daterange(start, end)
		index:domain.GameLineIndex = domain.GameLineIndex(lines)

		with open(f"input\\nba\\{year}.csv", "w", newline='') as output_f:

			writer = csv.writer(output_f)

			writer.writerow(header)
			
			for g in games:

				line = index.get(g.date, g.home, g.away)
				line_parts = [None,None]
				if line != None:
					line_parts = [line.team, line.spread]

				writer.writerow(g.to_output() + line_parts)

	for y in [2014,2015,2016,2017,2018]:
		generate_stats_for_year(y)

if __name__ == "__main__":

	date = database.get_last_date()

	dt = date + datetime.timedelta(days=1)

	#dt = datetime.datetime.now() + datetime.timedelta(days=-1)

	get_box_scores_for_date(dt)

	get_lines(dt)
		
	update_aggregate_stats()

	generate_stats()