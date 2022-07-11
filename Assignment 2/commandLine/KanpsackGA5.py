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
	
	def Validate(self, combination):
		indicies = []
		tracer = {}
		for item in self.items:
			tracer[item] = 0
		
		for item in combination:
			tracer[item] += 1
		for key,value in tracer.items():
			if value > 3:
				indicies.append(key)
		return indicies 

	def getFitness(self, combination):
		size = self.getSize(combination)
		if size > self.sizeLimit:
			return 0
		if len(self.Validate(combination)) != 0:
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

	def crossover(self, listOf2):
		combo1 = self.copy(listOf2[0])
		combo2 = self.copy(listOf2[1])
		length = 0
		if len(combo1) < len(combo2):
			length = len(combo1)
		else:
			length = len(combo2)

		for i in range(length):
			crossoverChecker = random.uniform(0.0,1.0)
			if crossoverChecker < self.crossoverThreshold:
				combo1[i], combo2[i] = combo2[i], combo1[i]
				if self.getFitness(combo1) == 0 or self.getFitness(combo2) == 0:
					combo1[i], combo2[i] = combo2[i], combo1[i]
		return combo1, combo2
	
	def mutate(self, combination):
		for i in range(len(combination)):
			mutationChecker = random.uniform(0.0,1.0)
			if mutationChecker < self.mutationThreshold:
				tempCombo = self.copy(combination)
				combination[i] = self.change(combination[i])
				if self.getFitness(combination) == 0:
					combination[i] = tempCombo[i]
		return combination
	
	def BestCombinations(self, popList):
		li = self.copy(popList)
		minPopulation = []
		val = []
		backup = []
		for item in li:
			val.append(self.getFitness(item))
		
		for i in range (8):
			index = val.index(max(val))
			if li[index] in minPopulation:
				backup.append(li[index])
				val.pop(index)
				li.pop(index)
				continue
			minPopulation.append(li[index])
			val.pop(index)
			li.pop(index)
		i = 0
		while(len(minPopulation)<8):
			minPopulation.append(backup[i])
			i+=1
		return minPopulation

	def findOptimum(self):
		for i in range(self.iterationLimit):
			tempCombo = []
			best8 =  self.BestCombinations(self.bestCombo)
			tempCombo.extend(best8)
			for i in range(4):
				parent9, parent10 =  self.crossover(random.sample(best8, 2))
				self.mutate(parent9)
				self.mutate(parent10)
				tempCombo.append(parent9)
				tempCombo.append(parent10)
				self.bestCombo = tempCombo		
		best = self.BestCombinations(self.bestCombo)[0]
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