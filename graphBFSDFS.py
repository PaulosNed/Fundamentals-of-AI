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


class Graph:
    def __init__(self):
        self.nodes=[]
        self.edges = []
        self.neighbouringNodes = {}

    
    def add_node(self, node):
        if not isinstance(node, Node):
            raise Exception("un-initialized node")
        if node.name not in self.nodes:
            self.nodes.append(node.name)
            self.neighbouringNodes[node.name] = []
        
    def add_edge(self, name, node1, node2, weight = 1, directed = False):
        if isinstance(node1, Node) and isinstance(node2, Node):
            e = Edge(name, node1, node2, weight, directed)
            self.edges.append(e.name)

            if node1.name in self.nodes and node2.name in self.nodes:
                self.neighbouringNodes[node2.name].append(node1.name)
                if (e.directed == False):
                    self.neighbouringNodes[node1.name].append(node2.name)
            else:
                raise Exception("please add the nodes to the graph first!!")

        else:
            raise Exception("Please initialize the nodes first!!")

    def getGraph(self):
        print("Nodes: ", self.nodes, "\n\n")
        print("Edges: ", self.edges, "\n\n")
        print("List of corresponding neighbouring nodes: ", self.neighbouringNodes, "\n\n")

    def bfs(self, startingNode, targetNode):
        if isinstance(startingNode, Node):
            visited = []
            queue = [startingNode.name]
            adjacentsList = {}
            path = [targetNode.name]
            while queue:
                if targetNode.name in queue:
                    temp = targetNode.name
                    while(temp != startingNode.name):
                        path.append(adjacentsList[temp])
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
            stack = [startingNode.name]
            adjacentsList = {}
            path = [targetNode.name]
            while stack:
                if targetNode.name in stack:
                    temp = targetNode.name
                    while(temp != startingNode.name):
                        path.append(adjacentsList[temp])
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

g.add_edge("edge1", x, y)
g.add_edge("edge2", x, z)
g.add_edge("edge3", y, z)
g.add_edge("edge4", p, z)
g.add_edge("edge5", p, r)
g.add_edge("edge6", p, q)
g.add_edge("edge7", q, y)
g.add_edge("edge8", x, s)
g.add_edge("edge9", z, s)
g.add_edge("edge10", s, t)
g.add_edge("edge11", t, p)


g.getGraph()
# g.to_aj_matrix()
# print(g.bfs(x,p))