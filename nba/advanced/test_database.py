import unittest

import database
import scraper

class TestDatabase(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		super(TestDatabase, cls).setUpClass()

		entry_one = scraper.BoxScoreEntry("mil","brogdon", [])
		entry_one.minutes = 1
		entry_one.field_goals_made = 2
		entry_one.field_goals_attemped = 3
		entry_one.threes_made = 4
		entry_one.threes_attempted = 5
		entry_one.free_throws_made = 6
		entry_one.free_throws_attempted = 7
		entry_one.offensive_rebounds = 8
		entry_one.defensive_rebounds = 9
		entry_one.assists = 10
		entry_one.steals = 11
		entry_one.blocks = 12
		entry_one.blocks = 13
		entry_one.turnovers = 14
		entry_one.personal_fouls = 15
		entry_one.points = 16

		entry_two = scraper.BoxScoreEntry("gsw","curry", [])
		entry_two.minutes = 1
		entry_two.field_goals_made = 2
		entry_two.field_goals_attemped = 3
		entry_two.threes_made = 4
		entry_two.threes_attempted = 5
		entry_two.free_throws_made = 6
		entry_two.free_throws_attempted = 7
		entry_two.offensive_rebounds = 8
		entry_two.defensive_rebounds = 9
		entry_two.assists = 10
		entry_two.steals = 11
		entry_two.blocks = 12
		entry_two.blocks = 13
		entry_two.turnovers = 14
		entry_two.personal_fouls = 15
		entry_two.points = 16

		box_score = scraper.BoxScore(2018,11,8,[entry_one, entry_two])

		database.insert_box_score(box_score)

	def test_successful_setup(self):

		self.assertTrue(True, "fake test just to run good stuff in the setup")