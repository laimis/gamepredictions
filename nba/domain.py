import datetime

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
			self.fouls, self.points
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