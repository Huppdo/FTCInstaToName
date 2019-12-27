from fuzzywuzzy import fuzz

allTeams = []

found = False
possible = ""
if searchingName != "robotics" and searchingName != "robots" and searchingName != "bots" and searchingName != "robotic":
    for i in range(len(allTeams)):
        try:
            if fuzz.ratio(allTeams[i]["team_name_short"].lower().replace(" ", ""),str(searchingName)) >= 75:
                possible += str(allTeams[i]["team_key"]) + ", "
                found = True
        except AttributeError:
            continue
else:
    sendText(number, "That is an invalid search word. (EC3 - Overflow)")
    return True
if found == False:
    sendText(number, "That team name was not found. Please try again")
