import unittest

import importer

class TestImport(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		super(TestImport, cls).setUpClass()

		with open("input\\2014.csv", 'r') as input_f:
			cls.output = importer.transform_input_to_output(input_f, 4)

	def test_total_rows(self):

		self.assertEqual(194, len(self.output))

	def test_first_row_correct(self):

		self.assertEqual(
			['Minnesota Vikings', 'Green Bay Packers', 0.5, 0.5, 22.75, 23.0, 1],
			self.output[0]
		)

	def test_last_row_correct(self):

		self.assertEqual(
			['Cincinnati Bengals', 'Pittsburgh Steelers', 0.75, 0.75, 25.5, 30.25, 1],
			self.output[len(self.output)-1]
		)

if __name__ == '__main__':
    unittest.main()