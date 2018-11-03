from dateutil.parser import parse

# this represents csv row from basketball reference
class NBAGame:
	def __init__(self, row, counter):
		self.counter = counter
		
		dt = parse(row[0])

		self.date = dt # dt.strftime("%Y-%m-%d")
		self.away = row[2]
		self.away_pts = int(row[3])
		self.home = row[4]
		self.home_pts = int(row[5])
		
		if self.home_pts > self.away_pts:
			self.home_win = 1
		else:
			self.home_win = 0