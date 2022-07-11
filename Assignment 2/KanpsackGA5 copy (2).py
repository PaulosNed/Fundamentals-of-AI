import copy
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
		# self.crossoverThreshold = 0.5
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

	def crossover(self, combination1, combination2):
		combo1 = self.copy(combination1)
		combo2 = self.copy(combination2)
		length = 0
		if len(combo1) < len(combo2):
			length = len(combo1)
		else:
			length = len(combo2)

		for i in range(length):
			if combo1[i].value < combo2[i].value:
				combo1[i], combo2[i] = combo2[i], combo1[i]
				if self.getFitness(combo1) == 0 or self.getFitness(combo2)==0:
					combo1[i], combo2[i] = combo2[i], combo1[i]
			# crossoverChecker = random.uniform(0.0,1.0)
			# if crossoverChecker < self.crossoverThreshold:
			# 	combo1[i], combo2[i] = combo2[i], combo1[i]
		return combo1, combo2
	
	def mutate(self, combination):
		for i in range(len(combination)):
			mutationChecker = random.uniform(0.0,1.0)
			if mutationChecker < self.mutationThreshold:
				a = copy.copy(combination[i])
				combination[i] = self.change(combination[i])
				if self.getFitness(combination) == 0:
					combination[i] = a
		return combination
	
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

		# index3 = val.index(max(val))
		# minPopulation.append(li[index3])
		# val.pop(index3)
		# li.pop(index3)

		# index4 = val.index(max(val))
		# minPopulation.append(li[index4])
		# val.pop(index4)
		# li.pop(index4)

		# index5= val.index(max(val))
		# minPopulation.append(li[index5])
		# val.pop(index5)
		# li.pop(index5)

		# index6 = val.index(max(val))
		# minPopulation.append(li[index6])
		# val.pop(index6)
		# li.pop(index6)

		# index7 = val.index(max(val))
		# minPopulation.append(li[index7])
		# val.pop(index7)
		# li.pop(index7)

		# index8 = val.index(max(val))
		# minPopulation.append(li[index8])
		# val.pop(index8)
		# li.pop(index8)

		return minPopulation
	def CombinationSelector(self, combination):
		selector = []
		for item in combination:
			v = self.getFitness(item)
			for i in range(v):
				selector.append(combination.index(item))
		return selector


	def findOptimum(self):
		domain = self.CombinationSelector(self.bestCombo)
		for i in range(self.iterationLimit):
			domain = self.CombinationSelector(self.bestCombo)
			tempCombo = []
			parent1, parent2 =  self.BestCombinations(self.bestCombo)
			tempCombo.append(parent1)
			tempCombo.append(parent2)
			indic = random.sample(domain, 14)
			restOfParents = []
			for index in indic:
				restOfParents.append(self.bestCombo[index])
			for i in range(7):
				tempP1, tempP2 = random.sample(restOfParents, 2)
				tempP1, tempP2 = self.crossover(tempP1, tempP2)
				self.mutate(tempP1)
				self.mutate(tempP2)
				tempCombo.append(tempP1)
				tempCombo.append(tempP2)

			self.bestCombo = tempCombo	
			
		best = self.BestCombinations(self.bestCombo)[0]
		for item in self.bestCombo:
			print(self.getFitness(item))
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