from fuzzywuzzy import fuzz
import requests
from re import sub

allTeams = []
bad_words = ['robotics', 'robots','bots','robotic','bot','robot']
PARAMS = {'Content-Type':'application/json',
            'X-TOA-Key':'',
            'X-Application-Origin':'Instagram To Team Accts'}

debug = True

def _get_number_and_name(name):
    return sub('[^0-9]','', name), sub('[^a-z]','',name) #Returns a tuple of the team number and name as strings, if present



def check_name_and_number(searchingName):
    if debug: print("{0.BOLD}{1}{0.END}:".format(color,searchingName)) #I know, I know. All of this if debug nonsense just clutters up the code. Whatever.
    possible = []
    found = False
    number, name = _get_number_and_name(searchingName)
    if name not in bad_words:
        for i in range(len(allTeams)):
            if str(allTeams[i]['team_key']) == number:
                possible.append((str(allTeams[i]['team_name_short']),str(allTeams[i]['team_key'])))
                found = True
                if debug: print("\tA team, {0} was found by their number {1}".format(allTeams[i]['team_name_short'],allTeams[i]['team_key']))
                continue
            try:
                if fuzz.ratio(allTeams[i]["team_name_short"].lower().replace(" ", ""),str(name)) >= 75: #Detects at least 75% similarity in the team names
                    possible.append((str(allTeams[i]["team_name_short"]),str(allTeams[i]["team_key"]))) #adds the found team's name and number to the list of possible teams
                    found = True
                    if debug: print("\tA team, {0} was found by their name".format(allTeams[i]['team_name_short']))
            except AttributeError:
                continue

    else:
        if debug: print("\tThe name {} is not valid".format(searchingName))
        return None
    if found == False:
        if debug: print("\tThe name {} was not found".format(searchingName))
        return None
    return (possible[0] if len(possible) == 1 else possible)

def scrape_all_teams():
    url = 'https://theorangealliance.org/api/team/'
    return requests.get(url,headers=PARAMS).json()

def run_bulk_teams(handles):
    problems = []
    teams = []
    team_info = list(filter(None,list(map(check_name_and_number,handles)))) #Runs handles through check_name_and_number, and results in a list of tuples containing a team name and number.
    for i in range(len(team_info)):
        numbers = team_info[i]
        if type(numbers) == list:
            problems.append(team_info[i])
            print(team_info[i],'was sent to problems')
        elif type(numbers[0]) == str:
            teams.append([numbers[0],numbers[1],handles[i]]) #A list. Field 1 is the name, 2 is the number, 3 is the handle.
            print(team_info[i],'was sent to teams')
    return problems,teams

class color: #For fancy formatting for debug because I'm extra
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

if __name__ == '__main__': #yay it works
    allTeams = scrape_all_teams()
    problems, teams = run_bulk_teams()
    print('problems',problems)
    print('teams',teams)
