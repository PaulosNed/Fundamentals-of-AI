import math
import random
import sys
import time

import time
# from timeit import timeit


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

    def get_distance(self, start,end):
        enddis = self.heuristicdis[end]

        for lat, long in self.heuristicdis[start]:
            distance = math.sqrt(
                    (float(long) - float(enddis[0][0])) ** 2 + (float(lat) - float(enddis[0][1])) ** 2)
        return distance
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
    def Population(self,generation):
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
        for i in range(10):
            l=self.DFS(generation[i])
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
    def cross_over(self,parent1,parent2):
        '''generates two children from the selected parents'''
        # #for creating child 1
        # parent1=selected[0]
        # print(parent1)
        # parent2=selected[1]
        # print(parent2)
        child1=[]
        child2=[]

        print(parent1)
        # index=len(parent1)//2
        print(parent2)

        for i in range(len(parent1)//2):
            child1.append(parent1[i])
        for i in range((len(parent2)//2),(len(parent2)//2)+4):
            child1.append(parent2[i])
        for i in range((len(parent1)//2)+4,len(parent1)-1):
            child1.append(parent1[i])
        #for child2
        for j in range(len(parent2)//2):
            child2.append(parent2[j])
        for j in range((len(parent1)//2),(len(parent1)//2)+4):
            child2.append(parent1[j])
        for j in range((len(parent2)//2)+4,len(parent2)-1):
            child2.append(parent2[j])












        listOfChildren=[]
        print("child1")
        print(child1)
        print("child2")
        print(child2)



        listOfChildren.append(child1)

        listOfChildren.append(child2)
        return listOfChildren
    def Mutuation(self,crossoverValue):
        fit1=self.fitness_value(crossoverValue[0])
        fit2 = self.fitness_value(crossoverValue[1])
        print("p1")
        print(crossoverValue[0])
        print("p2")
        print(crossoverValue[1])
        global toMutuate
        if fit1 > fit2:
            toMutuate=crossoverValue[1]
        elif fit1 <fit2:
            toMutuate=crossoverValue[0]
        else:
            toMutuate=random.choice(crossoverValue)
        # geneToflip=random.choice(toMutuate)
        # print(geneToflip)
        # flipindex1=toMutuate.index(geneToflip)
        # global flipindex2
        # if flipindex1==toMutuate.index(toMutuate[-1]):
        #     flipindex2=flipindex1-1
        # else:
        #     flipindex2=flipindex1+1
        # toMutuate[flipindex1],toMutuate[flipindex2]=toMutuate[flipindex2],toMutuate[flipindex1]
        # index=toMutuate.index(geneToflip)
        # for i in range(len(toMutuate)-2):
        #     if self.get_distance(geneToflip,toMutuate[i])<self.get_distance(geneToflip,toMutuate[toMutuate.index(geneToflip)+1]):
        #         toMutuate[toMutuate.index(geneToflip)+1], toMutuate[i] = toMutuate[i], toMutuate[toMutuate.index(geneToflip)+1]
        #         print(toMutuate[i])
        toMutuate[4],toMutuate[5]=toMutuate[5],toMutuate[4]
        toMutuate[4],toMutuate[2]=toMutuate[2],toMutuate[4]
        toMutuate[4], toMutuate[3] = toMutuate[3], toMutuate[4]






        return toMutuate
    def Mutuated_generation(self,initgeneration):
        generation=[]
        for i in range(5):
            Population = initgeneration
            selected = self.selection(Population)
            crossOver = self.cross_over(selected[0], selected[1])
            Mutuated = self.Mutuation(crossOver)
            generation.append(Mutuated)
        return generation
    def step_Mututation(self,generation):
        Population =generation
        selected = self.selection(Population)
        crossOver = self.cross_over(selected[0], selected[1])
        Mutuated = self.Mutuation(crossOver)
        return Mutuated
    def Genetic_Algorithm(self):

        # generation0=self.Mutuated_generation(self.Population(self.nodeList))
        # generation1=self.Mutuated_generation(generation0)
        # path1=self.step_Mututation(generation0)
        #
        # path2=self.step_Mututation(generation1)
        # if self.fitness_value(path1)>self.fitness_value(path2):
        #     return path2
        # else:
        #     return path1
        Population =gr.Population(self.nodeList)
        selected = self.selection(Population)
        crossOver = self.cross_over(selected[0], selected[1])
        Mutuated = self.Mutuation(crossOver)
        return Mutuated







    def hill_climbing(self):

        currentSolution=self.generate_solution()
        distance=self.fitness_value(currentSolution)
        next=self.generate_solution()
        distanceNe=self.fitness_value(next)
        while(distanceNe >distance):
            next=self.generate_solution()
            distanceNe=self.fitness_value(next)

        currentSolution=next
        print(currentSolution)
        return currentSolution

    def generate_solution(self):
        start = random.choice(self.nodeList)
        solution = self.DFS(start)
        return solution

    def simulated_annealing(self):
        Initial_Temprature=0.1   #update initial here
        End_Temprature = 0.01
        tempDec=0.002
        e=2.718
        # solution1=self.generate_solution()
        # current_path=solution1
        current_path=self.generate_solution()
        #
        # cost=self.fitness_value(solution1)
        # start = random.choice(self.nodeList)
        # solution2=self.generate_solution()
        # cost2 = self.fitness_value(solution2)
        # if (e**(cost-cost2)/Initial_Temprature)>=1:
        #     current_path=solution2
        #     cost=cost2
        # elif(e**(cost-cost2)/Initial_Temprature)<=0 :
        #     current_path=solution1
        #     return current_path
        temprature = Initial_Temprature
        while temprature > End_Temprature:
            current_energy=self.fitness_value(current_path)
            solution2=self.generate_solution()
            next_energy=self.fitness_value(solution2)
            change_In_energy=next_energy-current_energy
            if (change_In_energy>0):
                current_path=solution2
            elif(e**(change_In_energy/Initial_Temprature)>random.uniform(0, 1)):
                current_path=solution2
            temprature = temprature - (temprature*tempDec)
        print(current_path)
        return current_path

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
# gr=Graph()
# graph_from_file(gr,sys.argv[4])

# gr.undirected_graph(gr.edge_list)
# start=random.choice(gr.nodeList)

#
# print(gr.DFS(start))

# gr.read_HeuristicsData('HeuristicsData.txt')
# print(gr.fitness_value(gr.selection(gr.Population(gr.nodeList))[0]))
# print(gr.Mutuated_generation(gr.Population(gr.nodeList)))
# print(gr.fitness_value(gr.Genetic_Algorithm()))
# start=time.perf_counter()
# print(gr.fitness_value(gr.simulated_annealing()))
# end=time.perf_counter()
# print((end-start)*1000)





def main():
    global gr 
    gr = Graph()
    graph_from_file(gr,sys.argv[4])

    gr.undirected_graph(gr.edge_list)
    start=random.choice(gr.nodeList)
    gr.read_HeuristicsData('HeuristicsData.txt')
    if len(sys.argv)<5:
        print(" please insert the right format  \"python knapsack.py --algorithm ga --file my-file.txt\"")
        return
    else:
        if sys.argv[2]=='ga':
            print(gr.fitness_value(gr.Genetic_Algorithm()))
        elif sys.argv[2]=='hill_climbing':
            print(gr.fitness_value(gr.hill_climbing()))
        elif sys.argv[2]=='simulated_annealing':
            print(gr.fitness_value(gr.simulated_annealing()))
        else:
            print ("please select a from the algotrithm listed below \n ga \n  hill_climbing\n simulated_annealing ")


if __name__=='__main__':
	main()



