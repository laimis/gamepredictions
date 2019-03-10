import math

class Strategy:
	def __init__(self):
		self.candidates = 0
		self.matches = 0
		self.winning_picks = 0
		self.name = "undefined"

	def evaluate(self, row):

		self.candidates += 1

		self.__evaluate__(row)

	# override in subclass
	def __evaluate__(row):
		None

	def get_results(self):
		return StrategyResult(self.name, self.candidates, self.matches, self.winning_picks)

class StrategyResult:
	def __init__(self, name, candidates, matches, winning_picks):
		self.name = name
		self.candidates = candidates
		self.matches = matches
		self.winning_picks = winning_picks

	def summary(self, bet_size = 10, bet_position = 114):
		
		single_win = bet_size * 100 / bet_position
		money_wagered = self.matches * bet_size
		
		money_lost = (self.matches - self.winning_picks) * bet_size
		money_won = self.winning_picks * single_win
		profit = round(money_won - money_lost)

		match_pct = round(self.matches / self.candidates * 100, 2)
		winning_pct = round(self.winning_picks / self.matches * 100, 2)
		
		print(f"{self.name} strategy results:")
		print(f"	{self.matches} out of {self.candidates} ({match_pct}%)")
		print(f"	wins: ({self.winning_picks} ({winning_pct}%)")
		print(f"	profit with {bet_size} bets: {profit}")

class LosingStreakStrategy(Strategy):

	def __init__(self, streak, choose_to_cover):
		super(LosingStreakStrategy,self).__init__()
		self.streak = streak
		self.choose_to_cover = choose_to_cover
		self.name = "losing streak {0} choose to cover {1}".format(self.streak, self.choose_to_cover)

	def __evaluate__(self, data):
		
		if data.home_streak <= self.streak:
			self.matches += 1

			if self.choose_to_cover and data.spread_covered:
				self.winning_picks += 1
			elif not self.choose_to_cover and not data.spread_covered:
				self.winning_picks += 1

class DumbStrategyAlwaysCover(Strategy):

	def __init__(self):
		super(DumbStrategyAlwaysCover, self).__init__()
		self.name = "Always pick to cover"

	def __evaluate__(self, data):
		
		self.matches += 1

		if data.spread_covered:
			self.winning_picks += 1

def all_strategies():
	return [
		LosingStreakStrategy(-3, True),
		LosingStreakStrategy(-5, False),
		DumbStrategyAlwaysCover()
	]