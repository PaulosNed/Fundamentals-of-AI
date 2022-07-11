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
		self.mutationThreshold = 0.35
		self.iterationLimit = 100
		self.best = {}
	
	def addItem(self, item):
		if not isinstance(item, Item):
			raise Exception("not instantiated")
		self.items.append(item)	
		self.best[item.name] = 0

	def getPopulation(self):
		temp = []
		for i in range(16):
			a = self.getRandom()
			temp.append(a)
		self.bestCombo = temp
	
	def defineSelector(self, itemsList):
		l = []
		for item in itemsList:
			v = item.value/ item.size
			for i in range(int(v)):
				l.append(item)
		return l

	def getRandom(self):
		randomSelection = []
		tempSize = 0
		domain = self.defineSelector(self.items)
		amountTracer = {}
		while(True):
			selection = random.choice(domain)
			if selection not in amountTracer.keys():
				amountTracer[selection] = 3
			if tempSize + selection.size > self.sizeLimit:
				break
			if amountTracer[selection] == 0:
				continue
			tempSize += selection.size
			amountTracer[selection] -= 1
			randomSelection.append(selection)
		return randomSelection
		
	def getSize(self, combination):
		size = 0
		for item in combination:
			size += item.size
		return size

	def getFitness(self, combination):
		size = self.getSize(combination)
		if size > self.sizeLimit:
			return 0

		value = 0
		for item in combination:
			value += item.value
		return value

	def change(self, value):
		new = random.choice(self.items)
		if new == value:
			return self.change(value)
		return new
	
	def copy(self, combination):
		d = []
		for i in range(len(combination)):
			d.append(combination[i])
		return d

	def crossover(self, combination1, combination2):
		combo1 = self.betterSolution(combination1, combination2)
		if combo1 == combination1:
			combo2 = combination2
		else:
			combo2 = combination1
		length = 0
		if len(combo1) < len(combo2):
			length = len(combo1)
		else:
			length = len(combo2)

		for i in range(length):
			# crossoverChecker = random.uniform(0.0,1.0)
			if combo1[i].value < combo2[i].value:
				combo1[i], combo2[i] = combo2[i], combo1[i]
				if len(self.validate(combo1))!=0 or len(self.validate(combo2))!=0:
					combo1[i], combo2[i] = combo2[i], combo1[i]
		return combo1, combo2
	
	def mutate(self, combination):
		for i in range(len(combination)):
			selector = self.defineSelector(combination)
			comparer = random.choice(selector)
			# mutationChecker = random.uniform(0.0,1.0)
			if combination[i].value / combination[i].size < comparer.value/comparer.size:
				combination[i] = comparer
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

		return minPopulation

	def selectionList(self, popList):
		l = []
		for lists in popList:
			length = self.getFitness(lists)//10
			for i in range(length):
				l.append(lists)
		return l

	def findOptimum(self):
		for i in range(self.iterationLimit):
			current = []
			parent1, parent2=  self.BestCombinations(self.bestCombo)
			current.append(parent1)
			current.append(parent2)
			selectionList = self.selectionList(self.bestCombo)
			for i in range(7):
				parent3, parent4 = random.sample(selectionList, 2)
				parent3, parent4 = self.crossover(parent3, parent4)
				self.mutate(parent3)
				self.mutate(parent4)
				current.append(parent3)
				current.append(parent4)
			self.bestCombo = current
			random.shuffle(self.bestCombo)

		best = self.BestCombinations(self.bestCombo)[1]

		for item in best:
			self.best[item.name]+=1

		return self.best, self.getFitness(best), self.getSize(best)
	
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
	# a.GATester()

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