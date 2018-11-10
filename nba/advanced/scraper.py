from bs4 import BeautifulSoup
import urllib.request

class BoxScoreTeam:

	def __init__(self, team_name, away):
		self.entries = []
		self.team_name = team_name
		self.away = away

	def add_box_score_entry(self, entry):
		self.entries.append(entry)

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

class BoxScoreEntry:
	def __init__(self, team, name, columns):

		self.team = team
		self.name = name

		if len(columns) == 0:
			return
			
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

def __get_boxscore_soup__(box_score_url):
	with urllib.request.urlopen(f"{ref_url}/{box_score_url}") as response:
		html = response.read()
		return BeautifulSoup(html, 'html.parser')

def __get_boxscore_links_soup__(year, month, day):
	with urllib.request.urlopen(f"{ref_url}/boxscores/?month={month}&day={day}&year={year}") as response:
		html = response.read()
		return BeautifulSoup(html, 'html.parser')

def get_boxscore_links(year, month, day):

	links = []

	soup = __get_boxscore_links_soup__(year, month, day)
		
	for href in [x.get("href") for x in soup.find_all('a') if x.get('href').startswith(f"/boxscores/{year}") ]:
		
		if href not in links:
			links.append(href)

	return links

def get_boxscore_details(year:int, month:int, day:int, box_score_url:str) -> BoxScore:

	def skip_box_score_row(r):
		row_text = r.get_text()
		return "Basic Box" in row_text \
				or "Advanced Box" in row_text \
				or "Starters" in row_text \
				or "Reserves" in row_text \
				or "Team Totals" in row_text

	soup = __get_boxscore_soup__(box_score_url)

	entries = []

	for table in soup.find_all('table'):

		# box score tables start with ids like box_mil_basic, box_mil_advanced, etc
		if "id" not in table.attrs:
			continue

		table_id = table["id"]
		
		if not table_id.startswith("box_"):
			continue
			
		if table_id.endswith("_advanced"):
			continue
			
		team_name = table_id.replace("box_", "").replace("_basic", "")
		
		for r in table.find_all('tr'):

			# skip rows that are separators
			if skip_box_score_row(r):
				continue

			name = r.find("th").find("a").contents[0]
			columns = r.find_all("td")

			entry = BoxScoreEntry(team_name, name, columns)
			
			entries.append(entry)

	return BoxScore(year, month, day, entries)

if __name__ == "__main__":
	pass