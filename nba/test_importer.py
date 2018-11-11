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
			[2015, '2015-11-09', 100, 'por', 'den', 1, 0.5714285714285714, 0.3333333333333333, 1.7142857142857082, -6.166666666666671, 0.4503296703296703, 0.2778125928125928],
			self.output[0]
		)

	def test_last_row_correct(self):

		self.assertEqual(
			[2015, '2016-04-09', 1193, 'okc', 'sac', 1, 0.7, 0.4, 7.300000000000011, 1.2000000000000028, 0.34682245386192745, 0.39065267671251447],
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
			"wins": 40, "scored": 8099, "allowed": 8235, "date": 0, "ftm": 35.30051187574503, "tpm": 30.90915325347887
		}

		team_stats = self.stats[team]

		for s in team_stats:
			if s != "date":
				self.assertEqual(verify[s], sum(team_stats[s]), f"{s} should match for {team}")

if __name__ == '__main__':
    unittest.main()