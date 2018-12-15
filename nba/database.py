import psycopg2
import psycopg2.extras
import datetime

import nba.scraper as scraper
import nba.domain as domain

from typing import List

__connection_string__ = "host='localhost' dbname='bets' user='bet' password='bet'"

def __map_record_to_game__(record):
	stat_dict = {"fgm":0,"fga":0,"tpm":0,"tpa":0,"ftm":0,"fta":0,"oreb":0,"dreb":0,"assists":0,"steals":0,"blocks":0,"turnovers":0,"fouls":0,"points":0}

	for k in stat_dict:
		stat_dict[k] = record[f"away_{k}"]
		
	away_stats = domain.GameStats(stat_dict)

	for k in stat_dict:
		stat_dict[k] = record[f"home_{k}"]
		
	home_stats = domain.GameStats(stat_dict)

	return domain.Game(record["date"], record["gameid"], record["away"], record["home"], away_stats, home_stats)
		
def get_game_stats(gameid:str) -> domain.Game:

	with psycopg2.connect(__connection_string__) as conn:
		with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:

			cur.execute(
				"select * from gamestats where gameid = %s",
				[gameid]
			)

			record = cur.fetchone()

			game = __map_record_to_game__(record)

	return game

def get_games(date:datetime.date) -> List[domain.Game]:

	games:List[domain.Game] = []

	with psycopg2.connect(__connection_string__) as conn:
		with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:

			cur.execute("select * from games where date = %s order by home", [date])

			records = cur.fetchall()

			for r in records:
				games.append(get_game_stats(r["id"]))

	return games

def get_games_with_daterange(start:datetime.date, end:datetime.date) -> List[domain.Game]:

	games:List[domain.Game] = []

	with psycopg2.connect(__connection_string__) as conn:
		with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:

			cur.execute("select * from gamestats where date between %s and %s order by date", [start, end])

			records = cur.fetchall()

			for r in records:
				game_stat = __map_record_to_game__(r)
				games.append(game_stat)

	return games

def __insert_box_score_row__(cur: psycopg2.extensions.cursor, box_score_id:str, bse: scraper.BoxScoreEntry):
	
	cur.execute(
		"INSERT INTO gamerows \
		(gameid,team,name,minutes,fgm,fga,tpm,tpa,ftm,fta,oreb,dreb,assists,steals,blocks,turnovers,fouls,points) VALUES \
		(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
		(box_score_id, bse.team, bse.name, bse.minutes, bse.field_goals_made, bse.field_goals_attemped, bse.threes_made, bse.threes_attempted, bse.free_throws_made, bse.free_throws_attempted, bse.offensive_rebounds, bse.defensive_rebounds, bse.assists, bse.steals, bse.blocks, bse.turnovers, bse.personal_fouls, bse.points)
	)

def insert_box_score(box_score: scraper.BoxScore):

	with psycopg2.connect(__connection_string__) as conn:

		box_score_id = None
		with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:

			cur.execute(
				"INSERT INTO games (date,away, home) VALUES (%s, %s, %s) RETURNING id",
				(f"{box_score.year}-{box_score.month}-{box_score.day}", box_score.away.team_name, box_score.home.team_name)
			)

			box_score_id = cur.fetchone()[0]
			
			conn.commit()

		with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:

			all_entries = box_score.away.entries + box_score.home.entries
			for e in all_entries:
				__insert_box_score_row__(cur, box_score_id, e)

			conn.commit()

def insert_line(dt:datetime.date, team:str, val:float):

	with psycopg2.connect(__connection_string__) as conn:

		with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:

			cur.execute(
				"INSERT INTO gamelines (date,team,value) VALUES (%s, %s, %s)",
				(f"{dt.year}-{dt.month:02}-{dt.day:02}", team, val)
			)
			
			conn.commit()

def update_aggregate_stats():
	with psycopg2.connect(__connection_string__) as conn:

		with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:

			script = ""
			with open('nba\\dailyrun.sql', 'r') as script_file:
				script=script_file.read()

			cur.execute(script)

			conn.commit()