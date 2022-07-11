import random

class Item:
	def __init__(self, name, size, value) -> None:
		self.name = name   #string
		self.size = size  #float
		self.value = value  #int
class Combination:
	def __init__(self, popList, value) -> None:
		self.popList = popList
		self.value = value
	

class GeneticAlgorithm:
	
	def __init__(self, size) -> None:
		self.items = []
		self.sizeLimit = size
		self.crossoverThreshold = 0.35
		self.mutationThreshold = 0.25
		self.iterationLimit = 100
		self.populationList = []
		# self.bestCombo = []
		self.i = 0 
		
	def addItem(self, item):
		if not isinstance(item, Item):
			raise Exception("not instantiated")
		self.items.append(item)

	def startPopulationList(self):
		for i in range(4):
			a =	self.getRandom()
			b = Combination(a, self.getFitness(a))
			self.populationList.append(b)
			# print(a)

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
		for i in range(len(self.items)):
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

	# def getAllFitnesses(self, sample):
	# 	d = {}
	# 	for item in sample:
	# 		d[item] = self.getFitness(item)
	# 	return d

	def change(self, value):
		if (value == 0):
			return 1
		else:
			return 0

	def crossover(self, combination1, combination2):
		for i in range(len(self.items)):
			crossoverChecker = random.uniform(0.0,1.0)
			if crossoverChecker < self.crossoverThreshold:
				combination1.popList[i], combination2.popList[i] = combination2.popList[i], combination1.popList[i]
				combination1.value = self.getFitness(combination1.popList)
				combination2.value = self.getFitness(combination2.popList)
		return combination1, combination2
	
	def mutate(self, combination):
		for i in range(len(self.items)):
			mutationChecker = random.uniform(0.0,1.0)
			if mutationChecker < self.mutationThreshold:
				combination.popList[i] = self.change(combination.popList[i])
				combination.value = self.getFitness(combination.popList)
		return combination

	def betterSolution(self, popList):
		c = popList[0]
		value = 0
		for combo in popList:
			if combo.value > value:
				value = combo.value
				c = combo
		return c
	
	def generateNewPopulation(self, popList):
		tempList = []

		best1 = self.betterSolution(popList)
		tempList.append(best1)
		popList.remove(best1)
		best2 = self.betterSolution(popList)
		tempList.append(best2)

		best3, best4 = self.crossover(best1, best2)
		best3 = self.mutate(best3)
		best4 = self.mutate(best4)
		
		tempList.append(best1)
		tempList.append(best2)

		return tempList
		# bad1 = self.worseSolution(popList2)
		# popList.remove(bad1)

		# selector = self.getAllFitnesses(popList)
		# values = list(selector.values())
		# values.sort()
		# values.reverse()

		# selectorSorted = []
		# for value in values:
		# 	for key in selector.keys():
		# 		if selector[key] == value:
		# 			selectorSorted.append(key)
		# 			break

		# a, b = self.crossover(selectorSorted[0], selectorSorted[1])
		# a = self.mutate(a)
		# b = self.mutate(b)
		# tempList.append(a)
		# tempList.append(b)
		
		# c, d = self.crossover(selectorSorted[0], selectorSorted[2])
		# c = self.mutate(c)
		# d = self.mutate(d)
		# tempList2 = []
		# tempList2.append(c)
		# tempList2.append(d)
		# e = self.betterSolution(tempList2)
		# tempList.append(e)

		# return tempList
		
	def findOptimum(self):
		for i in range(self.iterationLimit):
			# currentCombo = self.getRandom()
			# nextCombo = self.getRandom()
			self.populationList = self.generateNewPopulation(self.populationList)
			# nextCombo = self.mutate(nextCombo)
			# betterCombo = self.betterSolution(currentCombo, nextCombo)

		# return self.betterSolution(self.populationList), self.getFitness(self.betterSolution(self.populationList))
		finalCombo = self.betterSolution(self.populationList)
		return finalCombo.popList, finalCombo.value, self.getSize(finalCombo.popList)

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
			b = Item(lineInfo[0], float(lineInfo[1]), int(lineInfo[2]))
			a.addItem(b)

	a.startPopulationList()
	print(a.findOptimum())

Initializer("10items.txt")

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