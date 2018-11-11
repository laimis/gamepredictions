import unittest

import nba.scraper as scraper

import datetime

class TestScraper(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		super(TestScraper, cls).setUpClass()

		cls.links = scraper.get_boxscore_links(2018, 11, 8)
		cls.box_score = scraper.get_boxscore_details(2018, 11, 8, cls.links[0])

		cls.games = scraper.get_games(datetime.date(2018,11,11))

	def test_total_number_of_links_should_match(self):

		self.assertEqual(4, len(self.links))

	def test_box_score_summary_correct(self):

		self.assertEqual(24, len(self.box_score.away.entries) + len(self.box_score.home.entries))

	def test_matchup_properly_assigns_stats(self):

		self.assertEqual("mil", self.box_score.away.team_name, "away team matches")
		self.assertEqual("gsw", self.box_score.home.team_name, "home team matches")

		self.assertTrue(self.box_score.away.away, "away team should be away")
		self.assertFalse(self.box_score.home.away, "home team should be home")

	def test_games_match(self):

		self.assertEqual(6, len(self.games))