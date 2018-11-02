def add_to_stats(stats, rd, tracked_stats):

	def add_to_stats_internal(stats, team, to_add):

		if team not in stats:
			stats[team] = dict([(x,[]) for x in tracked_stats])
			
		for idx,s in enumerate(tracked_stats):
			stats[team][s].append(to_add[idx])

	add_to_stats_internal(stats, rd.home, [rd.homeWin, rd.homePts, rd.awayPts, rd.homeYards, rd.awayYards])
	add_to_stats_internal(stats, rd.away, [1 - rd.homeWin, rd.awayPts, rd.homePts, rd.awayYards, rd.homeYards])

def calc_features(stats, game_info, weeks_to_roll, tracked_stats):

	home_pct, home_pts, home_allowed, home_yards, home_yards_allowed = calc_stats(stats, game_info.home, weeks_to_roll, tracked_stats)
	away_pct, away_pts, away_allowed, away_yards, away_yards_allowed = calc_stats(stats, game_info.away, weeks_to_roll, tracked_stats)

	return [
		away_pct,
		home_pct,
		away_pts - away_allowed,
		home_pts - home_allowed,
		away_yards,
		home_yards,
	]

def calc_stats(stats, team, weeks_to_roll, tracked_stats):
 
	def do_calculation(team_stats, stat, length):
		return sum(team_stats[stat][-weeks_to_roll:]) / len(team_stats[stat][-weeks_to_roll:])

	team_stats = stats[team]

	return tuple([do_calculation(team_stats, x, weeks_to_roll) for x in tracked_stats])