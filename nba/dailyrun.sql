 DROP TABLE gamestats;
 CREATE TABLE gamestats (
	gameid text, date timestamp, away text, home text, 
	away_points int, away_fgm int, away_fga int, away_tpm int, away_tpa int, away_ftm int, away_fta int, away_oreb int, away_dreb int, away_assists int, away_steals int, away_blocks int, away_turnovers int, away_fouls int,
	home_points int, home_fgm int, home_fga int, home_tpm int, home_tpa int, home_ftm int, home_fta int, home_oreb int, home_dreb int, home_assists int, home_steals int, home_blocks int, home_turnovers int, home_fouls int
);
 ALTER TABLE gamestats OWNER TO bet;
 INSERT INTO gamestats (gameid, date, away, home)
SELECT id, date, away, home FROM games;
 UPDATE gamestats SET (away_points, away_fgm, away_fga) = (SELECT sum(points), sum(fgm), sum(fga) FROM gamerows WHERE gameid = gamestats.gameid and team = gamestats.away);
UPDATE gamestats SET (home_points, home_fgm, home_fga) = (SELECT sum(points), sum(fgm), sum(fga) FROM gamerows WHERE gameid = gamestats.gameid and team = gamestats.home);
 UPDATE gamestats SET (away_tpm, away_tpa) = (SELECT sum(tpm), sum(tpa) FROM gamerows WHERE gameid = gamestats.gameid and team = gamestats.away);
UPDATE gamestats SET (home_tpm, home_tpa) = (SELECT sum(tpm), sum(tpa) FROM gamerows WHERE gameid = gamestats.gameid and team = gamestats.home);
 UPDATE gamestats SET (away_ftm, away_fta) = (SELECT sum(ftm), sum(fta) FROM gamerows WHERE gameid = gamestats.gameid and team = gamestats.away);
UPDATE gamestats SET (home_ftm, home_fta) = (SELECT sum(ftm), sum(fta) FROM gamerows WHERE gameid = gamestats.gameid and team = gamestats.home);
 UPDATE gamestats SET (away_oreb, away_dreb) = (SELECT sum(oreb), sum(dreb) FROM gamerows WHERE gameid = gamestats.gameid and team = gamestats.away);
UPDATE gamestats SET (home_oreb, home_dreb) = (SELECT sum(oreb), sum(dreb) FROM gamerows WHERE gameid = gamestats.gameid and team = gamestats.home);
 UPDATE gamestats SET (away_assists, away_steals, away_blocks) = (SELECT sum(assists), sum(steals), sum(blocks) FROM gamerows WHERE gameid = gamestats.gameid and team = gamestats.away);
UPDATE gamestats SET (home_assists, home_steals, home_blocks) = (SELECT sum(assists), sum(steals), sum(blocks) FROM gamerows WHERE gameid = gamestats.gameid and team = gamestats.home);
 UPDATE gamestats SET (away_turnovers, away_fouls) = (SELECT sum(turnovers), sum(fouls) FROM gamerows WHERE gameid = gamestats.gameid and team = gamestats.away);
UPDATE gamestats SET (home_turnovers, home_fouls) = (SELECT sum(turnovers), sum(fouls) FROM gamerows WHERE gameid = gamestats.gameid and team = gamestats.home); 