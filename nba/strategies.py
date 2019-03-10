import math

class Strategy:
	def __init__(self):
		self.candidates = 0
		self.matches = 0
		self.winning_picks = 0

	def summary(self):
		bet_size = 10
		bet_position = 114

		money_wagered = self.matches * bet_size

		money_lost = (self.matches - self.winning_picks) * bet_size
		
		single_win = bet_size * 100 / bet_position

		money_won = self.winning_picks * single_win

		profit = round(money_won - money_lost)

		match_pct = round(self.matches / self.candidates * 100, 2)
		print(self.matches, " out of ", self.candidates, match_pct, "%")

		winning_pct = round(self.winning_picks / self.matches * 100, 2)
		print("wins: ", self.winning_picks, winning_pct, "%")

		print("profit with",bet_size,"bet:",profit)

class LosingStreakStrategy(Strategy):

	def __init__(self, streak, choose_to_cover):
		super(LosingStreakStrategy,self).__init__()
		self.streak = streak
		self.choose_to_cover = choose_to_cover

	def evaluate(self, data):
		
		self.candidates += 1
		
		if data.home_streak <= self.streak or data.away_streak <= self.streak:
			self.matches += 1

			if self.choose_to_cover and data.spread_covered:
				self.winning_picks += 1
			elif not self.choose_to_cover and not data.spread_covered:
				self.winning_picks += 1

	def summary(self):
		print("losing streak ",self.streak,"choose to cover", self.choose_to_cover,"strategy results:")
		super().summary()