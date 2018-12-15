-- DROP SEQUENCE games_id CASCADE;
CREATE SEQUENCE games_id;
ALTER TABLE games_id OWNER TO bet;

-- DROP TABLE games;
CREATE TABLE games (id text DEFAULT(nextval('games_id')) PRIMARY KEY, date timestamp, away text, home text);
ALTER TABLE games owner TO bet;

CREATE UNIQUE INDEX games_date_away_home_idx ON games USING btree(date, away, home);

-- DROP SEQUENCE gamerows_id CASCADE;
CREATE SEQUENCE gamerows_id;
ALTER TABLE gamerows_id OWNER TO bet;

-- DROP TABLE gamerows;
CREATE TABLE gamerows(
	id text DEFAULT(nextval('gamerows_id')) PRIMARY KEY, 
	gameid TEXT, team text, name text, 
	minutes text, fgm int, fga int, tpm int, tpa int, ftm int, fta int, oreb int, dreb int, assists int, steals int, blocks int, turnovers int, fouls int, points int);
ALTER TABLE gamerows owner TO bet;

-- DROP SEQUENCE gamelines_id CASCADE;
CREATE SEQUENCE gamelines_id;
ALTER TABLE gamelines_id OWNER TO bet;

-- DROP TABLE gamelines;
CREATE TABLE gamelines(
	id text DEFAULT(nextval('gamelines_id')) PRIMARY KEY, date TIMESTAMP, team text, value text);
ALTER TABLE gamelines owner TO bet;

CREATE UNIQUE INDEX gamelines_unique ON gamelines USING BTREE(date, team);