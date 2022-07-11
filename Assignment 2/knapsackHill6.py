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
		self.current = []
		self.bestCombo = {}
		
	def addItem(self, item):
		if not isinstance(item, Item):
			raise Exception("not instantiated")
		self.items.append(item)
		self.bestCombo[item.name] = 0

	def copy(self, combination):
		d = []
		for item in combination:
			d.append(item)
		return d

	def getValues(self, items):
		value = []
		for item in items:
			value.append(item.value)
		return value

	def getSize(self, combination):
		size = 0
		for item in combination:
			size += item.size
		return size

	def findBest(self, itemsList):
		value = 0
		best = None
		for item in itemsList:
			if item.value / item.size > value:
				value = item.value / item.size
				best = item
		return best


	def betterSolution(self, combination1, combination2):
		combo1Value = self.getValues(combination1)
		combo2Value = self.getValues(combination2)

		if combo1Value>combo2Value:
			return 1
		else:
			return 2

	def getLocalMax(self, itemsList):
		tracer = {}
		tracer[self.current[0]] = 2
		neighbour = self.findBest(itemsList)
		weight = self.getSize(self.current)
		while (weight + neighbour.size <= self.sizeLimit):
			if neighbour in tracer.keys() and tracer[neighbour] == 0:
				break
			self.current.append(neighbour)
			if neighbour not in tracer.keys():
				tracer[neighbour] = 3
			tracer[neighbour] -= 1
			weight += neighbour.size
		itemsList.remove(neighbour)
		if itemsList:
			return self.getLocalMax(itemsList)

		value = 0
		size = 0
		for item in self.current:
			self.bestCombo[item.name] += 1
			value += item.value
			size += item.size

		return self.bestCombo, value, size
	
	def findOptimum(self):
		a = random.choice(self.items)
		if a.size < self.sizeLimit:
			self.current.append(a)
		else:
			return self.findOptimum()
		itemsList = self.copy(self.items)
		return self.getLocalMax(itemsList)

	def hillTester(self):
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
			
		return mean(timeList), mean(values), mean(sizes)
    
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

# a = HillClimbing(42)

# a.addItem(x)
# a.addItem(y)
# a.addItem(z)
# a.addItem(w)
# a.addItem(p)
# a.addItem(q)
# a.addItem(r)
# a.addItem(s)

# print(a.findOptimum())