from dateutil.parser import parse

# this represents csv row from basketball reference
class NBAGame:
	def __init__(self, counter, row=None, date = None):
		self.counter = counter

		if date is not None:
			self.date = date

		self.home_win = -1

		if row is None:
			return

		self.date = parse(row[0])
		self.away = row[1]
		self.away_pts = self.__safe_int__(row[15])
		self.away_fgm = self.__safe_int__(row[2])
		self.away_fga = self.__safe_int__(row[3])
		self.away_tpm = self.__safe_int__(row[4])
		self.away_tpa = self.__safe_int__(row[5])
		self.away_ftm = self.__safe_int__(row[6])
		self.away_fta = self.__safe_int__(row[7])
		self.away_oreb = self.__safe_int__(row[8])
		self.away_dreb = self.__safe_int__(row[9])
		self.away_assists = self.__safe_int__(row[10])
		self.away_turnovers = self.__safe_int__(row[13])
		
		self.home = row[16]
		self.home_pts = self.__safe_int__(row[30])
		self.home_fgm = self.__safe_int__(row[17])
		self.home_fga = self.__safe_int__(row[18])
		self.home_tpm = self.__safe_int__(row[19])
		self.home_tpa = self.__safe_int__(row[20])
		self.home_ftm = self.__safe_int__(row[21])
		self.home_fta = self.__safe_int__(row[22])
		self.home_oreb = self.__safe_int__(row[23])
		self.home_dreb = self.__safe_int__(row[24])
		self.home_assists = self.__safe_int__(row[25])
		self.home_turnovers = self.__safe_int__(row[26])
		
		if self.home_pts > self.away_pts:
			self.home_win = 1
		else:
			self.home_win = 0

	def __safe_int__(self, val):
		if not val: return 0

		return int(val)