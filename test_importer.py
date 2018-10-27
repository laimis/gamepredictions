import unittest

import importer

class TestImport(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		super(TestImport, cls).setUpClass()

		with open("input\\2014.csv", 'r') as input_f:
			cls.output, _ = importer.transform_input_to_output(2014, input_f, 4)

	def test_total_rows(self):

		self.assertEqual(179, len(self.output))

	def test_first_row_correct(self):

		self.assertEqual(
			[2014, 5, 'Minnesota Vikings', 'Green Bay Packers', 1, 0.5, 0.5, 1.75, -1],
			self.output[0]
		)

	def test_last_row_correct(self):

		self.assertEqual(
			[2014, 16, 'Denver Broncos', 'Cincinnati Bengals', 1, 1.0, 0.75, 8.75, 4.75],
			self.output[len(self.output)-1]
		)

if __name__ == '__main__':
    unittest.main()