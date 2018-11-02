import unittest

import common
import nfl

import csv

class TestCommon(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		super(TestCommon, cls).setUpClass()

		with open("input\\nfl\\2014.csv", 'r') as input_f:
			rows = csv.reader(input_f)
			lst = list(rows)

			cls.first = nfl.NFLGame(lst[0])
			cls.second = nfl.NFLGame(lst[1])

	def test_parsed_firstrow_matches(self):

		self.assertEqual(1, self.first.week, "week should match")
		self.assertEqual("Seattle Seahawks", self.first.home, "home team should match")
		self.assertEqual("Green Bay Packers", self.first.away, "away team should match")

		self.assertEqual(36, self.first.homePts, "home team pts should match")
		self.assertEqual(16, self.first.awayPts, "away team pts should match")
		
		self.assertEqual(1, self.first.homeWin, "home is a winner")

	def test_parsed_secondrow_matches(self):

		self.assertEqual(1, self.second.week, "week should match")
		self.assertEqual("St. Louis Rams", self.second.home, "home team should match")
		self.assertEqual("Minnesota Vikings", self.second.away, "away team should match")

		self.assertEqual(6, self.second.homePts, "home team pts should match")
		self.assertEqual(34, self.second.awayPts, "away team pts should match")
		
		self.assertEqual(0, self.second.homeWin, "home is a winner")

if __name__ == '__main__':
    unittest.main()