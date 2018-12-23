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

		self.assertEqual(1094, len(self.output))
	
	def test_first_row_correct(self):

		self.assertEqual(
			[2015, '2015-11-09', 100, 'por', 'den', 1, 0.5714285714285714, 0.3333333333333333, 1.7142857142857082, -6.166666666666671, 0.4503296703296703, 0.2778125928125928, 8.714285714285714, 8.666666666666668, 45.57142857142857, 45.5, -1, -2, '', 0, False, True],
			self.output[0]
		)

	def test_last_row_correct(self):

		self.assertEqual(
			[2015, '2016-04-09', 1193, 'okc', 'sac', 1, 0.65, 0.35, 7.300000000000011, -1.4499999999999886, 0.34548591140245344, 0.34885483976095205, 10.05, 11.45, 50.85, 41.55, -1, -2, '', 0, False, True],
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

		team = "chi"

		verify = {
			"wins": 40,
			"scored": 8099,
			"allowed": 8235,
			"date": 0,
			"fg%": 35.30051187574503,
			"tp%":30.90915325347887,
			"ft%":71.18474354352571,
			"rebs":3708,
			"assists":1814,
			"turnovers":791,
			"streak":0
		}

		team_stats = self.stats[team]

		for s in team_stats:
			if s != "date":
				self.assertEqual(verify[s], sum(team_stats[s]), f"{s} should match for {team}")

if __name__ == '__main__':
    unittest.main()