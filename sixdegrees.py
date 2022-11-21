# Early idea, levels of seperation
#1. check if same team already, already done
#2. check for previous nfl or college teammates
#3. check for mutual previous nfl or college teammates
#4. mutual of mutuals until you either find a connection, or there is no confirmed connection
#
#5. Need to get the team history of EVERY PLAYER 
#
"""
player class holds individual data for all players

Attributes: 

past_teams {teamname: list[years(int)]}: contains a mapping of all years that the player was on any team,
used to check if players were on the same roster at some year 

age: age of player 
weigth: weight of player
height: string height of player in form f'i''
position: abbreviated string of player position listed on the roster

"""
import time
import retrieval
import json
class SixDegrees:

    
    
    def __init__(self):
        
        with open("players_dict.json","r") as f:
            self.players_dict = json.load(f)
        with open("teams_map.json","r") as f:
            self.teams_map = json.load(f)
        
    
    
    def run_menu(self):
        print("Welcome to Six Degrees of the NFL! Please enter Two NFL players you would like to connect!")
        time.sleep(.2)
        player1 = self.players_dict[input("Please enter first player name: ")]
        player2 = self.players_dict[input("Please enter second player name: ")]
        player1 = retrieval.Player(player1['player_name'],player1['position'],player1['teams_list'],player1['url'])
        player2 = retrieval.Player(player2['player_name'],player2['position'],player2['teams_list'],player2['url'])
        
        return player1.findpath(player2)
    
    
        

if __name__ =="__main__":
    sixdegrees= SixDegrees()
    sixdegrees.run_menu()