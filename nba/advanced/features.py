from typing import Dict

import domain

tracked_stats = ["wins", "scored", "allowed", "fgm", "fga", "tpm", "tpa", "ftm", "fta", "rebs", "assists", "steals", "blocks", "turnovers","fouls"]

games_to_roll = 10

def add_to_stats(stats:Dict, g:domain.Game):

	def add_to_stats_internal(stats:Dict, team:str, team_stats:domain.GameStats, opp_stats:domain.GameStats, is_win:int):

		if team not in stats:
			stats[team] = dict([(x,[]) for x in tracked_stats])
			
		stats[team]["wins"].append(is_win)
		stats[team]["scored"].append(team_stats.points)
		stats[team]["allowed"].append(opp_stats.points)
		stats[team]["fgm"].append(team_stats.fields_goals_made)
		stats[team]["fga"].append(team_stats.fields_goals_attempted)
		stats[team]["tpm"].append(team_stats.threes_made)
		stats[team]["tpa"].append(team_stats.threes_attempted)
		stats[team]["ftm"].append(team_stats.free_throws_made)
		stats[team]["fta"].append(team_stats.free_throws_attemped)
		stats[team]["rebs"].append(team_stats.offensive_rebounds+team_stats.defense_rebounds)
		stats[team]["assists"].append(team_stats.assists)
		stats[team]["steals"].append(team_stats.steals)
		stats[team]["blocks"].append(team_stats.blocks)
		stats[team]["turnovers"].append(team_stats.turnovers)
		stats[team]["fouls"].append(team_stats.fouls)

	home_win = 1
	if g.away_stats.points > g.home_stats.points:
		home_win = 0

	add_to_stats_internal(stats, g.home, g.home_stats, g.away_stats, home_win)
	add_to_stats_internal(stats, g.away, g.away_stats, g.home_stats, 1 - home_win)

def get_feature_headers():
	return "year,date,counter,away,home,home_win,away_pct,home_pct,away_diff,home_diff\n"

def calc_features(stats, game_info):

	home_pct, home_pts, home_allowed, home_games = calc_stats(stats, game_info.home, game_info.date)
	away_pct, away_pts, away_allowed, away_games = calc_stats(stats, game_info.away, game_info.date)

	return [
		away_pct,
		home_pct,
		away_pts - away_allowed,
		home_pts - home_allowed,
		# away_games,
		# home_games
	]

def number_of_games_within_date(dates, date, number_of_days):
	number_of_games = 0
	# print(dates)
	for d in dates[-5:]:
		if (date - d).days <= number_of_days:
			number_of_games += 1
	return number_of_games

def calc_stats(stats, team, date):
 
	def do_calculation(team_stats, stat):
		if stat == "date":
			return number_of_games_within_date(team_stats[stat], date, 1)

		return sum(team_stats[stat][-games_to_roll:]) / len(team_stats[stat][-games_to_roll:])

	team_stats = stats[team]

	return tuple([do_calculation(team_stats, x) for x in tracked_stats])