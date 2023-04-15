import requests
import time
import pandas as pd 
import numpy as np
import datetime
#very very brute force navigation of the api for now 
HEADERS =  {
	        "X-RapidAPI-Key": "e0259fc1a8mshf3acbf6e3c99144p15e1edjsnb6ad953c45df",
	        "X-RapidAPI-Host": "basketapi1.p.rapidapi.com"
        }
def get_active_players():
    nba_ids =  {x for x in range(3409,3438)}
#pelicans are disjointed, presumably because of the name change
    nba_ids.add(5539)
    data =  pd.DataFrame(columns= ['id', 'name'])
    data.set_index('id',inplace=True)
    for teamid in range(3409,3438):
        time.sleep(2)
        url = f"https://basketapi1.p.rapidapi.com/api/basketball/team/{teamid}/players"

        headers = {
	        "X-RapidAPI-Key": "e0259fc1a8mshf3acbf6e3c99144p15e1edjsnb6ad953c45df",
	        "X-RapidAPI-Host": "basketapi1.p.rapidapi.com"
        }
        response = (requests.request("GET", url, headers=headers)).json()
        #can access all players. Need to build a local mapping of ids for the players as we get them. Then go ahead, grab transfer history per id!
        for player in response['players']:
            player_id = player['player']['id']
            player_name = player['player']['name']
            print(player_id,player_name)
            data.loc[player_id] = [player_name]
    
    data.to_csv('activeplayers_2023.csv')

def get_players_history(ids):
    #passed the index of the player dataframe, calls api to assemble a comprehensive df of trade history, and append it to the 
    #history dataframe
    data = pd.DataFrame(columns = ['player_id','player_name','team',"start","end"])
    for id in ids:
        try:
            data =  pd.concat([data,addtenures(id)])
        #rookies seem to have no transaction data, this was a workaround for that issue
        except ValueError:
            #incase of an id without trades, we will fill in history with just their current team
            url = f"https://basketapi1.p.rapidapi.com/api/basketball/player/{id}" 
            response = (requests.request("GET", url, headers=HEADERS)).json()
            row =  [id,response['player']['name'],response['player']['team']['name'],np.NaN,np.NaN]
            print(row)
            data.loc[id] = row
    data.to_csv('active_player_histories.csv')

def addtenures(player_id):
    # end --> NaN signifies current team
    df = pd.DataFrame(columns = ['player_id','player_name','team',"start","end"])
    #search tenures of the given player
    url = f"https://basketapi1.p.rapidapi.com/api/basketball/player/{player_id}/transfers"

    headers = {
	    "X-RapidAPI-Key": "e0259fc1a8mshf3acbf6e3c99144p15e1edjsnb6ad953c45df",
	    "X-RapidAPI-Host": "basketapi1.p.rapidapi.com"
    }
    try:
        response = (requests.request("GET", url, headers=headers)).json()
    except ValueError: 
        raise ValueError (f"No response for playerid {player_id}")
    hist = response['transferHistory']
    

    for i,trade in enumerate(hist):
        #current team - meaning no end date
        if(i == 0):
            row = [player_id,trade['player']['name'], trade['toTeamName'],datetime.date.fromtimestamp(trade['transferDateTimestamp']),np.NaN]
        #previous teams
        else:
            row = [player_id, trade['player']['name'], trade['toTeamName'],datetime.date.fromtimestamp(trade['transferDateTimestamp']),datetime.date.fromtimestamp(hist[i-1]['transferDateTimestamp'])]
        df.loc[len(df.index)] = row
    #terminal print to keep track of properly running requests
    print(df.head())
    return df

if __name__ == "__main__":
    players = pd.read_csv('activeplayers_2023.csv')
    players.set_index('id',inplace=True)
    get_players_history(players.index)
    