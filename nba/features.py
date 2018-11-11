import nba.parser as parser

tracked_stats = ["wins", "scored", "allowed", "date", "ftm", "tpm"]
games_to_roll = 10

def to_stats_home(rd:parser.NBAGame):
	return [rd.home_win, rd.home_pts, rd.away_pts, rd.date, rd.home_fgm/rd.home_fga, rd.home_tpm/rd.home_tpa]

def to_stats_away(rd:parser.NBAGame):
	return [1 - rd.home_win, rd.away_pts, rd.home_pts, rd.date, rd.away_fgm/rd.away_fga, rd.away_tpm/rd.home_tpa]

def add_to_stats(stats, rd):

	def add_to_stats_internal(stats, team, to_add):

		if team not in stats:
			stats[team] = dict([(x,[]) for x in tracked_stats])
			
		for idx,s in enumerate(tracked_stats):
			stats[team][s].append(to_add[idx])

	add_to_stats_internal(stats, rd.home, to_stats_home(rd))
	add_to_stats_internal(stats, rd.away, to_stats_away(rd))

def get_feature_headers():
	return "year,date,counter,away,home,home_win,away_pct,home_pct,away_diff,home_diff,away_tpm,home_tpm\n"

def calc_features(stats, game_info):

	home_pct, home_pts, home_allowed, home_games, home_ftm, home_tpm = calc_stats(stats, game_info.home, game_info.date)
	away_pct, away_pts, away_allowed, away_games, away_ftm, away_tpm = calc_stats(stats, game_info.away, game_info.date)

	return [
		away_pct,
		home_pct,
		away_pts - away_allowed,
		home_pts - home_allowed,
		away_tpm,
		home_tpm
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