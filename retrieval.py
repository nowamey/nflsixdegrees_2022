from logging import exception
from xml.etree.ElementTree import Comment
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import time
import json
# this file is responsible for running all webscraping operations, and organizing information to be used by sixdegrees.py
COLS =["playerid","number","player_name",'team',"age",'pos',"games","games_started","weight","height","college","birthdate","yrs","av","drafted"]
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
    def __init__(self,player_name,position,teams_list,url):
        self.player_name = player_name
        self.position = position
        self.teams_list = teams_list
        self.url = url
       
        for team in self.teams_list:
            if team[1] == '2022':
                self.active = True

    def __repr__(self):
        return f"({self.player_name}, {self.position},{self.teams_list},{self.url})"   

        
    def findpath(self,player_two):
        """
        Search playersdict for the shortest path relating two connected players 
        """
        queue = [self]
        visited = set()
        visited.add(self)
    
        while(queue):
            curr = queue.pop(0)
            #assuming these list comps just work for now 
            if(curr not in visited):
                if(curr == player_two):
                    return("search complete! Theres a connection!")
            visited.add(curr)

        
            rosters = [teams_map[tuple(team)] for team in self.teams_list]
            neighbors = [player for player in [roster for roster in rosters]]

            for neighbor in neighbors:
                if(neighbor not in visited):
                    queue.append(neighbor)
        return("Search failed! no connection!")

      
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
    global data
    year =2022
    while(year>=2004):
        for team in TEAMS:
            roster = get_roster(team,year)
            get_players(roster,team,year)
        year-=1    
    data.to_csv('nfl_players_data.csv')

def get_csv():    
    data.to_csv(r"C:\Users\nowam\Documents\GitHub\nflsixdegrees_2022\player_data.csv",index= False)
def get_players(roster,team,year):
    #gets all active players into datastructure for search requests from front-end
    global data
    
    for row in roster.find_all('tr'):
        number = get_num(row.find('th'))
        rowsdata = row.find_all('td')
        links = row.find_all('a')
        row = [i.text for i in rowsdata]
        if(len(row)>0 and row[0]!="Team Total"):   
            link = links[0].get('href')
            row.insert(0,get_id(link))
            row.insert(2,f'{team }{year}')
            row.insert(1,number)
            if(len(row) == 16):
                row.pop()
            data.loc[len(data.index)] = row
def get_id(link):
    print(link)
    exp = r".+\/(?P<id>.+)\."
    return re.search(exp,link).group('id')
def get_num(num):
    exp = r">(?P<num>\d+)<"   
    return re.search(exp,num).group('num')         
        
def get_teams(url):
    ##not used anymore for right now.
    #get_teams retrieves and returns a set of all the teams the player has played with
    global teams_map
    soup =  (gethtml(url))
    logs = soup.find('table',{'id':'stats'}) #grabs the gameslog table: columns of interest : year, team
    
    #behold, the parsing 
    teams = set()
    
    for row in logs.find_all('tr'):
        rowsdata = row.find_all('td')
        row = [i.text for i in rowsdata]
        #certain rows are not neccessary, this dismisses them
        if(len(row)>5 and row[0]!=''):
            team = str(row[5].lower())
            year = row[0]
            teams.add(f'{team}{year}')
    return list(teams)    
def clean_name(name):
    #not used anymore for now
    index =0
    for letter in name:
        if(letter == '('):
            return name[0:index-1]
        index+=1
    return name
            
if __name__ == "__main__":
    run_retrieval()
    
    
    
    
    
        
    
    

    
        
        

        

