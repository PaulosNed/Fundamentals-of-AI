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
		self.crossoverThreshold = 0.005
		self.mutationThreshold = 0.0015
		self.iterationLimit = 10000
		self.bestCombo = []
	
	def addItem(self, item):
		if not isinstance(item, Item):
			raise Exception("not instantiated")
		self.items.append(item)	

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

	def change(self, value):
		if (value == 0):
			return 1
		else:
			return 0
	def crossover(self, combination1, combination2):
		for i in range(len(combination1)):
			crossoverChecker = random.uniform(0.0,1.0)
			if crossoverChecker < self.crossoverThreshold:
				combination1[i], combination2[i] = combination2[i], combination1[i]
		return combination1, combination2
	
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

	def findOptimum(self):
		for i in range(self.iterationLimit):
			currentCombo = self.getRandom()
			nextCombo = self.getRandom()
			currentCombo, nextCombo = self.crossover(currentCombo, nextCombo)
			currentCombo = self.mutate(currentCombo)
			nextCombo = self.mutate(nextCombo)
			betterCombo = self.betterSolution(currentCombo, nextCombo)

			if self.getFitness(betterCombo) > self.getFitness(self.bestCombo):
				self.bestCombo = betterCombo
			
		
		best = []
		bestValue = 0
		bestSize = 0
		for i in range(len(self.bestCombo)):
			if self.bestCombo[i] == 1:
				best.append(self.items[i].name)
				bestValue += self.items[i].value
				bestSize += self.items[i].size		
		return best, bestValue, bestSize


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
			print(lineInfo[1])
			b = Item(lineInfo[0], float(lineInfo[1]), int(lineInfo[2]))
			a.addItem(b)

	print(a.findOptimum())

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

# print(a.findOptimum())