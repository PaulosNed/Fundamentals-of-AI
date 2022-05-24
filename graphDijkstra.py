from asyncio.windows_events import NULL


class Node:
    
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class Edge:

    def __init__(self, name, node1, node2, weight, directed):
        self.name = name
        self.node1 = node1
        self.node2 = node2
        self.weight = weight
        self.directed = directed

    def __str__(self):
        return self.name


class Graph:
    def __init__(self):
        self.nodes=[]
        self.edges = []
        self.neighbouringNodes = {}
        self.edgesOfNode = {}

    
    def add_node(self, node):
        if not isinstance(node, Node):
            raise Exception("un-initialized node")
        if node not in self.nodes:
            self.nodes.append(node)
            self.neighbouringNodes[node] = []
        
    def add_edge(self, name, node1, node2, weight = 1, directed = False):
        if isinstance(node1, Node) and isinstance(node2, Node):
            e = Edge(name, node1, node2, weight, directed)
            self.edges.append(e)

            if node1 in self.nodes and node2 in self.nodes:
                self.neighbouringNodes[node2].append(node1)
                self.edgesOfNode[(node1, node2)] = e 
                if (e.directed == False):
                    self.neighbouringNodes[node1].append(node2)
            else:
                raise Exception("please add the nodes to the graph first!!")

        else:
            raise Exception("Please initialize the nodes first!!")

    def getGraph(self):
        Nli = []
        Eli = []
        for items in self.nodes:
            Nli.append(items.name) 
        print("Nodes: " , Nli , "\n\n")
        for edges in self.edges:
            Eli.append(edges.name) 
        print("Edges: ", Eli, "\n\n")
        di = {}
        for key in self.neighbouringNodes.keys():
            li2 = []
            for item in self.neighbouringNodes[key]:
                li2.append(item.name) 
            di[key.name] = li2
        print("Nodes with their neighbors: ", di ,"\n\n")
        di2 = {}
        for edgeKey in self.edgesOfNode.keys():
            temp = edgeKey
            di2[(temp[0].name, temp[1].name)] = self.edgesOfNode[edgeKey].name
        print("edges connecting the nodes: ", di2 ,"\n\n")

    def bfs(self, startingNode, targetNode):
        if isinstance(startingNode, Node):
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

    def AStar(self, startingNode, targetNode):
        openList = []
        closedList = []
        f = {}
        disFromA = {startingNode : 0}
        adjacentsList = {}
        path = []
        heuristic = {}
        current = startingNode
        #heuristic of start to target
        f[current] = disFromA[current] + heuristic[current]
        while(current != targetNode):
            for neighbour in self.neighbouringNodes[current]:
                if neighbour not in openList and neighbour not in closedList:
                    openList.append(neighbour)
                    temp = (current, neighbour)
                    if temp not in self.edgesOfNode.keys():
                        temp = (neighbour, current)
                    disFromA[neighbour] = disFromA[current] + self.edgesOfNode[temp].weight
                    # calculate heuristic here
                    tempF = disFromA[neighbour] + heuristic[neighbour]
                    if neighbour not in f.keys() or tempF < f[neighbour]:
                        f[neighbour] = tempF
                        adjacentsList[neighbour] = current
            closedList.append(current)
            openList.remove(current)
            current = min(f, key=f.get)

        last = targetNode
        while(last != startingNode):
            path.append(adjacentsList[last].name)
            last = adjacentsList[last]
        path.reverse()
        return path

    def to_aj_matrix(self):
        mx = []
        for nodeX in self.nodes:
            nodeYs = []
            for nodeY in self.nodes:
                if nodeY in self.neighbouringNodes[nodeX]:
                    nodeYs.append(1)
                    continue
                nodeYs.append(0)
            mx.append(nodeYs)
        print(mx) 

g = Graph()

x = Node("x")
y = Node("y")
z = Node("z")
p = Node("p")
r = Node("r")
s = Node("s")
q = Node("q")
t = Node("t")

g.add_node(x)
g.add_node(y)
g.add_node(z)
g.add_node(p)
g.add_node(r)
g.add_node(s)
g.add_node(q)
g.add_node(t)

g.add_edge("edge1", x, y, 5)
g.add_edge("edge2", x, z, 6)
g.add_edge("edge3", y, z, 7)
g.add_edge("edge4", p, z, 2)
g.add_edge("edge5", p, r, 1)
g.add_edge("edge6", p, q, 3)
g.add_edge("edge7", q, y, 15)
g.add_edge("edge8", x, s, 1)
g.add_edge("edge9", z, s, 4)
g.add_edge("edge10", s, t, 8)
g.add_edge("edge11", t, p, 9)


# g.getGraph()
# g.to_aj_matrix()
print(g.dijkstra(q,x))