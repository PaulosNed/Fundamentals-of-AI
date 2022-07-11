from dis import dis
from math import *
import math
import random
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

    def addPosition(self, file):
        wholeFile = open(file, "r")
        for line in wholeFile.readlines():
            lineInfo = line.split()
            if lineInfo[0] in self.nodes.keys():
                a = self.nodes[lineInfo[0]]
                a.latitude = radians(float(lineInfo[1]))
                a.longitude = radians(float(lineInfo[2]))

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
    
    def calculateHeuristic(Self, start, end):
        longtiude_diff = end.longitude - start.longitude
        latitude_diff = end.latitude - start.latitude
        a = sin(latitude_diff / 2)**2 + cos(start.latitude) * cos(end.latitude) * sin(longtiude_diff / 2)**2

        heuristic_value = 12742.02 * asin(sqrt(a))

        return heuristic_value
    
    def dijkstra(self, startingNode, targetNode):
        distanceTracker = {}
        adjacentssTracker = {}
        distance = {startingNode : 0}
        adjacentsList = {}
        path = [targetNode]
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
            path.append(adjacentsList[last])
            last = adjacentsList[last]
        path.reverse()
        return path, distance[targetNode]
        
    def dijkstraTester(self):
        length = len(self.nodes)
        nodesList = self.nodes.values()
        nodesList = list(nodesList)
        validList = []
        dis = []
        for i in range(length):
            for j in range (length):
                if j==i:
                    continue
                answer = self.dijkstra(nodesList[i],nodesList[j])
                if len(answer[0])==2:
                    validList.append(answer[0])
                    dis.append(answer[1])
        return validList, dis


class SimulatedAnnealing:
    def __init__(self, file) -> None:
        self.graph = Initializer(file)
        self.pathList = []
        self.distance = []
        self.randomPath = []
        self.nodes = list(self.graph.nodes.values())
        wholeInfo = open(file, "r")
        for line in wholeInfo.readlines():
            lineInfo = line.split()
            self.pathList.append([self.graph.nodes[lineInfo[0]], self.graph.nodes[lineInfo[1]]])
            self.distance.append(float(lineInfo[2]))
        self.START_TEMPRATURE = 100 
        self.END_TEMPRATURE = 1
        self.COOLLING_RATE = 0.0002
        self.currentCombo = None
        self.bestCombo = None

    def copy(self, combination):
        d = []
        for i in range(len(combination)):
            d.append(combination[i])
        return d

    # def getRandom(self):
    #     unvisited = self.copy(self.nodes)
    #     visited = []
    #     start = random.choice(self.nodes)
    #     i = 0
    #     while(True):
    #         i+=1
    #         visited.append(start)
    #         unvisited.remove(start)
    #         neighboursofStart = self.graph.neighbouringNodes[start]
    #         random.shuffle(neighboursofStart)
    #         prev = start
    #         for item in neighboursofStart:
    #             if item in unvisited:
    #                 start = item
    #                 break
    #         if prev == start:
    #             if (len(visited) == len(self.nodes)):
    #                 for item in visited:
    #                     print(visited.name)
    #                 return visited
    #             restorer = self.copy(visited)
    #             restorer.reverse()
    #             restorer.pop(0)
    #             for item in restorer:
    #                 neighboursOfItem = self.graph.neighbouringNodes[item]
    #                 neighboursOfItem = random.sample(neighboursOfItem, len(neighboursOfItem))
    #                 for neighbour in neighboursOfItem:
    #                     if neighbour in unvisited:
    #                         index = visited.index(item)
    #                         li = visited[index+1:]
    #                         unvisited.extend(li)
    #                         visited = visited[:index+1]
    #                         print(len(visited))
    #                         start = neighbour

    def getRandom(self):
        return random.sample(self.nodes, len(self.nodes))

    def getValue(self, combination):
        value = 0
        j = 1
        for i in range(len(combination)):
            temp = [combination[i], combination[j]]
            if temp not in self.pathList:
                temp = [combination[j], combination[i]]
            if temp not in self.pathList:
                value += self.graph.calculateHeuristic(temp[0], temp[1])*200
            else:
                index = self.pathList.index(temp)
                value += self.distance[index]
        return value
        
    def acceptanceProbaility(self, value, newValue, temprature):
        if(newValue < value):
            return 1
        return math.exp((value-newValue)/temprature)

    def findOptimum(self):
        self.currentCombo= self.getRandom()
        self.bestCombo= self.currentCombo
        temprature = self.START_TEMPRATURE
        while(temprature>self.END_TEMPRATURE):
            nextCombo= self.getRandom()
            currentValue = self.getValue(self.currentCombo)
            nextValue = self.getValue(nextCombo)
            if self.acceptanceProbaility(currentValue, nextValue, temprature) > random.uniform(0,1):
                self.currentCombo = nextCombo
                currentValue = nextValue
            
            if currentValue > self.getValue(self.bestCombo):
                self.bestCombo = self.currentCombo
            temprature = temprature - (temprature*self.COOLLING_RATE)
        
        bestPath = []
        for item in self.bestCombo:
            bestPath.append(item.name)
        
        return bestPath, self.getValue(self.bestCombo)

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
    
    # d = g.dijkstraTester()
    return g

s = SimulatedAnnealing("graph.txt")
s.graph.addPosition("position.txt")
print(s.findOptimum())
    
# Initializer(fileName="graph.txt")
