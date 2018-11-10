import scraper
import database
import datetime

if __name__ == "__main__":

	dt = datetime.date(2015,10,27)
	end = datetime.date(2016,4,10)

	while dt < end:
		
		print(datetime.datetime.now(),"processing",dt)

		links = scraper.get_boxscore_links(dt.year, dt.month, dt.day)

		print("    ",datetime.datetime.now(),"received ",len(links))

		for l in links:
			print("    ",datetime.datetime.now(),"getting ",l)

			game = scraper.get_boxscore_details(dt.year, dt.month, dt.day, l)

			print("    ",datetime.datetime.now(),"saving ",game)

			database.insert_box_score(game)

		dt = dt + datetime.timedelta(days=1)