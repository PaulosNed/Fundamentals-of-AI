import math
import random
from statistics import mean
import time

class Item:
	def __init__(self, name, size, value) -> None:
		self.name = name   #string
		self.size = size  #float
		self.value = value  #int

class HillClimbing:
	def __init__(self, size) -> None:
		self.items = []
		self.sizeLimit = size
		self.bestCombo = []
		self.currentCombo = []
		self.best = []
	
	def addItem(self, item):
		if not isinstance(item, Item):
			raise Exception("not instantiated")
		self.items.append(item)
		
	def copy(self, combination):
		d = []
		for i in range(len(combination)):
			d.append(combination[i])
		return d

	def getRandom(self):
		randomSelection = random.sample(range(0, len(self.items)), len(self.items))
		tempSize = 0
		count = 0
		validList = [0] * len(self.items)
		for selection in randomSelection:
			if tempSize + self.items[selection].size > self.sizeLimit:
				break
			count+=1
			tempSize += self.items[selection].size
			# print(tempSize)
			validList[selection] = 1
		
		return validList
	
	def getValue(self, combination):
		size = self.getSize(combination)
		if size > self.sizeLimit:
			return 0

		value = 0
		for i in range(len(combination)):
			if combination[i]==1:
				value += self.items[i].value
		return value
	
	def getSize(self, combination):
		size = 0
		for i in range(len(combination)):
			if combination[i]==1:
				size += self.items[i].size
		return size

	def climbHill(self):
		self.currentCombo = self.getRandom()
		if len(self.currentCombo) != len(self.items):
			t = len(self.items) - len(self.currentCombo)
			l = [0] * t
			self.currentCombo.extend(l)
		value = self.getValue(self.currentCombo)
		size = self.getSize(self.currentCombo)
		for i in range(len(self.items)):
			if self.currentCombo[i] == 0 and size + self.items[i].size < self.sizeLimit:
				self.currentCombo[i] = 1
				value += self.items[i].value
				size += self.items[i].size
		
		self.bestCombo = self.currentCombo

		for i in range(len(self.bestCombo)):
			if self.bestCombo[i]==1:
				self.best.append(self.items[i].name)

		return self.best,  value, size
			 
	def hillTester(self):
		timeList = []
		values = []
		sizes = []

		for i in range(10):
			begin = time.perf_counter()
			answer = self.climbHill()
			end = time.perf_counter()
			t = (end - begin) * 1000
			timeList.append(t)
			values.append(answer[1])
			sizes.append(answer[2])
		print("\nAverage time, value and size of Hill Climbing algprothm when 20 items: ", mean(timeList),",", mean(values),",", mean(sizes), "\n")
	

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

	print(a.climbHill())

Initializer("20items.txt")