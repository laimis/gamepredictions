import psycopg2
import psycopg2.extras

import scraper

__connection_string__ = "host='localhost' dbname='bets' user='bet' password='bet'"

def insert_box_score(box_score: scraper.BoxScore):

	with psycopg2.connect(__connection_string__) as conn:
		with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:

			cur.execute(
				"INSERT INTO games (date,away, home) VALUES (%s, %s, %s) RETURNING id",
				(f"{box_score.year}-{box_score.month}-{box_score.day}", box_score.away.team_name, box_score.home.team_name)
			)

			id = cur.fetchone()[0]
			
			conn.commit()

			return id

entry_one = scraper.BoxScoreEntry("mil","brogdon", [])
entry_two = scraper.BoxScoreEntry("gsw","brogdon", [])

box_score = scraper.BoxScore(2018,11,8,[entry_one, entry_two])

id = insert_box_score(box_score)

print(id)