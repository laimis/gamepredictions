from dateutil.parser import parse

# this represents csv row from basketball reference
class NBAGame:

	def __init__(self, row, counter):
		self.counter = counter

		self.date = parse(row[0])
		self.away = row[1]
		self.away_pts = self.__safe_int__(row[14])
		self.home = row[15]
		self.home_pts = self.__safe_int__(row[28])
		
		if self.home_pts > self.away_pts:
			self.home_win = 1
		else:
			self.home_win = 0

	def __safe_int__(self, val):
		if not val: return 0

		return int(val)