# this represents csv row from pro football reference
class NFLGame:
	def __init__(self, row):
		self.week = int(row[0])
		winner = row[4]
		losser = row[6]
		winnerPts = int(row[8])
		losserPts = int(row[9])
		winnerYards = int(row[10])
		losserYards = int(row[12])

		isHomeWinner = row[5] != "@"

		self.away = winner
		self.awayPts = winnerPts
		self.awayYards = winnerYards
		self.home = losser
		self.homePts = losserPts
		self.homeYards = losserYards
		self.homeWin = 0

		if isHomeWinner:
			self.away = losser
			self.awayPts = losserPts
			self.awayYards = losserYards
			self.home = winner
			self.homePts = winnerPts
			self.homeYards = winnerYards
			self.homeWin = 1

