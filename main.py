from fuzzywuzzy import fuzz
import requests
from regex import sub

allTeams = []
bad_words = ['robotics', 'robots','bots','robotic','bot','robot']
PARAMS = {'Content-Type':'application/json',
            'X-TOA-Key':'nice try mate',
            'X-Application-Origin':'Atom'}


def _get_number_and_name(name):
    return sub('[^0-9]','', name), sub('[^a-z]','',name) #Returns a tuple of the team number and name as strings, if present



def check_name_and_number(searchingName):
    possible = ''
    found = False
    number,name = _get_number_and_name(searchingName)
    if name not in bad_words:
        for i in range(len(allTeams)):
            try:
                if fuzz.ratio(allTeams[i]["team_name_short"].lower().replace(" ", ""),str(name)) >= 75: #Detects at least 75% similarity in the team names
                    possible += ', ' + str(allTeams[i]["team_key"]) if len(possible) != 0 else str(allTeams[i]["team_key"]) #adds the found team to the list
                    found = True
            except AttributeError:
                continue
    else:
        sendText(number, "That is an invalid search word. (EC3 - Overflow)")
        return True
    if found == False:
        sendText(number, "That team name was not found. Please try again")
    return possible

def scrape_all_teams():
    while True:
        url = 'https://theorangealliance.org/api/team/'
            data = requests.get(url,headers=PARAMS)
            print('data is a ',type(data))
            print('the len of data is ',len(data))

if __name__ == '__main__':
    scrape_all_teams()
