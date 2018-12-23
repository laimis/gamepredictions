from bs4 import BeautifulSoup
import urllib.request
import calendar
import json
import datetime

from typing import List


class ESPNGameLine:
	def __init__(self, date:datetime.date, team:str, spread:float):

		corrected = self.__get_correct_name__(team)

		self.date = date
		self.team = corrected
		self.spread = spread
	
	def __get_correct_name__(self, name:str) -> str:
		if name == "gs":
			return "gsw"
		if name == "wsh":
			return "was"
		if name == "ny":
			return "nyk"
		if name == "no":
			return "nop"
		if name == "utah":
			return "uta"
		if name == "bkn":
			return "brk"
		if name == "cha":
			return "cho"
		if name == "phx":
			return "pho"
		if name == "sa":
			return "sas"
		
		return name

class BoxScoreTeam:
	def __init__(self, team_name, away):
		self.entries = []
		self.team_name = team_name
		self.away = away

	def add_box_score_entry(self, entry):
		self.entries.append(entry)

	def __str__(self):
		return self.team_name


class BoxScore:
	def __init__(self, year, month, day, entries):

		self.year = year
		self.month = month
		self.day = day

		self.away = None
		self.home = None

		current = None

		for e in entries:
			if self.away == None:
				self.away = BoxScoreTeam(e.team, True)
				current = self.away

			if self.away.team_name != e.team and self.home == None:
				self.home = BoxScoreTeam(e.team, False)
				current = self.home

			current.add_box_score_entry(e)

	def __str__(self):
		return f"{self.year}-{self.month}-{self.day}, {self.away} @ {self.home}"


class BoxScoreEntry:
	def __init__(self, team, name, columns):

		self.team = team
		self.name = name

		if len(columns) == 0:
			return

			# player did not play
		if len(columns) == 1 or len(columns[0].contents) == 0:
			self.minutes = ""
			self.field_goals_made = 0
			self.field_goals_attemped = 0
			self.threes_made = 0
			self.threes_attempted = 0
			self.free_throws_made = 0
			self.free_throws_attempted = 0
			self.offensive_rebounds = 0
			self.defensive_rebounds = 0
			self.assists = 0
			self.steals = 0
			self.blocks = 0
			self.turnovers = 0
			self.personal_fouls = 0
			self.points = 0
		else:
			self.minutes = columns[0].contents[0]

			self.field_goals_made = columns[1].contents[0]
			self.field_goals_attemped = columns[2].contents[0]

			self.threes_made = columns[4].contents[0]
			self.threes_attempted = columns[5].contents[0]

			self.free_throws_made = columns[7].contents[0]
			self.free_throws_attempted = columns[8].contents[0]

			self.offensive_rebounds = columns[10].contents[0]
			self.defensive_rebounds = columns[11].contents[0]

			self.assists = columns[13].contents[0]
			self.steals = columns[14].contents[0]
			self.blocks = columns[15].contents[0]
			self.turnovers = columns[16].contents[0]
			self.personal_fouls = columns[17].contents[0]
			self.points = columns[18].contents[0]


ref_url = "https://www.basketball-reference.com"

def __get_soup__(url):

	headers = headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
	}

	req = urllib.request.Request(f"{url}", headers=headers)
	with urllib.request.urlopen(req) as response:
		html = response.read()
		return BeautifulSoup(html, "html.parser")

def __get_boxscore_soup__(box_score_url):
	return __get_soup__(f"{ref_url}/{box_score_url}")

def __get_boxscore_links_soup__(year, month, day, attempt=0):

	try:
		return __get_soup__(f"{ref_url}/boxscores/?month={month}&day={day}&year={year}")
	except urllib.error.HTTPError as e:

		if attempt < 2:
			return __get_boxscore_links_soup__(year, month, day, attempt + 1)
		else:
			print("exception!", e)
			exit(-1)


def get_boxscore_links(year, month, day) -> List[str]:

	links: List[str] = []

	soup = __get_boxscore_links_soup__(year, month, day)

	for href in [
		x.get("href")
		for x in soup.find_all("a")
		if x.get("href").startswith(f"/boxscores/{year}")
	]:

		if href not in links:
			links.append(href)

	return links


