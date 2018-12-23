import unittest
import datetime

import nba.database as database
import nba.scraper as scraper


class TestDatabase(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		super(TestDatabase, cls).setUpClass()

		date = datetime.date(2018,11,9)

		cls.games = database.get_games(date)

		cls.game = database.get_game_stats("4144")

		cls.lines = database.get_lines_with_daterange(date, date)

	def test_get_games_returns_correct_games(self):
		
		self.assertEqual(7, len(self.games), "number of games should match")

	def test_first_game_correct(self):

		self.assertEqual("9096", self.games[0].id, "first game's away team match")
		self.assertEqual("det", self.games[0].away, "first game's away team match")
		self.assertEqual("atl", self.games[0].home, "first game's home team match")

	def test_last_game_correct(self):

		self.assertEqual("9102", self.games[-1].id, "first game's away team match")
		self.assertEqual("bos", self.games[-1].away, "first game's away team match")
		self.assertEqual("uta", self.games[-1].home, "first game's home team match")

	def test_game_teams_correct(self):

		self.assertEqual("hou", self.game.away, "away team matches")
		self.assertEqual("lal", self.game.home, "home team matches")

	def test_away_game_stats(self):

		away_stats = self.game.away_stats
		self.assertEqual(31, away_stats.fields_goals_made)
		self.assertEqual(73, away_stats.fields_goals_attempted)

		self.assertEqual(12, away_stats.threes_made)
		self.assertEqual(29, away_stats.threes_attempted)

		self.assertEqual(34, away_stats.free_throws_made)
		self.assertEqual(50, away_stats.free_throws_attemped)

		self.assertEqual(14, away_stats.offensive_rebounds)
		self.assertEqual(33, away_stats.defense_rebounds)

		self.assertEqual(22, away_stats.assists)
		self.assertEqual(7, away_stats.steals)
		self.assertEqual(3, away_stats.blocks)
		self.assertEqual(13, away_stats.turnovers)
		self.assertEqual(30, away_stats.fouls)
		self.assertEqual(108, away_stats.points)

	def test_home_game_stats(self):

		home_stats = self.game.home_stats
		self.assertEqual(28, home_stats.fields_goals_made)
		self.assertEqual(79, home_stats.fields_goals_attempted)

		self.assertEqual(3, home_stats.threes_made)
		self.assertEqual(10, home_stats.threes_attempted)

		self.assertEqual(31, home_stats.free_throws_made)
		self.assertEqual(39, home_stats.free_throws_attemped)

		self.assertEqual(11, home_stats.offensive_rebounds)
		self.assertEqual(25, home_stats.defense_rebounds)

		self.assertEqual(16, home_stats.assists)
		self.assertEqual(7, home_stats.steals)
		self.assertEqual(3, home_stats.blocks)
		self.assertEqual(11, home_stats.turnovers)
		self.assertEqual(32, home_stats.fouls)
		self.assertEqual(90, home_stats.points)

	def test_lines_correct(self):

		self.assertEqual(7, len(self.lines), "line number should match")