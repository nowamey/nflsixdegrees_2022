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

class SixDegrees:

    
    
    def __init__(self):
        #attributes: players: dictionary: name: Player object with that name
        #           players_list: list of all player objects currently in the nfl
        data = retrieval.run_retrieval() #tuple holding all relevant data, will apply to the sixdegrees object
        

    def findpath(player_one,player_two):
        """
        """
    def run_menu():
        print("Welcome to Six Degrees of the NFL! Please enter Two NFL players you would like to connect!")
        time.sleep(.2)
        player1 = input("Please enter first player name: ")
        player2 = input("Please enter second player name: ")
        players = [player1,player2]
        return players
        

if __name__ =="__main__":
    sixdegrees= SixDegrees()
    sixdegrees.run_menu