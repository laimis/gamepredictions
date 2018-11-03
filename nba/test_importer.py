import unittest

import nba.importer as importer
import nba.features as features
import common

class TestImport(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		super(TestImport, cls).setUpClass()

		cls.output, cls.stats = importer.generate_output_and_stats(2015, "input\\nba\\2015.csv")

	def test_total_rows(self):

		self.assertEqual(1174, len(self.output))
	
	def test_first_row_correct(self):

		self.assertEqual(
			[2015, '2015-11-09', 100, 'Portland Trail Blazers', 'Denver Nuggets', 1, 0.5714285714285714, 0.3333333333333333, 1.7142857142857082, -6.166666666666671, 1, 1],
			self.output[0]
		)

	def test_last_row_correct(self):

		self.assertEqual(
			[2015, '2016-04-30', 1273, 'Oklahoma City Thunder', 'San Antonio Spurs', 1, 0.6, 0.7, 13.5, 7.799999999999997, 0, 0],
			self.output[len(self.output)-1]
		)

	def test_stats_each_team_present(self):

		self.assertEqual(
			30, len(self.stats), "stats count should match"
		)

	def test_validate_stats(self):

		tracked_stats = features.tracked_stats

		for team in self.stats:
			team_stats = self.stats[team]
		
			for idx,k in enumerate(tracked_stats):
				self.assertTrue(k in team_stats, f"{k} present for {team}")

				self.assertEqual(
					len(team_stats[tracked_stats[idx]]), len(team_stats[tracked_stats[idx-1]]),
					f"unequal lenght stats for {team}"
				)

	def test_specific_stats_match(self):

		team = "Chicago Bulls"

		verify = {
			"wins": 42, "scored": 8335, "allowed": 8456, "date": 0
		}

		team_stats = self.stats[team]

		for s in team_stats:
			if s != "date":
				self.assertEqual(verify[s], sum(team_stats[s]), f"{s} should match for {team}")

if __name__ == '__main__':
    unittest.main()