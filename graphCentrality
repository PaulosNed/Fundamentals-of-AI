import math

class Node:
    
    def __init__(self, name):
        self.name = name

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
                if a not in self.positonOfNodes.keys():
                    radA = (float(lineInfo[1]) * math.pi) / 180
                    radB = (float(lineInfo[2]) * math.pi) / 180
                    self.positonOfNodes[a] = (radA, radB)
            else:
                raise Exception("node doesn't exist")

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
                    temp = targetNode
                    while(temp != startingNode):
                        path.append(adjacentsList[temp].name)
                        temp = adjacentsList[temp]
                    path.reverse()
                    return path
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
                    while(temp != startingNode):
                        path.append(adjacentsList[temp].name)
                        temp = adjacentsList[temp]
                    path.reverse()
                    return path
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
        print("Total Cost: \t", distance[targetNode])
        return path
        
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
                    heuristic[neighbour] = 6371.01 * math.acos(math.sin(self.positonOfNodes[neighbour][0])*math.sin(self.positonOfNodes[targetNode][0]) + math.cos(self.positonOfNodes[neighbour][0])*math.cos(self.positonOfNodes[targetNode][0])*math.cos(self.positonOfNodes[targetNode][1] - self.positonOfNodes[neighbour][1]))
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
        print("Total Cost: \t", distance[targetNode])
        return path

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
    
    # g.getGraph()
    firstNode = g.nodes["Oradea"]
    secondNode = g.nodes["Vaslui"]
    print(g.bfs(firstNode, secondNode))
    print(g.dfs(firstNode, secondNode))
    print(g.dijkstra(firstNode, secondNode))
    print(g.AStar("position.txt" ,firstNode, secondNode))
    
Initializer(fileName="graph.txt")
