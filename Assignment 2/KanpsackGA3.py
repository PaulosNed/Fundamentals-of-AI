import math
import random

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
		self.bestCombo = self.getPopulation()
	
	def addItem(self, item):
		if not isinstance(item, Item):
			raise Exception("not instantiated")
		self.items.append(item)	

	def getPopulation(self):
		temp = []
		for i in range(4):
			a = self.getRandom()
			temp.append(a)
		self.bestCombo = temp

	def getRandom(self):
		randomSelection = random.sample(range(0, len(self.items)), len(self.items))
		tempSize = 0
		validList = [0] * len(self.items)
		for selection in randomSelection:
			if tempSize + self.items[selection].size > self.sizeLimit:
				break
			tempSize += self.items[selection].size
			validList[selection] = 1
		return validList
		
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

		return minPopulation

	def findOptimum(self):
		for i in range(self.iterationLimit):
			parent1, parent2 =  self.BestCombinations(self.bestCombo)
			# ran = random.sample(self.bestCombo, 2)
			parent3, parent4 =  self.crossover(parent1, parent2)
			self.mutate(parent3)
			self.mutate(parent4)
			self.bestCombo = [parent1, parent2, parent3, parent4]
		
		a = self.betterSolution(self.bestCombo[0], self.bestCombo[1])
		b = self.betterSolution(self.bestCombo[2], self.bestCombo[3])
		best = self.betterSolution(a,b)

		return best, self.getFitness(best), self.getSize(best)
			

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

Initializer("15items.txt")

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