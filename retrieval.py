from logging import exception
from xml.etree.ElementTree import Comment
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import time

comm = re.compile("<!--|-->")

teams = ["buf","mia","nyj","nwe","oti","clt","jax","htx","rav","cin","cle","pit","kan","sdg","den","rai",
        "phi","dal","nyg","was","tam","atl","nor","car","min","gnb","det","chi","sfo","crd","ram","sea"]

fullnames = ["Buffalo Bills","Miami Dolphins","New York Jets","New England Patriots","Tennessee Titans","Indianapolis Colts","Jacksonville Jaguars",
             "Houston Texans","Baltimore Ravens","Cincinatti Bengals","Cleveland Browns","Pittsburgh Steelers","Kansas City Chiefs","Los Angeles Chargers",
             "Denver Broncos","Las Vegas Raiders","Philadelphia Eagles","Dallas Cowboys","New York Giants","Washington Commanders","Tampa Bay Buccaneers",
             "Atlanta Falcons","New Orleans Saints","Carolina Panthers","Minnesota Vikings","Green Bay Packers","Detroit Lions","Chicago Bears",
             "San Francisco 49ers","Arizona Cardinals","Los Angeles Rams","Seattle Seahawks"]

def gethtml(url):
    page = requests.get(url)
    soupdata = BeautifulSoup(comm.sub("",page.text),'lxml')
    return soupdata
def getRoster(team):
    #avoid rate limit from pfr 
    time.sleep(1)
    soup = gethtml(f"https://www.pro-football-reference.com/teams/{team}/2022_roster.htm")
    roster = soup.find('table',{'id':'roster'})
    return roster

if __name__=="__main__":
    #known column declarations for the roster pages
    cols =["Number","Player","Age","Position","G","GS","Wt","Ht","College/Univ","Birthdate","yrs","Drafted","team"]
    data = pd.DataFrame(columns=cols)
    teamcounter = 0
    
    #sets to help make linking tables for db
    colleges = dict()
    positions = dict()
    teamnames = dict()
    
    for team in teams:
        roster = getRoster(team)
        
        for row in roster.find_all('tr'):
            rowsdata = row.find_all('td')
            row = [i.text for i in rowsdata]
            
            #Taking into account undrafted players
            row.append(fullnames[teamcounter])
            
                
            length = len(data)
            print(row)
            
            if(len(row) == 13):

                if(row[11] == ""):
                    row[11] = "Undrafted"
                
                #should populate the row with id's from the dictionary, rather than strings
                
                data.loc[length] = row
                
        teamcounter+=1
    #Linking  tables set up for db
    
    
    
    data.to_csv(r"C:C:\Users\nowam\Documents\GitHub\nflsixdegrees_2022\player_data.csv",index= False)
    
    

    
    
    
        
    
    

    
        
        

        

