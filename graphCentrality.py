from math import *

class Node:
    def __init__(self, name, latitude = None, longitude = None):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        return self.name

class Edge:

    def __init__(self, node1, node2, weight, directed, name):
        self.name = name
        self.node1 = node1
        self.node2 = node2
        self.weight = weight
        self.directed = directed

    def __str__(self):
        return self.name


class Graph:
    def __init__(self):
        self.nodes={}
        self.neighbouringNodes = {}
        self.edgesOfNode = {}
        self.positonOfNodes = {}

    def add_node(self, node):
        if not isinstance(node, Node):
            raise Exception("not instantiated node")
        if node.name not in self.nodes.keys():
            self.nodes[node.name] = node
            self.neighbouringNodes[node] = []
        
    def add_edge(self, node1, node2, weight = 1, directed = False, name = None):
        if isinstance(node1, Node) and isinstance(node2, Node):
            e = Edge(node1, node2, weight, directed, name)
            
            if node1 in self.nodes.values() and node2 in self.nodes.values():
                self.neighbouringNodes[node2].append(node1)
                self.edgesOfNode[(node1, node2)] = e 
                if (e.directed == False):
                    self.neighbouringNodes[node1].append(node2)
            else:
                raise Exception("please add the nodes to the graph first!!")

        else:
            raise Exception("Please initialize the nodes first!!")
    
    def addPosition(self, file):
        wholeFile = open(file, "r")
        for line in wholeFile.readlines():
            lineInfo = line.split()
            if lineInfo[0] in self.nodes.keys():
                a = self.nodes[lineInfo[0]]
                a.latitude = radians(float(lineInfo[1]))
                a.longitude = radians(float(lineInfo[2]))

    def calculateHeuristic(Self, start, end):
        longtiude_diff = end.longitude - start.longitude
        latitude_diff = end.latitude - start.latitude
        a = sin(latitude_diff / 2)**2 + cos(start.latitude) * cos(end.latitude) * sin(longtiude_diff / 2)**2

        heuristic_value = 12742.02 * asin(sqrt(a))

        return heuristic_value

    def getGraph(self):
        print("Nodes: " , self.nodes.keys() , "\n\n")
        di2 = {}
        for edgeKey in self.edgesOfNode.keys():
            temp = edgeKey
            di2[(temp[0].name, temp[1].name)] = self.edgesOfNode[edgeKey].name
        print("edges: ", di2.values() ,"\n\n")
        print("edges connecting the nodes: ", di2 ,"\n\n")
        di = {}
        for key in self.neighbouringNodes.keys():
            li2 = []
            for item in self.neighbouringNodes[key]:
                li2.append(item.name) 
            di[key.name] = li2
        print("Nodes with their neighbors: ", di ,"\n\n")

    def dijkstra(self, startingNode, targetNode):
        distanceTracker = {}
        adjacentssTracker = {}
        distance = {startingNode : 0}
        adjacentsList = {}
        path = [targetNode.name]
        current = startingNode
        while(current != targetNode):
            for neighbour in self.neighbouringNodes[current]:
                if neighbour not in distance.keys():
                    temp = (current, neighbour)
                    if temp not in self.edgesOfNode.keys():
                        temp = (neighbour, current)
                    tempD = distance[current] + self.edgesOfNode[temp].weight
                    if neighbour not in distanceTracker.keys() or distanceTracker[neighbour] > tempD:
                        distanceTracker[neighbour] = tempD
                        adjacentssTracker[neighbour] = current
            nextKey = min(distanceTracker, key=distanceTracker.get)
            distance[nextKey] = distanceTracker[nextKey]
            adjacentsList[nextKey] = adjacentssTracker[nextKey]
            distanceTracker.pop(nextKey)
            adjacentssTracker.pop(nextKey)
            current = nextKey

        last = targetNode
        while(last != startingNode):
            path.append(adjacentsList[last].name)
            last = adjacentsList[last]
        path.reverse()
        # print("Total Cost: \t", distance[targetNode])
        return path, distance[targetNode]
        
    def AStar(self, file,  startingNode, targetNode):
        self.addPosition(file)
        distanceTracker = {}
        adjacentssTracker = {}
        distance = {startingNode : 0}
        adjacentsList = {}
        heuristic = {}
        f = {}
        path = [targetNode.name]
        current = startingNode
        while(current != targetNode):
            for neighbour in self.neighbouringNodes[current]:
                if neighbour not in distance.keys():
                    temp = (current, neighbour)
                    if temp not in self.edgesOfNode.keys():
                        temp = (neighbour, current)
                    tempD = distance[current] + self.edgesOfNode[temp].weight
                    heuristic[neighbour] = self.calculateHeuristic(neighbour, targetNode)
                    tempF = heuristic[neighbour] + tempD 
                    if neighbour not in f.keys() or f[neighbour] > tempF:
                        distanceTracker[neighbour] = tempD
                        adjacentssTracker[neighbour] = current
                        f[neighbour] = tempF
            nextKey = min(f, key=f.get)
            distance[nextKey] = distanceTracker[nextKey]
            adjacentsList[nextKey] = adjacentssTracker[nextKey]
            f.pop(nextKey)
            distanceTracker.pop(nextKey)
            adjacentssTracker.pop(nextKey)
            current = nextKey

        last = targetNode
        while(last != startingNode):
            path.append(adjacentsList[last].name)
            last = adjacentsList[last]
        path.reverse()
        # print("Total Cost: \t", distance[targetNode])
        return path, distance[targetNode]

    def degreeCentrality(self):
        degree ={}
        maxi = []
        length = len(self.nodes) - 1
        for item in self.neighbouringNodes.keys():
            degree[item.name] = len(self.neighbouringNodes[item]) / length
        maxDegree = max(degree, key=degree.get)
        maxi.append(maxDegree)
        for item in degree.keys():
            if item == maxDegree:
                continue
            if degree[item] == degree[maxDegree]:
                maxi.append(item)
        print("\nThe Node(s) with maximum degree centrality is/are: ",maxi, "with degree centrality",degree[maxDegree])
        print("\nDegree of All nodes: ",degree,"\n\n")

    def betweenessCentralityDijkstra(self):
        betweeness = {}
        highest = []
        length = len(self.nodes)
        denominator = (length * (length-1)) / 2
        nodesList = self.nodes.values()
        nodesList = list(nodesList)
        for i in range(length):
            for j in range (i+1, length):
                answer = self.dijkstra(nodesList[i],nodesList[j])
                if len(answer[0]) > 2:
                    for k in range(1, len(answer[0])-1):
                        if answer[0][k] not in betweeness.keys():
                            betweeness[answer[0][k]] = 1 / (denominator)
                        else:
                            betweeness[answer[0][k]] = betweeness[answer[0][k]] + (1/(denominator))
        for key in betweeness.keys():
            if betweeness[key] == max(betweeness.values()):
                highest.append(key)
        print("\nThe Node(s) with maximum betweenness centrality using Dijkstra is/are: ",highest, "with betweenness centrality value of",max(betweeness.values()))
        print("\nBetweenness of All nodes with value different from 0: ",betweeness, "\n\n")

    def betweenessCentralityAStar(self, file):
        betweeness = {}
        highest = []
        length = len(self.nodes.values())
        denominator = (length * (length-1)) / 2
        nodesList = self.nodes.values()
        nodesList = list(nodesList)
        for i in range(length):
            for j in range (i+1, length):
                answer = self.AStar(file, nodesList[i],nodesList[j])
                if len(answer[0]) > 2:
                    for k in range(1, len(answer[0])-1):
                        if answer[0][k] not in betweeness.keys():
                            betweeness[answer[0][k]] = 1 / (denominator)
                        else:
                            betweeness[answer[0][k]] = betweeness[answer[0][k]] + (1/(denominator))
        for key in betweeness.keys():
            if betweeness[key] == max(betweeness.values()):
                highest.append(key)
        print("\nThe Node(s) with maximum betweenness centrality using A* is/are: ",highest, "with betweenness centrality value of",max(betweeness.values()))
        print("\nBetweenness of All nodes with value different from 0: ",betweeness, "\n\n")

    def closnessCentralityDijkstra(self):
        closness = {}
        lowest = []
        for startNode in self.nodes.values():
            sum = 0
            for endNode in self.nodes.values():
                if startNode.name == endNode.name:
                    continue
                answer = self.dijkstra(startNode, endNode)
                sum+=answer[1]
            closness[startNode.name] = (len(self.nodes)-1) / sum
        for key in closness.keys():
            if closness[key] == max(closness.values()):
                lowest.append(key)
        print("\nThe Node(s) with closest to most of the nodes according to Dijkstra is/are: ",lowest, "with value of",max(closness.values()))
        print("\nclosness of All nodes: ",closness, "\n\n")

    def closnessCentralityAStar(self, file):
        closness = {}
        lowest = []
        for startNode in self.nodes.values():
            sum = 0
            for endNode in self.nodes.values():
                if startNode.name == endNode.name:
                    continue
                answer = self.AStar(file, startNode, endNode)
                sum+=answer[1]
            closness[startNode.name] = (len(self.nodes)-1) / sum
        for key in closness.keys():
            if closness[key] == max(closness.values()):
                lowest.append(key)
        print("\nThe Node(s) with closest to most of the nodes according to A* is/are: ",lowest, "with value of",max(closness.values()))
        print("\nclosness of All nodes: ",closness, "\n\n")
                

    def to_aj_matrix(self):
        mx = []
        for nodeX in self.nodes.values():
            nodeYs = []
            for nodeY in self.nodes.values():
                if nodeY in self.neighbouringNodes[nodeX]:
                    nodeYs.append(1)
                    continue
                nodeYs.append(0)
            mx.append(nodeYs)
        print(mx) 

def Initializer(fileName):
    g = Graph()

    wholeInfo = open(fileName, "r")
    for line in wholeInfo.readlines():
        lineInfo = line.split()
        if lineInfo[0] not in g.nodes.keys():
            a = Node(lineInfo[0])
            g.add_node(a)
        if lineInfo[1] not in g.nodes.keys():
            b = Node(lineInfo[1])
            g.add_node(b)
        node1 = g.nodes[lineInfo[0]]
        node2 = g.nodes[lineInfo[1]]
        temp = (node1, node2)
        if temp not in g.edgesOfNode.keys():
            temp = (node2, node1)
        if temp not in g.edgesOfNode.keys():    
            g.add_edge(node1, node2, float(lineInfo[2]), name=lineInfo[3])
    
    g.degreeCentrality()
    g.betweenessCentralityDijkstra()
    g.betweenessCentralityAStar("position.txt")
    g.closnessCentralityDijkstra()
    g.closnessCentralityAStar("position.txt")


Initializer(fileName="graph.txt")