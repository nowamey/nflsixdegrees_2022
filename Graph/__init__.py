from collections import deque
import networkx as nx

class Graph:
    def __init__(self):
        self.connections = {}
        self.size = 0

    def addNode(self, value):
        if self.nodeExists(value) == True: return
        self.connections[value] = set() # can only have one connection to each other value
        self.size += 1

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
    
    def to_graphml(self):
        graph = nx.Graph()

        for node, neighbors in self.connections.items():
            for neighbor in neighbors:
                graph.add_edge(node, neighbor)

        nx.write_graphml(graph, "football_connections.graphml")

    # makes debugging a little easier
    # prints as an adjacency list
    def __str__(self):
        s = "-- Graph contents:\n"
        for node, neighbors in self.connections.items():
            s += f"  {node}: {str(neighbors)}\n"
        return s[:-1] # chops off the last newline


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