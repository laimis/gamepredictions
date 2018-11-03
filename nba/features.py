tracked_stats = ["wins", "scored", "allowed"]
games_to_roll = 10

def add_to_stats(stats, rd):

	def add_to_stats_internal(stats, team, to_add):

		if team not in stats:
			stats[team] = dict([(x,[]) for x in tracked_stats])
			
		for idx,s in enumerate(tracked_stats):
			stats[team][s].append(to_add[idx])

	add_to_stats_internal(stats, rd.home, [rd.home_win, rd.home_pts, rd.away_pts])
	add_to_stats_internal(stats, rd.away, [1 - rd.home_win, rd.away_pts, rd.home_pts])

def calc_features(stats, game_info):

	home_pct, home_pts, home_allowed = calc_stats(stats, game_info.home)
	away_pct, away_pts, away_allowed = calc_stats(stats, game_info.away)

	return [
		away_pct,
		home_pct,
		away_pts - away_allowed,
		home_pts - home_allowed
	]

def calc_stats(stats, team):
 
	def do_calculation(team_stats, stat):
		return sum(team_stats[stat][-games_to_roll:]) / len(team_stats[stat][-games_to_roll:])

	team_stats = stats[team]

	return tuple([do_calculation(team_stats, x) for x in tracked_stats])