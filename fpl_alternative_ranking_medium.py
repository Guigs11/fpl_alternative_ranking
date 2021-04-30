# basic imports
import pandas as pd
import json
import urllib.request

################################ Data mining from the FPL API ################################
# The only 3 parameters to specify are "h2h_leagueID", the "firstGameweek" and "lastGameweek"
h2h_leagueID = 896976
firstGameweek = 1
lastGameweek = 32

# Get the head to head game results at each game week
data = []
for i in range(firstGameweek, lastGameweek+1):
    base = "https://fantasy.premierleague.com/api/leagues-h2h-matches/league/" + str(h2h_leagueID) + "/?page=1&event=" + str(i)
    page = urllib.request.urlopen(base)
    data.append(json.load(page))
    print("GW" + str(i) + " : Done.")
    
 
################################ Calculations ################################
# Calculate the number of players in the league
nb_of_games_per_gw = len(data[0]["results"])
nb_of_players_in_league = 2*nb_of_games_per_gw
        
# Get the team names in a list
teams = []
for match in range(0, nb_of_games_per_gw):
    teams.append(data[0]["results"][match]["entry_1_name"])
    teams.append(data[0]["results"][match]["entry_2_name"])
 
# Organise the data in a dict by teams
# First, create a dict of empty lists for each Team
resultsByTeam = {}
for team in teams:
    resultsByTeam.update({team : []})
     
# Second, populate the lists with the Teams data (name of the teams and their number of points at that GW)
for i in range(0, len(data)): # i = gw-1
    for match in range(0, nb_of_games_per_gw):
        for team in teams:
            if (data[i]["results"][match]["entry_1_name"] == team):
                resultsByTeam[team].append({"GW" : firstGameweek+i, "points" : data[i]["results"][match]["entry_1_points"]})
            elif (data[i]["results"][match]["entry_2_name"] == team):
                resultsByTeam[team].append({"GW" : firstGameweek+i, "points" : data[i]["results"][match]["entry_2_points"]})
    
# Create the dataframe of results per team and per gameweek: classic_ranking
gameweek = []
for gw in range(firstGameweek, lastGameweek+1):
    gameweek.append("GW" + str(gw))
gameweek_num = list(range(firstGameweek,lastGameweek+1))
points = []
 
# Initialise classic_ranking    
classic_ranking = pd.DataFrame(index=teams, columns=gameweek)
 
# Populate classic_ranking
for team in teams:
    for gw in gameweek_num:
        classic_ranking.loc[team, "GW" + str(gw)] = resultsByTeam[team][gw-firstGameweek]["points"]
 
# Create f1_ranking which is a copy of classic_ranking where we'll translate fpl points to new ranking points
f1_ranking = classic_ranking.copy()
 
# Compare each entry and assign them a number of points
# 25-18-15-12-10-8-6-4-2-1
for gw in range(firstGameweek, lastGameweek+1):
    for team1 in teams:
        f1_ranking.loc[team1, "GW" + str(gw)] = 25
        i = 0
        for team2 in [item for item in teams if item not in [team1]]:
            if (classic_ranking.loc[team1, "GW" + str(gw)] < classic_ranking.loc[team2, "GW" + str(gw)]) and (i == 0):
                f1_ranking.loc[team1, "GW" + str(gw)] = 18
                i = i+1
            elif (classic_ranking.loc[team1, "GW" + str(gw)] < classic_ranking.loc[team2, "GW" + str(gw)]) and (i == 1):
                f1_ranking.loc[team1, "GW" + str(gw)] = 15
                i = i+1
            elif (classic_ranking.loc[team1, "GW" + str(gw)] < classic_ranking.loc[team2, "GW" + str(gw)]) and (i == 2):
                f1_ranking.loc[team1, "GW" + str(gw)] = 12
                i = i+1
            elif (classic_ranking.loc[team1, "GW" + str(gw)] < classic_ranking.loc[team2, "GW" + str(gw)]) and (i == 3):
                f1_ranking.loc[team1, "GW" + str(gw)] = 10
                i = i+1
            elif (classic_ranking.loc[team1, "GW" + str(gw)] < classic_ranking.loc[team2, "GW" + str(gw)]) and (i == 4):
                f1_ranking.loc[team1, "GW" + str(gw)] = 8
                i = i+1
            elif (classic_ranking.loc[team1, "GW" + str(gw)] < classic_ranking.loc[team2, "GW" + str(gw)]) and (i == 5):
                f1_ranking.loc[team1, "GW" + str(gw)] = 6
                i = i+1
            elif (classic_ranking.loc[team1, "GW" + str(gw)] < classic_ranking.loc[team2, "GW" + str(gw)]) and (i == 6):
                f1_ranking.loc[team1, "GW" + str(gw)] = 4
                i = i+1
            elif (classic_ranking.loc[team1, "GW" + str(gw)] < classic_ranking.loc[team2, "GW" + str(gw)]) and (i == 7):
                f1_ranking.loc[team1, "GW" + str(gw)] = 2
                i = i+1
            elif (classic_ranking.loc[team1, "GW" + str(gw)] < classic_ranking.loc[team2, "GW" + str(gw)]) and (i == 8):
                f1_ranking.loc[team1, "GW" + str(gw)] = 1
                i = i+1
                               
# Add a "total" column at the end of classic_ranking
classic_ranking['total'] = classic_ranking.sum(axis=1)
classic_ranking = classic_ranking.astype('int64')
# Add a "total" column at the end of f1_ranking
f1_ranking['total'] = f1_ranking.sum(axis=1)
f1_ranking = f1_ranking.astype('int64')



'''
# Organise the data in a dict by Game Week
# First, create a dict of empty lists for each Game Week
resultsByGw = {}
for gw in range(firstGameweek, lastGameweek+1):
    resultsByGw.update({"GW" + str(gw) : []})

# Second, populate the lists with the GW data (name of the teams and their number of points at that GW)
for i in range(0, len(data)): # i = gw-1
    for match in range(0, nb_of_games_per_gw):
        resultsByGw["GW" + str(firstGameweek+i)].append({"name" : data[i]["results"][match]["entry_1_name"], "points" : data[i]["results"][match]["entry_1_points"]})
        resultsByGw["GW" + str(firstGameweek+i)].append({"name" : data[i]["results"][match]["entry_2_name"], "points" : data[i]["results"][match]["entry_2_points"]})
'''