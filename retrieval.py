from logging import exception
from xml.etree.ElementTree import Comment
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import time
# this file is responsible for running all webscraping operations, and organizing information to be used by sixdegrees.py
COLS =["Number","Player","Age","Position","G","GS","Wt","Ht","College/Univ","Birthdate","yrs","Drafted","team"]
data = pd.DataFrame(columns=COLS)
playercount=0 
player_dict = dict() #maps filtered strings to a list of players to be iterated
players_list = []
teams = set()
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
    def __init__(self,player_name,position,weight,teamslist = [],url = None):
        self.player_name = player_name
        self.past_teams = []
    def __repr__(self):
        return f"{self.player_name}\n{self.past_teams}"
    
class Team:
    def __init__(self,team_name,year):
        self.team_name = team_name
        self.year = year
        players = []

def gethtml(url):
    #gethtml grabs html document to parse through for any given site
    page = requests.get(url)
    print(page)
    soupdata = BeautifulSoup(comm.sub("",page.text),'lxml')
    return soupdata
def getRoster(team,year):
    #avoid rate limit from pfr 
    time.sleep(1)
    soup = gethtml(f"https://www.pro-football-reference.com/teams/{team}/{year}_roster.htm")
    roster = soup.find('table',{'id':'roster'})
    return roster
def run_retrieval():
    for team in TEAMS:
        roster = getRoster(team,2022)
        get_players(roster)
    return players_list

    return data                        
def get_csv():    
    data.to_csv(r"C:\Users\nowam\Documents\GitHub\nflsixdegrees_2022\player_data.csv",index= False)
def get_players(roster):
    #gets all players into datastructure based on search term, assigns players an id in turn,
    # so once requested we know which exact player url needs to be searched
    global player_dict
    global players_list
    rosterplayers = []
    for row in roster.find_all('tr'):
            rowsdata = row.find_all('td')
            row = [i.text for i in rowsdata]
            
            searchterm = filtername(row[0])
            player = Player(row[0],row[2],row[5])
            if(player_dict[searchterm] is None):
                player_dict[searchterm] = []
                player_dict[searchterm].append(player)
            else:
                #making sure we dont add players more than we need to
                if(player not in players_list):    
                    players_list.append(player)
                    player_dict[searchterm].append(player)
def assign_ids_teams():
    global player_dict
    
    for term in player_dict.keys():
        for player in players:
            pass
    pass
   
    
def get_teams(name):
    global players
    #scrape game logs to build out a list of team objects (year,name)
    url = f"http://pro-football-reference.com/players/{filtername(name)[0]}/{filtername(name)[1]}00/gamelog"
    soup =  (gethtml(url))
    logs = soup.find('table',{'id':'stats'}) #grabs the gameslog table: columns of interest : year, team
    
    #behold, the parsing 
    teams = dict()
    
    for row in logs.find_all('tr'):
        rowsdata = row.find_all('td')
        row = [i.text for i in rowsdata]
        #certain rows are not neccessary, this dismisses them
        if(len(row)>5 and row[0]!=''):
            teams[row[0]] =row[5]
    return teams

    
    
   
    
    
   
def findnamecode(name):
    #this method checks if the name in question is actually at the first link, if not, checks next link
    #important for edge case of people having the same name abbreviation, doesnt mean they are the exact same name
    pass

def filtername(name):
    #helps get names in format so be searched in browser 
    ir = False
    
    firstlast = []
    counter =0
    for char in name:
        if(char == "("):
            ir = True
            name = name[0:counter-1]
            break
        counter+=1
    counter = 0
    for char in name:
        if (char == " "):
            break
        counter+=1
    firstlast = f"{name[counter+1:counter+5]}{name[0:2]}"      
    #tuple gives us last initial, and name abbreviation.
    return name[counter+1],firstlast
    
    
if __name__ == "__main__":
    #run_retrieval()
    print('ayeeeee')
    
    
    
        
    
    

    
        
        

        

