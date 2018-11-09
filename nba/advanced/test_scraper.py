import unittest

import scraper

class TestImport(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		super(TestImport, cls).setUpClass()

		cls.links = scraper.get_boxscore_links(2018, 11, 8)
		cls.entries = scraper.get_boxscore_details(cls.links[0])

	def test_total_number_of_links_should_match(self):

		self.assertEqual(4, len(self.links))

	def test_box_score_summary_correct(self):

		self.assertEqual(24, len(self.entries))