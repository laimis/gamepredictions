import datetime
from dateutil.parser import parse

class GameStats:
	def __init__(self, stat_dict):

		self.fields_goals_made = stat_dict["fgm"]
		self.fields_goals_attempted = stat_dict["fga"]
		
		self.threes_made = stat_dict["tpm"]
		self.threes_attempted = stat_dict["tpa"]

		self.free_throws_made = stat_dict["ftm"]
		self.free_throws_attemped = stat_dict["fta"]

		self.offensive_rebounds = stat_dict["oreb"]
		self.defense_rebounds = stat_dict["dreb"]

		self.assists = stat_dict["assists"]
		self.steals = stat_dict["steals"]
		self.blocks = stat_dict["blocks"]
		self.turnovers = stat_dict["turnovers"]
		self.fouls = stat_dict["fouls"]
		self.points = stat_dict["points"]

	def to_array(self):
		return [
			self.fields_goals_made, self.fields_goals_attempted,
			self.threes_made, self.threes_attempted,
			self.free_throws_made, self.free_throws_attemped,
			self.offensive_rebounds, self.defense_rebounds,
			self.assists, self.steals, self.blocks,
			self.turnovers, self.fouls, self.points
		]

class Game:
	def __init__(self, date:datetime.date, id:str, away:str, home:str, away_stats:GameStats, home_stats:GameStats):
		self.id = id
		self.date = date
		self.away = away
		self.away_stats = away_stats
		self.home = home
		self.home_stats = home_stats

	def to_output(self):
		return [self.date,self.away] + self.away_stats.to_array() + [self.home] + self.home_stats.to_array()

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

		winner = self.away
		covered = self.home_pts - self.away_pts

		if self.home_pts > self.away_pts:
			self.home_win = 1
			winner = self.home
			covered = self.away_pts - self.home_pts
		else:
			self.home_win = 0

		self.line_team = row[31]
		self.line_spread = self.__safe_float__(row[32])
		
		if self.line_team == winner:
			self.spread_correct = True
		else:
			self.spread_correct = False

		self.spread_covered = covered < self.line_spread
		
	def __safe_int__(self, val):
		if not val: return 0

		return int(val)

	def __safe_float__(self, val):
		if not val: return 0

		return float(val)

class GamePrediction:
	def __init__(self, game:NBAGame, prediction:int, confidence):
		self.confidence = max(confidence)
		
		if prediction == 0:
			self.winner = game.away
		else:
			self.winner = game.home

class GameLineIndex:
	def __init__(self, lines):

		self.__map__ = {}

		for l in lines:
			key = self.__get_key__(l.date, l.team)
			value = l

			self.__map__[key] = value

	def __get_key__(self, date:datetime.date, team:str):
		return str(date) + str(team)

	def get(self, date:datetime.date, team1:str, team2:str):

		for t in [team1, team2]:
			key = self.__get_key__(date, t)

			if key in self.__map__:
				return self.__map__[key]

		return None

		