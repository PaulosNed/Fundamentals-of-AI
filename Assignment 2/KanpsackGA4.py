import math
import random
from statistics import mean
import time

class Item:
	def __init__(self, name, size, value) -> None:
		self.name = name   #string
		self.size = size  #float
		self.value = value  #int

class GeneticAlgorithm:
	def __init__(self, size) -> None:
		self.items = []
		self.sizeLimit = size
		self.crossoverThreshold = 0.5
		self.mutationThreshold = 0.25
		self.iterationLimit = 100
	
	def addItem(self, item):
		if not isinstance(item, Item):
			raise Exception("not instantiated")
		self.items.append(item)	

	def getPopulation(self):
		temp = []
		for i in range(16):
			a = self.getRandom()
			temp.append(a)
		self.bestCombo = temp

	def getRandom(self):
		randomSelection2 = []
		for i in range(len(self.items)):
			randomSelection2.append(random.choice([0,1]))
		return randomSelection2
		
	def getSize(self, combination):
		size = 0
		for i in range(len(combination)):
			if combination[i]==1:
				size += self.items[i].size
		return size

	def getFitness(self, combination):
		size = self.getSize(combination)
		if size > self.sizeLimit:
			return 0

		value = 0
		for i in range(len(combination)):
			if combination[i]==1:
				value += self.items[i].value
		return value

	def getValue(self, combination):
		size = self.getSize(combination)
		if size > self.sizeLimit:
			return 0

		value = 0
		for i in range(len(combination)):
			if combination[i]==1:
				value += self.items[i].value
		return value


	def change(self, value):
		if (value == 0):
			return 1
		else:
			return 0
	
	def copy(self, combination):
		d = []
		for i in range(len(combination)):
			d.append(combination[i])
		return d

	def crossover(self, combination1, combination2):
		combo1 = self.copy(combination1)
		combo2 = self.copy(combination2)
		for i in range(len(self.items)):
			crossoverChecker = random.uniform(0.0,1.0)
			if crossoverChecker < self.crossoverThreshold:
				combo1[i], combo2[i] = combo2[i], combo1[i]
		return combo1, combo2
	
	def mutate(self, combination):
		for i in range(len(combination)):
			mutationChecker = random.uniform(0.0,1.0)
			if mutationChecker < self.mutationThreshold:
				combination[i] = self.change(combination[i])
		return combination
	
	def betterSolution(self, combination1, combination2):
		combo1Value = self.getFitness(combination1)
		combo2Value = self.getFitness(combination2)

		if combo1Value>combo2Value:
			return combination1
		else:
			return combination2
	
	def BestCombinations(self, popList):
		li = self.copy(popList)
		minPopulation = []
		val = []
		for item in li:
			val.append(self.getFitness(item))
		
		index = val.index(max(val))
		minPopulation.append(li[index])
		val.pop(index)
		li.pop(index)

		index2 = val.index(max(val))
		minPopulation.append(li[index2])
		val.pop(index2)
		li.pop(index2)

		index3 = val.index(max(val))
		minPopulation.append(li[index3])
		val.pop(index3)
		li.pop(index3)

		index4 = val.index(max(val))
		minPopulation.append(li[index4])
		val.pop(index4)
		li.pop(index4)

		index5= val.index(max(val))
		minPopulation.append(li[index5])
		val.pop(index5)
		li.pop(index5)

		index6 = val.index(max(val))
		minPopulation.append(li[index6])
		val.pop(index6)
		li.pop(index6)

		index7 = val.index(max(val))
		minPopulation.append(li[index7])
		val.pop(index7)
		li.pop(index7)

		index8 = val.index(max(val))
		minPopulation.append(li[index8])
		val.pop(index8)
		li.pop(index8)

		return minPopulation

	def findOptimum(self):
		for i in range(self.iterationLimit):
			parent1, parent2, parent3, parent4, parent5, parent6, parent7, parent8 =  self.BestCombinations(self.bestCombo)
			parent9, parent10 =  self.crossover(parent1, parent2)
			self.mutate(parent9)
			self.mutate(parent10)
			parent11, parent12 =  self.crossover(parent3, parent4)
			self.mutate(parent11)
			self.mutate(parent12)
			parent13, parent14 =  self.crossover(parent5, parent6)
			self.mutate(parent13)
			self.mutate(parent14)
			parent15, parent16 =  self.crossover(parent7, parent8)
			self.mutate(parent15)
			self.mutate(parent16)
			self.bestCombo = [parent1, parent2, parent3, parent4, parent5, parent6, parent7, parent8, parent9, parent10, parent11, parent12, parent13, parent14, parent15, parent16]
		
		a = self.betterSolution(self.bestCombo[0], self.bestCombo[1])
		b = self.betterSolution(self.bestCombo[2], self.bestCombo[3])
		best = self.betterSolution(a,b)

		return best, self.getFitness(best), self.getSize(best)
	
	def GATester(self):
		timeList = []
		values = []
		sizes = []

		for i in range(10):
			begin = time.perf_counter()
			answer = self.findOptimum()
			end = time.perf_counter()
			t = (end - begin) * 1000
			timeList.append(t)
			values.append(answer[1])
			sizes.append(answer[2])
		print("\nAverage time, value and size of Genetic a;gprothm when 20 items: ", mean(timeList),",", mean(values),",", mean(sizes), "\n")
			

def Initializer(fileName):
	wholeInfo = open(fileName, "r")
	index = 0
	for line in wholeInfo.readlines():
		if index==0:
			a = GeneticAlgorithm(int(line))
			index+=1
		elif index==1:
			index+=1
			continue
		else:
			lineInfo = line.split(",")
			# print(lineInfo[1])
			b = Item(lineInfo[0], float(lineInfo[1]), int(lineInfo[2]))
			a.addItem(b)
	a.getPopulation()
	print(a.findOptimum())
	a.GATester()

Initializer("20items.txt")

# x= Item("x", 5, 6)
# y= Item("y", 15, 10)
# z= Item("z", 1, 10)
# w= Item("w", 2, 2)
# p= Item("p", 9, 8)
# q= Item("q", 3, 3)
# r= Item("r", 2, 1)
# s= Item("s", 7, 20)

# a = GeneticAlgorithm(42)

# a.addItem(x)
# a.addItem(y)
# a.addItem(z)
# a.addItem(w)
# a.addItem(p)
# a.addItem(q)
# a.addItem(r)
# a.addItem(s)

# a.getPopulation()
# print(a.findOptimum())