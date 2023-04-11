# temp file for defining a demo graph

# implication of this graph is that each value will
# only exist once-- these means that if 'Steph Currry' was
# a node, there could be no other 'Steph Curry'.

# to combat this problem, it would be beneficial to use an id as
# the value of a node

from collections import deque

class Graph:
    def __init__(self):
        self.connections = {}

    def addNode(self, value):
        self.connections[value] = set() # can only have one connection to each other value

    def nodeExists(self, value):
        return self.connections.get(value) != None

    def getNodeNeighbors(self, value):
        # if node does not exist, create node
        if self.nodeExists(value) == False:
            self.addNode(value)
        return self.connections.get(value)

    def addNeighbor(self, value0, value1):
        self.getNodeNeighbors(value0).add(value1)
        self.getNodeNeighbors(value1).add(value0)

    def bfs(self, origin, target):
        if self.nodeExists(origin) == False:
            raise ValueError(f"Node {origin} does not exist.")
        elif self.nodeExists(target) == False:
            raise ValueError(f"Node {target} does not exist.")
        elif origin == target: # already at target
            return [origin]
        
        queue = deque([(origin, [origin])]) # store tuples that contain (node, path)
        visited = set([origin])

        while queue:
            curr, path = queue.popleft()

            for neighbor in self.getNodeNeighbors(curr):
                if neighbor in visited: continue
                if neighbor == target: return path + [neighbor] # no need to continue iterating if found

                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

        return None
    
    # makes debugging a little easier
    # prints as an adjacency list
    def __str__(self):
        s = "-- Graph contents:\n"
        for node, neighbors in self.connections.items():
            s += f"  {node}: {str(neighbors)}\n"
        return s[:-1] # chops off the last newline


# simplified for sake of example
exampleTeam0 = {
    "name": "Derps",
    "year": 2022,
    "players": [
        "will slice",
        "med grivel",
        "noah ramey",
        "donal heidenblad"
    ]
}

exampleTeam1 = {
    "name": "Derps",
    "year": 2023,
    "players": [
        "will slice",
        "boss baby",
        "mario",
        "luigi"
    ]
}

# populate graph
def addPlayersToGraph(graph, players):
    numPlayers = len(players)

    # iterate through each player
    for i in range(0, numPlayers):
        player0 = players[i]

        # add connections to all players that aren't the 'player0'
        for j in range(i + 1, numPlayers):
            player1 = players[j]
            graph.addNeighbor(player0, player1)

graph = Graph()

addPlayersToGraph(graph, exampleTeam0["players"])
addPlayersToGraph(graph, exampleTeam1["players"])

# prints current adjacency list
# print(graph)

# bfs to find closest connection between 'noah ramey' and 'mario'
path = graph.bfs("noah ramey", "mario")
print(path)

# throw an error when looking for a node that doesn't exist
try:
    path = graph.bfs("luigi", "princess peach")
except ValueError:
    print("uh oh! encountered an error!")



# return none when there's no path
graph.addNode("derper")
path = graph.bfs("derper", "mario")
print(path)

# we're going to have to hope that each player has an id attached to their name. otherwise, we will have to
# create a hash based on the player's name and birthday (and hope there's no duplicates lul).

