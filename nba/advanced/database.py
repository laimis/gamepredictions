import psycopg2
import psycopg2.extras

import scraper

__connection_string__ = "host='localhost' dbname='bets' user='bet' password='bet'"

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