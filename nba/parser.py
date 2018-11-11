from dateutil.parser import parse

# this represents csv row from basketball reference
class NBAGame:

	def __init__(self, row, counter):
		self.counter = counter

		self.date = parse(row[0])
		self.away = row[1]
		self.away_pts = self.__safe_int__(row[14])
		self.away_fgm = self.__safe_int__(row[2])
		self.away_fga = self.__safe_int__(row[3])
		self.away_tpm = self.__safe_int__(row[4])
		self.away_tpa = self.__safe_int__(row[5])
		self.away_ftm = self.__safe_int__(row[6])
		self.away_fta = self.__safe_int__(row[7])
		self.home = row[15]
		self.home_pts = self.__safe_int__(row[28])
		self.home_fgm = self.__safe_int__(row[16])
		self.home_fga = self.__safe_int__(row[17])
		self.home_tpm = self.__safe_int__(row[18])
		self.home_tpa = self.__safe_int__(row[19])
		self.home_ftm = self.__safe_int__(row[20])
		self.home_fta = self.__safe_int__(row[21])
		
		if self.home_pts > self.away_pts:
			self.home_win = 1
		else:
			self.home_win = 0

	def __safe_int__(self, val):
		if not val: return 0

		return int(val)