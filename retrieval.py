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
colleges = dict()
positions = dict()
teamnames = dict()
teamcounter=0
#comm implemented to help pull from table that isnt directly embedded in the html
comm = re.compile("<!--|-->")

TEAMS = ["buf","mia","nyj","nwe","oti","clt","jax","htx","rav","cin","cle","pit","kan","sdg","den","rai",
        "phi","dal","nyg","was","tam","atl","nor","car","min","gnb","det","chi","sfo","crd","ram","sea"]

FULLNAMES = ["Buffalo Bills","Miami Dolphins","New York Jets","New England Patriots","Tennessee Titans","Indianapolis Colts","Jacksonville Jaguars",
             "Houston Texans","Baltimore Ravens","Cincinatti Bengals","Cleveland Browns","Pittsburgh Steelers","Kansas City Chiefs","Los Angeles Chargers",
             "Denver Broncos","Las Vegas Raiders","Philadelphia Eagles","Dallas Cowboys","New York Giants","Washington Commanders","Tampa Bay Buccaneers",
             "Atlanta Falcons","New Orleans Saints","Carolina Panthers","Minnesota Vikings","Green Bay Packers","Detroit Lions","Chicago Bears",
             "San Francisco 49ers","Arizona Cardinals","Los Angeles Rams","Seattle Seahawks"]

def gethtml(url):
    page = requests.get(url)
    print(page)
    soupdata = BeautifulSoup(comm.sub("",page.text),'lxml')
    return soupdata
def getRoster(team):
    #avoid rate limit from pfr 
    time.sleep(1)
    soup = gethtml(f"https://www.pro-football-reference.com/teams/{team}/2022_roster.htm")
    roster = soup.find('table',{'id':'roster'})
    return roster
def get_data(roster):
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
        roster = getRoster(team)
        get_data(roster)
    get_csv()
    return data                        
def get_csv():    
    data.to_csv(r"C:\Users\nowam\Documents\GitHub\nflsixdegrees_2022\player_data.csv",index= False)

#proof of concept, we can get down to just names :)
def player_histories():
    #work with testdata for n
    data = pd.read_csv(r"C:\Users\nowam\Downloads\rosters_data.csv")
    players = list(data["Number"]) #unsure why this is holding playernames, keeping for now to keep testing
    #cleaning the strings, getting rid of (IR, PUP, and erroneous Team totals
    filtered = []
    ir = False
    for player in players:
        counter =0
        for char in player:
            if(char == "("):
                ir = True
                filtered.append(player[0:counter-1])
                break
            counter+=1
        if(player != "Team Total"):
            if(ir == True):
                ir =False
            else:
                filtered.append(player)
    print(filtered)
    
    
if __name__ == "__main__":
    #run_retrieval()
    player_histories()
    
    
    
        
    
    

    
        
        

        

