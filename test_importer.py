import unittest

import importer
import common

class TestImport(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		super(TestImport, cls).setUpClass()

		cls.output, cls.stats = importer.generate_output_and_stats(2014, "input\\2014.csv", 4)

	def test_total_rows(self):

		self.assertEqual(179, len(self.output))

	def test_first_row_correct(self):

		self.assertEqual(
			[2014, 5, 'Minnesota Vikings', 'Green Bay Packers', 1, 0.5, 0.5, 1.75, -1, 3.4425, 3.065],
			self.output[0]
		)

	def test_last_row_correct(self):

		self.assertEqual(
			[2014, 16, 'Denver Broncos', 'Cincinnati Bengals', 1, 1.0, 0.75, 8.75, 4.75, 3.7025, 3.5375],
			self.output[len(self.output)-1]
		)

	def test_stats_each_team_present(self):

		self.assertEqual(
			32, len(self.stats), "stats count should match"
		)

	def test_validate_stats(self):

		tracked_stats = common.get_tracked_stats()

		for team in self.stats:
			team_stats = self.stats[team]
		
			for idx,k in enumerate(tracked_stats):
				self.assertTrue(k in team_stats, f"{k} present for {team}")

				self.assertEqual(
					len(team_stats[tracked_stats[idx]]), len(team_stats[tracked_stats[idx-1]]),
					f"unequal lenght stats for {team}"
				)

	def test_specific_stats_match(self):

		team = "Seattle Seahawks"

		verify = {
			"wins": 12, "points": 394, "allowed": 254, "yards": 6012, "yards_allowed": 4274
		}

		team_stats = self.stats[team]

		for s in team_stats:
			self.assertEqual(verify[s], sum(team_stats[s]), f"{s} should match for {team}")

if __name__ == '__main__':
    unittest.main()