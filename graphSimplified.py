class Node:
    
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class Edge:

    def __init__(self, name, node1, node2, weight):
        self.name = name
        self.node1 = node1
        self.node2 = node2
        self.weight = weight


class Graph:
    def __init__(self):
        self.nodes=[]
        self.edges = []
        self.neighbouringNodes = {}

    
    def add_node(self, node):
        if not isinstance(node, Node):
            node = Node(node)
        if node.name not in self.nodes:
            self.nodes.append(node.name)
            self.neighbouringNodes[node.name] = []
        
    def add_edge(self, name, node1, node2, weight = 1):
        if isinstance(node1, Node) and isinstance(node2, Node):
            e = Edge(name, node1, node2, weight)
            self.edges.append(e.name)

            if node1.name in self.nodes and node2.name in self.nodes:
                self.neighbouringNodes[node1.name].append(node2.name)
                self.neighbouringNodes[node2.name].append(node1.name)
            else:
                raise Exception("please add the nodes to the graph first!!")

        else:
            raise Exception("Please initialize the nodes first!!")

    def getGraph(self):
        print("Nodes: ", self.nodes, "\n\n")
        print("Edges: ", self.edges, "\n\n")
        print("List of corresponding neighbouring nodes: ", self.neighbouringNodes, "\n\n")

    def bfs(self, startingNode):
        if isinstance(startingNode, Node):
            visited = []
            queue = [startingNode.name]
            while queue:
                if queue[0] in visited:
                    queue.pop(0)
                    continue
                visited.append(queue[0])
                for queueItems in self.neighbouringNodes[queue[0]]:
                    queue.append(queueItems)
                queue.pop(0)
            print("completed succesfully\n", visited)
        else:
            raise Exception("Please enter an intiated and added starting node!!")

    def dfs(self, startingNode):
        if isinstance(startingNode, Node):
            visited = []
            stack = [startingNode.name]
            while stack:
                poped = stack.pop()
                if poped in visited:
                    continue
                visited.append(poped)
                for stackItems in self.neighbouringNodes[poped]:
                    stack.append(stackItems)
            print("completed succesfully\n", visited, "\n\n", stack)
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

x = Node("node1")
y = Node("node2")
z = Node("node3")
p = Node("node4")
r = Node("node5")

g.add_node(x)
g.add_node(y)
g.add_node(z)
g.add_node(p)
g.add_node(r)

g.add_edge("edge1", x, y)
g.add_edge("edge2", x, z)
g.add_edge("edge3", y, z)
g.add_edge("edge4", p, z)
g.add_edge("edge5", p, r)

# g.getGraph()
g.to_aj_matrix()
# g.dfs(r)

