import unittest
import datetime

import database
import scraper


class TestDatabase(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		super(TestDatabase, cls).setUpClass()

		date = datetime.date(2018,11,9)
		cls.games = database.get_games(date)

		cls.away_stats = database.get_game_stats("167", "det")
		cls.home_stats = database.get_game_stats("167", "atl")

		# entry_one = scraper.BoxScoreEntry("mil","brogdon", [])
		# entry_one.minutes = 1
		# entry_one.field_goals_made = 2
		# entry_one.field_goals_attemped = 3
		# entry_one.threes_made = 4
		# entry_one.threes_attempted = 5
		# entry_one.free_throws_made = 6
		# entry_one.free_throws_attempted = 7
		# entry_one.offensive_rebounds = 8
		# entry_one.defensive_rebounds = 9
		# entry_one.assists = 10
		# entry_one.steals = 11
		# entry_one.blocks = 12
		# entry_one.blocks = 13
		# entry_one.turnovers = 14
		# entry_one.personal_fouls = 15
		# entry_one.points = 16

		# entry_two = scraper.BoxScoreEntry("gsw","curry", [])
		# entry_two.minutes = 1
		# entry_two.field_goals_made = 2
		# entry_two.field_goals_attemped = 3
		# entry_two.threes_made = 4
		# entry_two.threes_attempted = 5
		# entry_two.free_throws_made = 6
		# entry_two.free_throws_attempted = 7
		# entry_two.offensive_rebounds = 8
		# entry_two.defensive_rebounds = 9
		# entry_two.assists = 10
		# entry_two.steals = 11
		# entry_two.blocks = 12
		# entry_two.blocks = 13
		# entry_two.turnovers = 14
		# entry_two.personal_fouls = 15
		# entry_two.points = 16

		# box_score = scraper.BoxScore(2011,11,8,[entry_one, entry_two])

		# database.insert_box_score(box_score)

	# def test_successful_setup(self):

	# 	self.assertTrue(True, "fake test just to run good stuff in the setup")

	def test_get_games_returns_correct_games(self):
		
		self.assertEqual(7, len(self.games), "number of games should match")

	def test_first_game_correct(self):

		self.assertEqual("167", self.games[0].id, "first game's away team match")
		self.assertEqual("det", self.games[0].away, "first game's away team match")
		self.assertEqual("atl", self.games[0].home, "first game's home team match")

	def test_last_game_correct(self):

		self.assertEqual("173", self.games[-1].id, "first game's away team match")
		self.assertEqual("bos", self.games[-1].away, "first game's away team match")
		self.assertEqual("uta", self.games[-1].home, "first game's home team match")

	def test_away_game_stats(self):

		self.assertEqual(46, self.away_stats.fields_goals_made)
		self.assertEqual(97, self.away_stats.fields_goals_attempted)

		self.assertEqual(20, self.away_stats.threes_made)
		self.assertEqual(47, self.away_stats.threes_attempted)

		self.assertEqual(12, self.away_stats.free_throws_made)
		self.assertEqual(19, self.away_stats.free_throws_attemped)

		self.assertEqual(10, self.away_stats.offensive_rebounds)
		self.assertEqual(34, self.away_stats.defense_rebounds)

		self.assertEqual(30, self.away_stats.assists)
		self.assertEqual(10, self.away_stats.steals)
		self.assertEqual(6, self.away_stats.blocks)
		self.assertEqual(10, self.away_stats.turnovers)
		self.assertEqual(31, self.away_stats.fouls)
		self.assertEqual(124, self.away_stats.points)

	def test_home_game_stats(self):

		self.assertEqual(36, self.home_stats.fields_goals_made)
		self.assertEqual(79, self.home_stats.fields_goals_attempted)

		self.assertEqual(7, self.home_stats.threes_made)
		self.assertEqual(28, self.home_stats.threes_attempted)

		self.assertEqual(30, self.home_stats.free_throws_made)
		self.assertEqual(40, self.home_stats.free_throws_attemped)

		self.assertEqual(9, self.home_stats.offensive_rebounds)
		self.assertEqual(44, self.home_stats.defense_rebounds)

		self.assertEqual(17, self.home_stats.assists)
		self.assertEqual(6, self.home_stats.steals)
		self.assertEqual(2, self.home_stats.blocks)
		self.assertEqual(16, self.home_stats.turnovers)
		self.assertEqual(21, self.home_stats.fouls)
		self.assertEqual(109, self.home_stats.points)

	