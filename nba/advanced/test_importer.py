import unittest

import importer as importer
import features as features

class TestImport(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		super(TestImport, cls).setUpClass()

		cls.stats = importer.generate_output_and_stats(2015)

	def test_total_rows(self):

		self.assertEqual(1094, len(self.output))
	
	def test_first_row_correct(self):

		self.assertEqual(
			[2015, '2015-11-09', 100, 'Portland Trail Blazers', 'Denver Nuggets', 1, 0.5714285714285714, 0.3333333333333333, 1.7142857142857082, -6.166666666666671],
			self.output[0]
		)

	def test_last_row_correct(self):

		self.assertEqual(
			[2015, '2016-04-09', 1193, 'Oklahoma City Thunder', 'Sacramento Kings', 1, 0.7, 0.4, 7.300000000000011, 1.2000000000000028],
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
			"wins": 40, "scored": 8099, "allowed": 8235, "date": 0
		}

		team_stats = self.stats[team]

		for s in team_stats:
			if s != "date":
				self.assertEqual(verify[s], sum(team_stats[s]), f"{s} should match for {team}")

if __name__ == '__main__':
    unittest.main()