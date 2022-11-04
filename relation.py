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
ALL_PLAYERS = dict()

class player:

    def __init__(self,past_teams,age,weight,height,position,drafted):
        self.past_teams = past_teams # need to get this as a dictionary of {teamname: years in form 2001,2002,etc}
        self.age = age 
        self.weight = weight
        self.height = height
        self.position = position

def findpath(player_one,player_two):
    """find path takes any two players in the NFL, and finds their shortest path to eachother based on their degrees of social seperation
        0 degrees: same team, or past team, in which case year is specified
        beyond the same team, there is another degree of seperation for each new mutual link there is to connect the players to eachother 

        Returns: list starting with player one, ending at player two with the connective path between them in the list
    """
def run_menu():
    print("Welcome to Six Degrees of the NFL! Please enter Two NFL players you would like to connect!")
    time.sleep(.2)
    player1 = input("Please enter first player name: ")
    player2 = input("Please enter second player name: ")
    players = [player1,player2]
    return players

if __name__ == "__main__":
    players = run_menu()
    findpath(players[0],players[1])
    ALL_PLAYERS =  retrieval.getplayers()
    