def get_boxscore_details(
	year: int, month: int, day: int, box_score_url: str
) -> BoxScore:
	def skip_box_score_row(r):
		row_text = r.get_text()
		return (
			"Basic Box" in row_text
			or "Advanced Box" in row_text
			or "Starters" in row_text
			or "Reserves" in row_text
			or "Team Totals" in row_text
		)

	soup = __get_boxscore_soup__(box_score_url)

	entries = []

	for table in soup.find_all("table"):

		# box score tables start with ids like box_mil_basic, box_mil_advanced, etc
		if "id" not in table.attrs:
			continue

		table_id = table["id"]

		if not table_id.startswith("box_"):
			continue

		if table_id.endswith("_advanced"):
			continue

		team_name = table_id.replace("box_", "").replace("_basic", "")

		for r in table.find_all("tr"):

			# skip rows that are separators
			if skip_box_score_row(r):
				continue

			name = r.find("th").find("a").contents[0]
			columns = r.find_all("td")

			entry = BoxScoreEntry(team_name, name, columns)

			entries.append(entry)

	return BoxScore(year, month, day, entries)


def get_games(dt):

	month = calendar.month_name[dt.month].lower()
	match = f"month={dt.month}&day={dt.day}&year={dt.year}"
	url = f"{ref_url}/leagues/NBA_{dt.year+1}_games-{month}.html"

	games = []

	with urllib.request.urlopen(url) as response:
		html = response.read()
		soup = BeautifulSoup(html, "html.parser")

		for table in soup.find_all("table"):
			if "id" not in table.attrs:
				continue

			if table["id"] != "schedule":
				continue

			skipped = False
			for tr in table.find_all("tr"):
				if not skipped:
					skipped = True
					continue

				href = tr.find_all("th")[0].find_all("a")[0]["href"]

				if match not in href:
					continue

				tds = tr.find_all("td")

				away = tds[1].find_all("a")[0].get_text()
				away_short = tds[1].find_all("a")[0]["href"].split("/")[2].lower()
				home = tds[3].find_all("a")[0].get_text()
				home_short = tds[3].find_all("a")[0]["href"].split("/")[2].lower()

				games.append((away_short, home_short))

	return games

def __get_gamecast_urls__(dt):
	scoreboard_url = f"http://www.espn.com/nba/scoreboard/_/date/{dt.year}{dt.month:02}{dt.day:02}"

	soup = __get_soup__(scoreboard_url)

	js = ""
	for s in soup.find_all("script"):
		txt = s.get_text()

		if "window.espn.scoreboardData" not in txt:
			continue

		end = txt.index(";window.espn.scoreboardSettings")
		start = txt.index("= {")

		js = txt[start + 2 : end]

		break

	loaded = json.loads(js)

	links = []
	for e in loaded["events"]:
		name = e["shortName"]
		url = ""
		for l in e["links"]:
			if l["shortText"] == "Gamecast":
				url = l["href"]
				break
		links.append((name,url))

	return links

def __get_gameday_lines__():
	scoreboard_url = f"http://www.espn.com/nba/scoreboard"

	soup = __get_soup__(scoreboard_url)

	js = ""
	for s in soup.find_all("script"):
		txt = s.get_text()

		if "window.espn.scoreboardData" not in txt:
			continue

		end = txt.index(";window.espn.scoreboardSettings")
		start = txt.index("= {")

		js = txt[start + 2 : end]

		break

	loaded = json.loads(js)

	lines = []
	for e in loaded["events"]:
		for c in e["competitions"]:
			for o in c["odds"]:
				lines.append(o["details"])

	return lines

def __get_line_info__(date:datetime.date, gamecast_url:str) -> ESPNGameLine:
	soup = __get_soup__(gamecast_url)

	mydivs = soup.findAll("div", {"class": "odds-details"})

	if len(mydivs) == 0:
		return ESPNGameLine(date, "notfound", 0)

	arr = mydivs[0].findAll("li")[0].get_text().replace("Line: ", "").split(" ")

	try:
		team = arr[0].lower()

		if "even" in team:
			spread = 0.0
		else:
			spread = float(arr[1])

		return ESPNGameLine(date, team, spread)
	except IndexError as err:
		print("failed to parse", mydivs[0].get_text(), "for url", gamecast_url,"team",team)
		exit(-1)

def get_lines(date) -> List[ESPNGameLine]:

	lines:List[ESPNGameLine] = []

	for pair in __get_gamecast_urls__(date):

		name = pair[0].lower()
		url = pair[1]

		print(name,url)

		line = __get_line_info__(date, url)

		if line.team == "even":
			line = ESPNGameLine(date, name.split(" @ ")[0],line.spread)

		lines.append(line)
	
	return lines
	
def get_gameday_lines() -> List[ESPNGameLine]:

	lines:List[ESPNGameLine] = []

	for line in __get_gameday_lines__():

		name = line.split(' ')[0].lower()
		spread = float(line.split(' ')[1])

		game_line = ESPNGameLine(datetime.datetime.now().date(), name, spread)

		lines.append(game_line)
	
	return lines

if __name__ == "__main__":
	pass

