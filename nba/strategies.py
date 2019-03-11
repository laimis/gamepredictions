import math

class StrategyResult:
	def __init__(self, name, candidates, matches, covered, not_covered):
		self.name = name
		self.candidates = candidates
		self.matches = matches
		self.covered = covered
		self.not_covered = not_covered

		self.match_pct = round(self.matches / self.candidates * 100, 2)
		self.cover_pct = round(self.covered / self.matches * 100, 2)
		self.not_cover_pct = round(self.not_covered / self.matches * 100, 2)

	def profits(self, bet_size = 10, bet_position = 114):
		
		single_win = bet_size * 100 / bet_position
		money_wagered = self.matches * bet_size
		
		money_lost = (self.matches - self.covered) * bet_size
		money_won = self.covered * single_win
		cover_profit = round(money_won - money_lost)

		money_lost = (self.matches - self.not_covered) * bet_size
		money_won = self.not_covered * single_win
		not_cover_profit = round(money_won - money_lost)
		return (cover_profit, not_cover_profit)

class Strategy:
	def __init__(self):
		self.candidates = 0
		self.matches = 0
		self.covered = 0
		self.not_covered = 0
		self.name = "undefined"

	def evaluate(self, row):

		self.candidates += 1

		self.__evaluate__(row)

	def matched(self, data):
		self.matches += 1

		if data.spread_covered:
			self.covered += 1
		
		if not data.spread_covered:
			self.not_covered += 1

	# override in subclass
	def __evaluate__(row):
		None

	def get_results(self) -> StrategyResult:
		return StrategyResult(self.name, self.candidates, self.matches, self.covered, self.not_covered)

class HomeLosingStreakStrategy(Strategy):

	def __init__(self, streak):
		super(HomeLosingStreakStrategy,self).__init__()
		self.streak = streak
		self.name = f"home losing streak {self.streak}"

	def __evaluate__(self, data):
		
		if data.home_streak <= self.streak and data.home == data.line_team:
			self.matched(data)

class HomeTeamAfterStreak(Strategy):

	def __init__(self, streak):
		super(HomeTeamAfterStreak,self).__init__()
		self.name = f"home team after {streak} win streak"
		self.streak = streak

	def __evaluate__(self, data):
		
		if data.home_streak < self.streak:
			return

		if data.home_pct >= 0.6:
			self.matched(data)

class DumbStrategyAlwaysCover(Strategy):

	def __init__(self):
		super(DumbStrategyAlwaysCover, self).__init__()
		self.name = "Always pick to cover"

	def __evaluate__(self, data):
		
		self.matched(data)

class SpecificTeam(Strategy):

	def __init__(self, team):
		super(SpecificTeam, self).__init__()
		self.name = f"Team {team}"
		self.team = team

	def __evaluate__(self, data):
		
		if data.line_team == self.team:
			self.matched(data)

def all_strategies():
	return [
		DumbStrategyAlwaysCover(),
		HomeLosingStreakStrategy(-3),
		HomeLosingStreakStrategy(-4),
		HomeLosingStreakStrategy(-5),
		HomeLosingStreakStrategy(-6),
		HomeTeamAfterStreak(2),
		HomeTeamAfterStreak(3)
	]