import math
import random

import time as t
from timeit import timeit


import random
import copy


class Node:
    def __init__(self):
        self.node = None
        self.adjecency_list = []

    def get_adjecencyList(self):
        return self.adjecency_list


class Edge:
    def __init__(self, start, end, weight=0):
        self.start = start
        self.end = end
        self.weight = weight

    def get_edge(self):
        edge = (self.start, self.end, self.weight)

        return edge

    def get_weight(self):
        return self.weight


class Graph:

    def __init__(self):
        self.nodeList = []

        self.dict = {}
        self.edge_list = []
        self.heuristicdis = {}
        self.heuristicValue = {}

    def undirected_graph(self, EdgeL):
        for start, end, weight in EdgeL:
            self.dict.setdefault(start, []).append((weight, end))
            self.dict.setdefault(end, []).append((weight, start))

        return self.dict

    def directed_graph(self, EdgeL):
        for start, end, weight in EdgeL:
            self.dict.setdefault(start, []).append((weight, end))

        return self.dict

    def get_connections(self, node):
        connections=[]
        for weight,no in self.dict[node]:
            connections.append(no)

        return connections

    def display_graph(self):
        print(self.dict)

    def add_edge(self, start, end, weight=1):
        edge = Edge(start, end, weight)
        edge = edge.get_edge()
        if start in self.nodeList:
            if end in self.nodeList:
                self.edge_list.append(edge)

        return self.dict

    def get_nodeList(self):
        return self.nodeList

    def add_node(self, node):

        self.nodeList.append(node)
        self.dict[node] = []

        return self.nodeList

    def read_HeuristicsData(self, Heursiticfile):

        with open(Heursiticfile) as graphData:
            lines = graphData.readlines()
            for line in lines:
                line = line.split()

                Latitude = line[1]
                Longitude = line[2]
                self.heuristicdis[line[0]] = [(Latitude, Longitude)]
        return self.heuristicdis
    def DFS(self, start):
        track_stack = []
        track_stack.append(start)
        isVisited = {}
        path = []
        path.append(start)

        for node in self.nodeList:
            isVisited[node] = False
        while track_stack:
            current_node = track_stack.pop()
            if current_node not in path :
                path.append(current_node)
            isVisited[current_node] = True
            for weight, neighbour in self.dict[current_node]:
                if isVisited[neighbour] == False:
                    track_stack.append(neighbour)

        return path
    def Population(self):
        '''This fuction will generate a  list population
        with the size of the node list '''
        Map=[]
        # plist=copy.copy(self.nodeList)
        # # print(plist)
        # for i in range(len(self.nodeList)):
        #     rl=random.sample(plist, len(plist))
        #     # print(rl)
        #     if rl not in Map:
        #         Map.append(rl)
        for i in self.nodeList:
            l=self.DFS(i)
            Map.append(l)
        return Map
    def fitness_value(self,chromosome_list):
        '''This fuction wiill return the fitness value of a chromesome
        using the euclidean distance'''
        chrfit=[]
        for i in range(len(chromosome_list)-1):
          #get the list that contains the latitude and longitude value of the node
          divalueA=self.heuristicdis[chromosome_list[i]]
          if chromosome_list!=[]:
            divalueB = self.heuristicdis[chromosome_list[i+1]]
          #get latitude and longitude
          lattitudeA=divalueA[0][0]

          longitudeA=divalueA[0][1]
          lattitudeB=divalueB[0][0]
          longitudeB=divalueB[0][1]
          #claculate the distance between the node and the node next to it using Euclidian distance
          if chromosome_list[i+1] in self.get_connections(chromosome_list[1]):
              fitness= math.sqrt(
                        (float( longitudeB) - float( longitudeA)) ** 2 + (float(lattitudeB) - float(lattitudeA)) ** 2)
          else:
              fitness = math.sqrt(
                  (float(longitudeB) - float(longitudeA)) ** 2 + (float(lattitudeB) - float(lattitudeA)) ** 2)+10
          #appennd the distance
          chrfit.append(fitness)
          #sum the distance between nodes to get the distance of the hole chromosome
        return sum(chrfit)
    def selection(self,population):
        '''Selects two chromosoms from the population using their fitness value as
         heuristics'''
        #stores the map of fitnessvalue-> chromosome
        fitValue={}
        #stores the fitness value of each chormosome
        checkfitness=[]
        #stores the two chromosomes selected from the population
        fit=[]
        for chromosome_list in population:
            fitValuenum=self.fitness_value(chromosome_list)
            # print(fitValuenum)
            fitValue[fitValuenum]=chromosome_list
            checkfitness.append(fitValuenum)
        checkfitness.sort()
        fit1=checkfitness[0]
        fit2=checkfitness[1]
        fit.append(fitValue[fit1])
        # print("fit1")
        # print(fit1)
        fit.append(fitValue[fit2])
        # print("fit1")
        # print(fit2)
        return fit
    def cross_over(self,selected):
        '''generates two children from the selected parents'''
        # #for creating child 1
        # parent1=selected[0]
        # print(parent1)
        # parent2=selected[1]
        # print(parent2)
        child1=[]
        child2=[]
        parent1 = selected[0]
        print(parent1)
        index=len(parent1)%2


        parent2 = selected[1]
        # child1.append(parent1[0])
        # for i in range(len(parent1)//2):
        #     if parent1[i] not in  child1:
        #         child1.append(parent1[i])
        # for j in range(len(parent2)):
        #     if parent2[j] not in child1 and parent2[j] in self.get_connections(child1[-1]):
        #         child1.append(parent2[j])
        #
        #     elif parent2[j] not in child1:
        #         child1.append(parent2[j])
        #     if len(child1)==len(parent2):
        #         break
        #
        # # for j in range(len(child1)-1):
        # #     if child1[j+1] not in self.get_connections(child1[j]):
        # #         for i in child1:
        # #             if i in self.get_connections(child1[j]) and i not in child1:
        # #                 child1[j+1]=i
        # for g in range(len(parent2)//2):
        #     if parent2[g] not in  child2:
        #         child2.append(parent2[g])
        # for h in range(len(parent1)):
        #     if parent1[h] not in child2:
        #         child2.append(parent2[h])
        #     if len(child2)==len(parent1):
        #         break

        listOfChildren=[]

        # for i in range(len(parent1)//2):
        #     child1.append(parent1[i])
        # # for gene in range(len(parent2)//2,(len(parent2))):
        # #     child1.append(gene)
        # for j in range(len(parent2)//2):
        #     child2.append(parent1[i])
        # # for gene2 in range(len(parent1)//2,(len(parent1)-1)):
        # #     child2.append(gene2)
        # for num in range(len(parent2)-1):
        #     index=len(child1)-2
        #     if child2[index] !=parent2[num]:
        #         child1.append(parent2[num])


        # child1.append(parent1[4])
        # global h
        #
        # for h in range(len(parent1)):
        #
        #     if parent1[h] in self.get_connections(child1[-1]) and parent1[h] not  in child1:
        #         child1.append(parent1[h])
        #         h=0
        #     # elif parent1[h] in self.get_connections(child1[0]) and parent1[h] not  in child1:
        #     #     child1.insert(0,parent1[h])
        #     #     h=0
        #
        #     # if len(child1)==(len(parent1)//2):
        #     #     break
        # global g
        #
        #
        # for g in range(len(parent2)):

        listOfChildren.append(child1)

        listOfChildren.append(child2)
        return listOfChildren
    def Mutuation(self):
        tobemut=self.cross_over(self.selection(self.Population()))
    def hil_climbing(self):
        path=[self.nodeList[0]]

        for i in range(len(self.nodeList)):
            if self.nodeList[i] in self.get_connections(path[-1]) and self.nodeList[i] not in path:
                path.append(self.nodeList[i])
        print(path)
    # def simulated_annealing(self):
    #     start=random.choice(self.nodeList)
    #     solution=self.DFS(start)
    #     cost=self.fitness_value(solution)
    #     start = random.choice(self.nodeList)
    #     solution2=self.DFS(start)
    #     cost2 = self.fitness_value(solution2)
    #     if cost
















def graph_from_file(graph, file):
    with open(file) as graphData:
        lines = graphData.readlines()
        for line in lines:
            line = line.split()
            if line[0] not in graph.nodeList:
                graph.add_node(line[0])
            if line[1] not in graph.nodeList:
                graph.add_node(line[1])
            graph.add_edge(line[0], line[1], line[2])
gr=Graph()
graph_from_file(gr,'graphData.txt')

gr.undirected_graph(gr.edge_list)
start=random.choice(gr.nodeList)

#
# print(gr.DFS(start))


gr.read_HeuristicsData('HeuristicsData.txt')
print(gr.selection(gr.Population()))







