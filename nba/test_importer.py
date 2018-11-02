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

		self.assertEqual(1074, len(self.output))
	
	def test_first_row_correct(self):

		self.assertEqual(
			[2015, 200, 'Phoenix Suns', 'New Orleans Pelicans', 1, 0.5384615384615384, 0.21428571428571427, 3.92307692307692, -6.857142857142861],
			self.output[0]
		)

	def test_last_row_correct(self):

		self.assertEqual(
			[2015, 1273, 'Oklahoma City Thunder', 'San Antonio Spurs', 1, 0.65, 0.75, 8.650000000000006, 8.149999999999991],
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
			"wins": 42, "scored": 8335, "allowed": 8456
		}

		team_stats = self.stats[team]

		for s in team_stats:
			self.assertEqual(verify[s], sum(team_stats[s]), f"{s} should match for {team}")

if __name__ == '__main__':
    unittest.main()