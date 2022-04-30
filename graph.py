class Node:
    
    def __init__(self, name):
        self.name = name
        self.edgeList = []

        # for edge in edges:
        #     if not isinstance(edge, Edge):
        #         edge = Edge(edge)
        #     self.edgeList.append(edge.name)

    def add_edges(self, *edges):
        for edge in edges:
            if isinstance(edge, Edge) and self in edge.endpoints:
                self.edgeList.append(edge.name)
            else: 
                raise Exception("Edge does not exist. Please instantiate the edge first!!")


    def __str__(self):
        return self.name

class Edge:

    def __init__(self, name, startNode, endNode, weight = 1):
        self.name = name
        self.weight = weight


        if not isinstance(startNode, Node) and isinstance(endNode,  Node):
            startNode = Node(startNode)
        elif isinstance(startNode, Node) and not isinstance(endNode,  Node):
            endNode = Node(endNode)
        elif not isinstance(startNode, Node) and not isinstance(endNode,  Node):
            startNode = Node(startNode)
            endNode = Node(endNode)



        if self.name not in startNode.edgeList and self.name in endNode.edgeList:
            startNode.edgeList.append(self.name)
        elif self.name in startNode.edgeList and self.name not in endNode.edgeList:
            endNode.edgeList.append(self.name)
        elif self.name not in startNode.edgeList and self.name not in endNode.edgeList:
            startNode.edgeList.append(self.name)
            endNode.edgeList.append(self.name)
        self.endpoints = (startNode, endNode) 


    def __str__(self):
        return self.name

class Graph:
    def __init__(self):
        nodes=[]
        edges = []
        correspondingEdgeList = []


        # for aNode in node:
        #     if not isinstance(aNode, Node):
        #         aNode = Node(aNode) 
        #     if aNode.name not in nodes:
        #         nodes.append(aNode.name)
        #         correspondingEdgeList.append(aNode.edgeList)

    
    def add_node(self, node):
        if not isinstance(node, Node):
            node = Node(node) 
        if node.name not in self.nodes:
            self.nodes.append(node.name)
            self.correspondingEdgeList.append(node.edgeList)

    def add_edge(self, edge):
        if not isinstance(edge, Edge):
            edge = Edge(edge) 
        if edge.name not in self.edges:
            self.edges.append(edge.name)

    def getGraph(self):
        print("Nodes: ", self.nodes, "\n")
        print("List of edges for each corresponding nodes: ", self.correspondingEdgeList, "\n")
        print("Edges: ", self.edges, "\n")



