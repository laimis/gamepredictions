import unittest
import datetime

import nba.domain as domain
import nba.scraper as scraper


class TestDomain(unittest.TestCase):

	def test_gameline_index(self):
		
		lines = []

		date = datetime.datetime.now()

		lines.append(scraper.ESPNGameLine(date, "bos", -7))
		lines.append(scraper.ESPNGameLine(date, "gsw", -11))

		index = domain.GameLineIndex(lines)

		line = index.get(date, "atl", "bos")

		self.assertEqual("bos", line.team, "boston was found")
		self.assertEqual(-7, line.spread, "spread  matches")

		line = index.get(date, "atl", "nok")

		self.assertEqual(None, line, "there is no line for such game")