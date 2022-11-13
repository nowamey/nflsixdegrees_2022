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
teamcounter=0
players = dict()
name_number = dict()
players_list = []
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
    def __init__(self,player_name):
        self.player_name = player_name
        self.past_teams = []
class Team:
    def __init__(self,team_name,year):
        self.team_name = team_name
        self.year = year

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
def get_data(roster):
    #gets names of every player on the roster for a given year 
    global teamcounter
    for row in roster.find_all('tr'):
            rowsdata = row.find_all('td')
            row = [i.text for i in rowsdata]
            
            #Taking into account undrafted players
            row.append(FULLNAMES[teamcounter])
            
                
            length = len(data)
            print(row)
            
            if(len(row) == 13):

                if(row[11] == ""):
                    row[11] = "Undrafted"
                
                
                if(row[0] != "Team Total"):
                    data.loc[length] = row
    teamcounter+=1
def run_retrieval():
    for team in TEAMS:
        roster = getRoster(team,2022)
        get_data(roster)
    get_csv()
    return data                        
def get_csv():    
    data.to_csv(r"C:\Users\nowam\Documents\GitHub\nflsixdegrees_2022\player_data.csv",index= False)
def get_players(roster):
    global teamcounter
    global players
    rosterplayers = []
    for row in roster.find_all('tr'):
            rowsdata = row.find_all('td')
            row = [i.text for i in rowsdata]
            player = Player(row[0],get_teams(row[0]))

            #making sure we dont add players more than we need to
            if(player not in players_list):    
                players_list.append(player)
                players[row[0]] = player
            #Taking into account undrafted players
            row.append(FULLNAMES[teamcounter])
            
                
            length = len(data)
            
            
            if(len(row) == 13):        
                if(row[0] != "Team Total"):
                    data.loc[length] = row
    players.append
    teamcounter+=1
def get_teams(name):
   global players
   #should give me a  monstrosity 
   print(gethtml(f"http://pro-football-reference.com/players/{'S'}/{filtername(name)}00.htm"))
   
def findnamecode(name):
    #this method checks if the name in question is actually at the first link, if not, checks next link
    pass
#proof of concept, we can get down to just names :)
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
    return firstlast  
    
    
if __name__ == "__main__":
    #run_retrieval()
    print('ayeeeee')
    
    
    
        
    
    

    
        
        

        

