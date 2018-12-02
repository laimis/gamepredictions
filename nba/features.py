import nba.domain as domain

from typing import List

tracked_stats = ["wins", "scored", "allowed", "date", "fg%", "tp%", "ft%", "rebs", "assists", "turnovers", "streak"]
GAMES_TO_ROLL = 20
STREAK_NUMBER = 3

def get_label_column_names():
	return ["year", "date", "counter", "away", "home", "home_win"]

def get_feature_column_names() -> List[str]:
	return ["away_pct", "home_pct", "away_diff", "home_diff"]

def get_feature_column_names_for_data_files():
	return ["away_pct", "home_pct", "away_diff", "home_diff", "away_tpm", "home_tpm", "away_todiff", "home_todiff", "away_rebs", "home_rebs", "away_streak", "home_streak"]

def get_data_header():
	combined = get_label_column_names() + get_feature_column_names_for_data_files()
	return ",".join(combined)

def to_stats_home(rd:domain.NBAGame):
	return [
		rd.home_win,
		rd.home_pts,
		rd.away_pts,
		rd.date, 
		rd.home_fgm/rd.home_fga,
		rd.home_tpm/rd.home_tpa,
		rd.home_ftm/rd.home_fta,
		rd.home_oreb + rd.home_dreb,
		rd.home_assists,
		rd.home_turnovers,
		rd.home_win,
	]

def to_stats_away(rd:domain.NBAGame):
	return [
		1 - rd.home_win,
		rd.away_pts,
		rd.home_pts,
		rd.date,
		rd.away_fgm/rd.away_fga,
		rd.away_tpm/rd.home_tpa,
		rd.away_ftm/rd.away_ftm,
		rd.away_oreb + rd.away_dreb,
		rd.away_assists,
		rd.away_turnovers,
		1 - rd.home_win,
	]

def add_to_stats(stats, rd):

	def add_to_stats_internal(stats, team, to_add):

		if team not in stats:
			stats[team] = dict([(x,[]) for x in tracked_stats])
			
		for idx,s in enumerate(tracked_stats):
			stats[team][s].append(to_add[idx])

	add_to_stats_internal(stats, rd.home, to_stats_home(rd))
	add_to_stats_internal(stats, rd.away, to_stats_away(rd))

def calc_features(stats, game_info):

	home_pct, home_pts, home_allowed, home_games, home_fg, home_tp, home_ft, home_rebs, home_assists, home_turnovers, home_streak = __calc_features__(stats, game_info.home, game_info.date)
	away_pct, away_pts, away_allowed, away_games, away_fg, away_tp, away_ft, away_rebs, away_assists, away_turnovers, away_streak = __calc_features__(stats, game_info.away, game_info.date)

	return [
		away_pct,
		home_pct,
		away_pts - away_allowed,
		home_pts - home_allowed,
		away_tp,
		home_tp,
		away_assists - away_turnovers,
		home_assists - home_turnovers,
		away_rebs,
		home_rebs,
		away_streak,
		home_streak
	]

def number_of_games_within_date(dates, date, number_of_days):
	number_of_games = 0
	# print(dates)
	for d in dates[-5:]:
		if (date - d).days <= number_of_days:
			number_of_games += 1
	return number_of_games

def __calc_features__(stats, team, date):
 
	def do_calculation(team_stats, stat):
		if stat == "date":
			return number_of_games_within_date(team_stats[stat], date, 1)

		if stat == "streak":
			streak_sum = sum(team_stats[stat][-STREAK_NUMBER:])

			if streak_sum == STREAK_NUMBER:
				return 1
			elif streak_sum == 0:
				return -1
			else:
				return 0

		return sum(team_stats[stat][-GAMES_TO_ROLL:]) / len(team_stats[stat][-GAMES_TO_ROLL:])

	team_stats = stats[team]

	return tuple([do_calculation(team_stats, x) for x in tracked_stats])