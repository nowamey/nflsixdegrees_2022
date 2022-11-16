from logging import exception
from xml.etree.ElementTree import Comment
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import time
import json
# this file is responsible for running all webscraping operations, and organizing information to be used by sixdegrees.py
COLS =["Number","Player","Age","Position","G","GS","Wt","Ht","College/Univ","Birthdate","yrs","Drafted","team"]
data = pd.DataFrame(columns=COLS)
playercount=0 
players_dict = dict() #maps filtered strings to a list of players to be iterated
players_list = []
teams_map = dict() #map teamname,year, to list of players on the
#comm implemented to help pull from table that isnt directly embedded in the html
comm = re.compile("<!--|-->")

TEAMS = ["buf","mia","nyj","nwe","oti","clt","jax","htx","rav","cin","cle","pit","kan","sdg","den","rai",
        "phi","dal","nyg","was","tam","atl","nor","car","min","gnb","det","chi","sfo","crd","ram","sea"]
FULLNAMES = ["Buffalo Bills","Miami Dolphins","New York Jets","New England Patriots","Tennessee Titans","Indianapolis Colts","Jacksonville Jaguars",
             "Houston Texans","Baltimore Ravens","Cincinatti Bengals","Cleveland Browns","Pittsburgh Steelers","Kansas City Chiefs","Los Angeles Chargers",
             "Denver Broncos","Las Vegas Raiders","Philadelphia Eagles","Dallas Cowboys","New York Giants","Washington Commanders","Tampa Bay Buccaneers",
             "Atlanta Falcons","New Orleans Saints","Carolina Panthers","Minnesota Vikings","Green Bay Packers","Detroit Lions","Chicago Bears",
             "San Francisco 49ers","Arizona Cardinals","Los Angeles Rams","Seattle Seahawks"]
class Player:
    def __init__(self,player_name,position,teams_list,url,active = False):
        self.player_name = player_name
        self.position = position
        self.teams_list = teams_list
        self.url = url

        for team in self.teams_list:
            if team[1] == '2022':
                self.active = True

    def __repr__(self):
        return f"({self.player_name}, {self.position},{self.teams_list},{self.url}, {self.active})"   
class Team:
    def __init__(self,team_name,year):
        self.team_name = team_name
        self.year = year
        players = get_roster(team_name,year)
    def __repr__(self):
        return f"{self.team_name} {self.year}"
def gethtml(url):
    #gethtml grabs html document to parse through for any given site
    page = requests.get(url)
    print(page)
    soupdata = BeautifulSoup(comm.sub("",page.text),'lxml')
    return soupdata
def get_roster(team,year):
    #getroster retrieves the actual table for a team roster
    time.sleep(5)
    soup = gethtml(f"https://www.pro-football-reference.com/teams/{team}/{year}_roster.htm")
    roster = soup.find('table',{'id':'roster'})
    return roster
def run_retrieval():
    roster = get_roster('rav',2022)
    get_players(roster)
    print(players_dict)
    print("\n\n\n")
    print(teams_map)
    #with open(r"c:/Users/nowam/Documents/Github/nflsixdegrees_2022/players_dict.json","w") as f:
    #    json.dump(players_dict,f)
    #with open(r"c:/Users/nowam/Documents/Github/nflsixdegrees_2022/teams_map.json","w") as f:
    #    json.dump(teams_map,f)
def get_csv():    
    data.to_csv(r"C:\Users\nowam\Documents\GitHub\nflsixdegrees_2022\player_data.csv",index= False)
def get_players(roster):
    #gets all active players into datastructure for search requests from front-end
    global players_dict
    global players_list
    
    for row in roster.find_all('tr'):
        rowsdata = row.find_all('td')
        links = row.find_all('a')
        row = [i.text for i in rowsdata]
        time.sleep(5)
        if(len(row)>0 and row[0]!="Team Total"):   
            link = links[0].get('href')
            name = row[0]
            position = row[2]
            url = f"http://pro-football-reference.com{link}/gamelog"
            player = Player(name,position,get_teams(url),url)
            players_dict[name] = player 
            print(player.player_name)   
def get_teams(url):
    #get_teams retrieves and returns a set of all the teams the player has played with
    soup =  (gethtml(url))
    logs = soup.find('table',{'id':'stats'}) #grabs the gameslog table: columns of interest : year, team
    
    #behold, the parsing 
    teams = set()
    
    for row in logs.find_all('tr'):
        rowsdata = row.find_all('td')
        row = [i.text for i in rowsdata]
        #certain rows are not neccessary, this dismisses them
        if(len(row)>5 and row[0]!=''):
            teams.add((row[5],row[0]))
    return teams

    
     
if __name__ == "__main__":
    run_retrieval()
    
    
    
    
        
    
    

    
        
        

        

