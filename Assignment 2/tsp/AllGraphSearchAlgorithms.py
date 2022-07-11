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

    def bfs(self, startingNode, targetNode):
        if isinstance(startingNode, Node) and isinstance(targetNode, Node):
            visited = []
            queue = [startingNode]
            adjacentsList = {}
            path = [targetNode.name]
            while queue:
                if targetNode in queue:
                    length = 0
                    temp = targetNode
                    while(temp != startingNode):
                        path.append(adjacentsList[temp].name)
                        coor = (temp, adjacentsList[temp])
                        if coor not in self.edgesOfNode.keys():
                            coor = (adjacentsList[temp], temp)
                        curr_len = self.edgesOfNode[coor].weight
                        length = length + curr_len
                        temp = adjacentsList[temp]
                    path.reverse()
                    return path, length
                visited.append(queue[0])
                for queueItems in self.neighbouringNodes[queue[0]]:
                    if queueItems not in visited and queueItems not in queue:
                        queue.append(queueItems)
                        adjacentsList[queueItems] = queue[0]
                        # print(adjacentsList)
                queue.pop(0)
        else:
            raise Exception("Please enter an intiated and added starting node!!")

    def dfs(self, startingNode, targetNode):
        if isinstance(startingNode, Node):
            visited = []
            stack = [startingNode]
            adjacentsList = {}
            path = [targetNode.name]
            while stack:
                if targetNode in stack:
                    temp = targetNode
                    length = 0
                    while(temp != startingNode):
                        path.append(adjacentsList[temp].name)
                        coor = (temp, adjacentsList[temp])
                        if coor not in self.edgesOfNode.keys():
                            coor = (adjacentsList[temp], temp)
                        curr_len = self.edgesOfNode[coor].weight
                        length = length + curr_len
                        temp = adjacentsList[temp]
                    path.reverse()
                    return path, length
                poped = stack.pop()
                visited.append(poped)
                for stackItems in self.neighbouringNodes[poped]:
                    if stackItems not in visited and stackItems not in stack:
                        stack.append(stackItems)
                        adjacentsList[stackItems] = poped
                        #print(adjacentsList)
        else:
            raise Exception("Please enter an intiated and added starting node!!")

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
        beginAdd = time.perf_counter()
        self.addPosition(file)
        endAdd = time.perf_counter()
        addTime = (endAdd-beginAdd)*1000
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
                    begin = time.perf_counter()
                    heuristic[neighbour] = self.calculateHeuristic(neighbour, targetNode)
                    end = time.perf_counter()
                    addTime += (end-begin)*1000
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
        return path, distance[targetNode], addTime

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

    def bfsTester(self):
        length = len(self.nodes)
        nodesList = self.nodes.values()
        nodesList = list(nodesList)
        timeList = []
        lengthLits = []
        hopeList = []
        for i in range(length):
            for j in range (length):
                if j==i:
                    continue
                begin = time.perf_counter()
                answer = self.bfs(nodesList[i],nodesList[j])
                end =time.perf_counter() 
                t = (end - begin)*1000
                timeList.append(t)
                hopeList.append(len(answer[0]))
                lengthLits.append(answer[1])
        
        print("Average BFS length: ", mean(lengthLits))
        return mean(timeList), mean(lengthLits), mean(hopeList)
    
    def dfsTester(self):
        length = len(self.nodes)
        nodesList = self.nodes.values()
        nodesList = list(nodesList)
        timeList = []
        lengthLits = []
        hopeList = []
        for i in range(length):
            for j in range (length):
                if j==i:
                    continue
                begin = time.perf_counter()
                answer = self.dfs(nodesList[i],nodesList[j])
                end =time.perf_counter() 
                t = (end - begin)*1000
                timeList.append(t)
                hopeList.append(len(answer[0]))
                lengthLits.append(answer[1])
        
        print("Average DFS length: ", mean(lengthLits))
        return mean(timeList), mean(lengthLits), mean(hopeList)

    def dijkstraTester(self):
        length = len(self.nodes)
        nodesList = self.nodes.values()
        nodesList = list(nodesList)
        timeList = []
        lengthLits = []
        hopeList = []
        for i in range(length):
            for j in range (length):
                if j==i:
                    continue
                begin = time.perf_counter()
                answer = self.dijkstra(nodesList[i],nodesList[j])
                end =time.perf_counter() 
                t = (end - begin)*1000
                timeList.append(t)
                hopeList.append(len(answer[0]))
                lengthLits.append(answer[1])
        
        print("Average Dijkstra length: ", mean(lengthLits))
        return mean(timeList), mean(lengthLits), mean(hopeList)
    
    def AStarTester(self, file):
        length = len(self.nodes)
        nodesList = self.nodes.values()
        nodesList = list(nodesList)
        timeList = []
        lengthLits = []
        hopeList = []
        for i in range(length):
            for j in range (length):
                if j==i:
                    continue
                begin = time.perf_counter()
                answer = self.AStar(file,nodesList[i],nodesList[j])
                end =time.perf_counter() 
                t = ((end - begin)*1000) - answer[2]
                timeList.append(t)
                hopeList.append(len(answer[0]))
                lengthLits.append(answer[1])
        
        print("Average A* length: ", mean(lengthLits))
        return mean(timeList), mean(lengthLits), mean(hopeList)

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
    
    # firstNode = g.nodes["Zerind"]
    # secondNode = g.nodes["Urziceni"]
    # print(g.bfs(firstNode, secondNode))
    # print(g.dfs(firstNode, secondNode))
    # print(g.dijkstra(firstNode, secondNode))
    # print(g.AStar("position.txt" ,firstNode, secondNode))
    # g.bfsTester()
    # g.dfsTester()
    # print(g.dijkstraTester())
    # print(g.AStarTester("position.txt"))
    
# Initializer(fileName="graph.txt")
