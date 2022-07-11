import math
import random
from statistics import mean
import time

class Item:
	def __init__(self, name, size, value) -> None:
		self.name = name   #string
		self.size = size  #float
		self.value = value  #int
		self.amount = 3

class SimulatedAnnealing:	
	def __init__(self, size) -> None:
		self.items = []
		self.sizeLimit = size
		self.START_TEMPRATURE = 100 
		self.END_TEMPRATURE = 1
		self.COOLLING_RATE = 0.0002
		self.currentCombo = None
		self.bestCombo = None
		self.best = {}
	
	def addItem(self, item):
		if not isinstance(item, Item):
			raise Exception("not instantiated")
		self.items.append(item)
		self.best[item.name] = 0
			

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
	
	def getValue(self, combination):
		value = 0
		for item in combination:
			value += item.value
		return value
	
	def getSize(self, combination):
		size = 0
		for item in combination:
			size += item.size
		return size

	def acceptanceProbaility(self, value, newValue, temprature):
		if(newValue > value):
			return 1
		return math.exp((newValue-value)/temprature)
	
	def findOptimum(self):
		self.currentCombo = self.getRandom()
		self.bestCombo = self.currentCombo
		temprature = self.START_TEMPRATURE
		# self.COOLLING_RATE = self.COOLLING_RATE / len(self.items)
		while(temprature>self.END_TEMPRATURE):
			nextCombo = self.getRandom()
			currentValue = self.getValue(self.currentCombo) / self.getSize(self.currentCombo)
			nextValue = self.getValue(nextCombo) / self.getSize(nextCombo)

			if self.acceptanceProbaility(currentValue, nextValue, temprature) > random.uniform(0,1):
				self.currentCombo = nextCombo
			
			if self.getValue(self.currentCombo) > self.getValue(self.bestCombo):
				self.bestCombo = self.currentCombo
			temprature = temprature - (temprature*self.COOLLING_RATE)
		
		bestValue = 0
		bestSize = 0
		for item in self.bestCombo:
			self.best[item.name] += 1
			bestValue += item.value
			bestSize += item.size		

		return self.best, bestValue, bestSize
	def SATester(self):
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
			
		print("\nAverage time, value and size of Simulated Algorith when 20 items: ", mean(timeList),",", mean(values),",", mean(sizes), "\n")

def Initializer(fileName):
	wholeInfo = open(fileName, "r")
	index = 0
	for line in wholeInfo.readlines():
		if index==0:
			a = SimulatedAnnealing(int(line))
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

# a = SimulatedAnnealing(42)

# a.addItem(x)
# a.addItem(y)
# a.addItem(z)
# a.addItem(w)
# a.addItem(p)
# a.addItem(q)
# a.addItem(r)
# a.addItem(s)

# print(a.findOptimum())