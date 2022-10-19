
from logging import exception
from xml.etree.ElementTree import Comment
from numpy import column_stack
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
comm = re.compile("<!--|-->")

teams = ["buf","mia","nyj","nwe","oti","clt","jax","htx","rav","cin","cle","pit","kan","sdg","den","rai",
        "phi","dal","nyg","was","tam","atl","nor","car","min","gnb","det","chi","sfo","crd","ram","sea"]

def gethtml(url):
    page = requests.get(url)
    soupdata = BeautifulSoup(comm.sub("",page.text),'lxml')
    return soupdata
def getRoster(team):
    soup = gethtml(f"https://www.pro-football-reference.com/teams/{team}/2022_roster.htm")
    roster = soup.find('table',{'id':'roster'})
    return roster
    
if __name__=="__main__":
    #known column declarations for the roster pages
    cols =["Number","Player","Age","Position","G","GS","Wt","Ht","College/Univ","Birthdate","yrs","Drafted"]
    data = pd.DataFrame(columns=cols)
    
    for team in teams:
        roster = getRoster(team)
        
        for row in roster.find_all('tr'):
            rowsdata = row.find_all('td')
            row = [i.text for i in rowsdata]
            length = len(data)
        
            
            if(len(row) ==12):
                data.loc[length] = row
            
            
            
    data.to_csv(r"C:\Users\nowam\sixdegrees\df.csv",index= False)
    
    
        
    
    

    
        
        

        

