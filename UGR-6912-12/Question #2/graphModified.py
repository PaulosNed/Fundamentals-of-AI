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

    def getGraph(self):
        print("\n\nNodes: " , list(self.nodes.keys()) , "\n\n")
        di2 = {}
        for edgeKey in self.edgesOfNode.keys():
            temp = edgeKey
            di2[(temp[0].name, temp[1].name)] = self.edgesOfNode[edgeKey].name
        print("edges: ", list(di2.values()) ,"\n\n")
        print("edges connecting the nodes: ", di2 ,"\n\n")
        di = {}
        for key in self.neighbouringNodes.keys():
            li2 = []
            for item in self.neighbouringNodes[key]:
                li2.append(item.name) 
            di[key.name] = li2
        print("Nodes with their neighbors: ", di ,"\n\n")

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
    
    g.getGraph()
    
Initializer(fileName="graph.txt")