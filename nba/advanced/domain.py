class Game:
	def __init__(self, date, id, away, home):
		self.id = id
		self.date = date
		self.away = away
		self.away_stats = None
		self.home = home
		self.home_stats = None

class GameStats:
	def __init__(self):
		self.points = 0
		self.fields_goals_made = 0
		self.fields_goals_attempted = 0

		self.threes_made = 0
		self.threes_attempted = 0

		self.free_throws_made = 0
		self.free_throws_attemped = 0

		self.offensive_rebounds = 0
		self.defense_rebounds = 0

		self.assists = 0
		self.steals = 0
		self.blocks = 0
		self.turnovers = 0
		self.fouls = 0
		self.points = 0

		self.players = []

	def add_player_stats(self, name,fields_goals_made,fields_goals_attempted,
					threes_made,threes_attempted,
					free_throws_made,free_throws_attempted,
					offensive_rebounds,defense_rebounds,
					assists, steals, blocks, turnovers, fouls,
					points):

		self.players.append(name)

		self.fields_goals_attempted += fields_goals_attempted
		self.fields_goals_made += fields_goals_made

		self.threes_made += threes_made
		self.threes_attempted += threes_attempted

		self.free_throws_made += free_throws_made
		self.free_throws_attemped += free_throws_attempted

		self.offensive_rebounds += offensive_rebounds
		self.defense_rebounds += defense_rebounds

		self.assists += assists
		self.steals += steals
		self.blocks += blocks
		self.turnovers += turnovers
		self.fouls += fouls
		self.points += points