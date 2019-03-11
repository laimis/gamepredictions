import math

class StrategyResult:
	def __init__(self, name, candidates, matches, winning_picks):
		self.name = name
		self.candidates = candidates
		self.matches = matches
		self.winning_picks = winning_picks

		self.match_pct = round(self.matches / self.candidates * 100, 2)
		self.winning_pct = round(self.winning_picks / self.matches * 100, 2)

	def profits(self, bet_size = 10, bet_position = 114):
		
		single_win = bet_size * 100 / bet_position
		money_wagered = self.matches * bet_size
		
		money_lost = (self.matches - self.winning_picks) * bet_size
		money_won = self.winning_picks * single_win
		profit = round(money_won - money_lost)

		return profit

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

	def get_results(self) -> StrategyResult:
		return StrategyResult(self.name, self.candidates, self.matches, self.winning_picks)

class LosingStreakStrategy(Strategy):

	def __init__(self, streak, choose_to_cover):
		super(LosingStreakStrategy,self).__init__()
		self.streak = streak
		self.choose_to_cover = choose_to_cover
		self.name = "home losing streak {0} choose to cover {1}".format(self.streak, self.choose_to_cover)

	def __evaluate__(self, data):
		
		if data.home_streak <= self.streak:
			self.matches += 1

			if self.choose_to_cover and data.spread_covered:
				self.winning_picks += 1
			elif not self.choose_to_cover and not data.spread_covered:
				self.winning_picks += 1

class HomeTeamAfterStreak(Strategy):

	def __init__(self, streak, choose_to_cover):
		super(HomeTeamAfterStreak,self).__init__()
		self.name = "good team after one win"
		self.choose_to_cover = choose_to_cover
		self.streak = streak

	def __evaluate__(self, data):
		
		if data.home_streak < self.streak:
			return

		if data.home_pct >= 0.6:
			self.matches += 1

			if self.choose_to_cover and data.spread_covered:
				self.winning_picks += 1
			
			if not self.choose_to_cover and not data.spread_covered:
				self.winning_picks += 1

class DumbStrategyAlwaysCover(Strategy):

	def __init__(self):
		super(DumbStrategyAlwaysCover, self).__init__()
		self.name = "Always pick to cover"

	def __evaluate__(self, data):
		
		self.matches += 1

		if data.spread_covered:
			self.winning_picks += 1

class SpecificTeam(Strategy):

	def __init__(self, team):
		super(SpecificTeam, self).__init__()
		self.name = f"Team {team}"
		self.team = team

	def __evaluate__(self, data):
		
		if data.line_team == self.team:
			self.matches += 1

			if data.spread_covered:
				self.winning_picks += 1

def all_strategies():
	return [
		LosingStreakStrategy(-3, True),
		LosingStreakStrategy(-4, True),
		LosingStreakStrategy(-5, True),
		LosingStreakStrategy(-6, True),
		LosingStreakStrategy(-3, False),
		LosingStreakStrategy(-4, False),
		LosingStreakStrategy(-5, False),
		LosingStreakStrategy(-6, False),
		DumbStrategyAlwaysCover(),
		HomeTeamAfterStreak(2, True),
		HomeTeamAfterStreak(3, True),
		SpecificTeam('gsw'),
		SpecificTeam('hou'),
		SpecificTeam('nyk'),
		SpecificTeam('lal')
	]