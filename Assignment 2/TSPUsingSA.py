import math
import random
from math import *
import time
from statistics import mean

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

    def dijkstraTester(self):
        length = len(self.nodes)
        nodesList = self.nodes.values()
        nodesList = list(nodesList)
        pathList = []
        lengthList = []
        for i in range(length):
            for j in range (length):
                if j==i or nodesList[j] in self.neighbouringNodes[nodesList[i]]:
                    continue
                answer = self.dijkstra(nodesList[i],nodesList[j])
                if len(answer[0]) == length:
                    pathList.append(answer[0])
                    lengthList.append(answer[1])
        
        return pathList, lengthList

class SaForTsa:	
    def __init__(self, graph):
        self.graph = graph
        self.START_COORDINATE = -2
        self.START_CITY = graph.nodes[next(iter(graph.nodes))]
        print(self.START_CITY)
        self.END_COORDINATE = 2
        self.START_TEMPRATURE = 100
        self.END_TEMPRATURE = 1
        self.COOLLING_RATE = 0.0002
        self.currentCoor = random.uniform(self.START_COORDINATE, self.END_COORDINATE)
        self.bestCoor = self.currentCoor
        

    def getEnergy(self, x):  #change
        return (x-0.3)*(x-0.3)*(x-0.3)-5*x+x*x-2

    def acceptanceProb(self, energy, newEnergy, temprature):
        if(newEnergy < energy):
            return 1
        return math.exp((energy-newEnergy)/temprature)

    def findOptimum(self):
        temprature = self.START_TEMPRATURE

        while(temprature>self.END_TEMPRATURE):
            nextCoor = random.uniform(self.START_COORDINATE, self.END_COORDINATE)
            currentEnergy = self.getEnergy(self.currentCoor)
            nextEnergy = self.getEnergy(nextCoor)

            if self.acceptanceProb(currentEnergy, nextEnergy, temprature) > random.uniform(0,1):
                self.currentCoor = nextCoor

            if self.getEnergy(self.currentCoor) > self.getEnergy(self.bestCoor):
                self.bestCoor = self.currentCoor

            temprature = temprature - (temprature*self.COOLLING_RATE)

        return self.bestCoor

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
    
    a = SaForTsa(g)
    print(a.findOptimum())

Initializer("graph.txt")

