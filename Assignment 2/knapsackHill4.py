import math
import random
from statistics import mean
import time

#normal generation to current
#generate random neighbor
#if better make neighbor normal and repeat
#else return neighbour

class Item:
	def __init__(self, name, size, value) -> None:
		self.name = name   #string
		self.size = size  #float
		self.value = value  #int

class HillClimbing:
	def __init__(self, size) -> None:
		self.items = []
		self.sizeLimit = size
		self.visited = []
		self.bestCombo = {}
		
	def addItem(self, item):
		if not isinstance(item, Item):
			raise Exception("not instantiated")
		self.items.append(item)
		self.bestCombo[item.name] = 0
		self.current = self.getRandom()
	
	def defineSelector(self, itemsList):
		l = []
		for item in itemsList:
			v = item.value/ item.size
			for i in range(int(v)*2):
				l.append(item)
		return l

	def getRandom(self):
		randomSelection = []
		tempSize = 0
		amountTracer = {}
		domain = self.defineSelector(self.items)
		for i in range(len(domain)):
			selection = random.choice(domain)
			if selection not in amountTracer.keys():
				amountTracer[selection] = 3
			if tempSize + selection.size > self.sizeLimit:
				break
			if amountTracer[selection] == 0:
				continue
			amountTracer[selection]-=1
			tempSize += selection.size
			randomSelection.append(selection)
		return randomSelection

	def copy(self, combination):
		d = []
		for i in range(len(combination)):
			d.append(combination[i])
		return d

	def getValues(self, items):
		value = []
		for item in items:
			value.append(item.value)
		return value

	def betterSolution(self, combination1, combination2):
		combo1Value = self.getValues(combination1)
		combo2Value = self.getValues(combination2)

		if combo1Value>combo2Value:
			return 1
		else:
			return 2

	def getLocalMax(self):
		neighbour = self.getRandom()
		if neighbour in self.visited:
			return self.getLocalMax()
		if self.betterSolution(self.current, neighbour) == 2:
			self.visited.append(self.current)
			self.current = neighbour
			return self.getLocalMax()
		value = 0
		size = 0
		for item in self.current:
			self.bestCombo[item.name] += 1
			value += item.value
			size += item.size

		return self.bestCombo, value, size


	def hillTester(self):
		timeList = []
		values = []
		sizes = []

		for i in range(10):
			begin = time.perf_counter()
			answer = self.getLocalMax()
			end = time.perf_counter()
			t = (end - begin) * 1000
			timeList.append(t)
			values.append(answer[1])
			sizes.append(answer[2])
			
		print("\nAverage time, value and size of Simulated Algorith when 20 items: ", mean(timeList),",", mean(values),",", mean(sizes), "\n")

def Initializer(fileName):
	wholeInfo = open(fileName, "r")
	index = 0
	for line in wholeInfo.readlines():
		if index==0:
			a = HillClimbing(int(line))
			index+=1
		elif index==1:
			index+=1
			continue
		else:
			lineInfo = line.split(",")
			b = Item(lineInfo[0], float(lineInfo[1]), int(lineInfo[2]))
			a.addItem(b)

	print(a.hillTester())

Initializer("20items.txt")