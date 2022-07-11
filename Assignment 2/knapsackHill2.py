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
		self.bestCombo = {}
		self.itemsList = []
		self.values = []
	
	def addItem(self, item):
		if not isinstance(item, Item):
			raise Exception("not instantiated")
		self.items.append(item)
		self.itemsList = self.copy(self.items)
		self.values = self.getValues(self.itemsList)
		self.bestCombo[item] = 0
	
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
	
	def climbHill(self):
		tracker = []
		initial = random.sample(self.items, 1)[0]
		index = self.items.index(initial)
		for i in range(index+1, len(self.items)):
			if self.items[i].value > self.items[index].value:
				tracker.append(initial)
				initial = self.items[i]
			else:
				break
		return initial, tracker
	
	def getMax(self, initial, tracker, size):
		if initial.size < size:
			self.bestCombo[initial] = 1
			currSize = initial.size
			while(currSize + initial.size < size):
				currSize += initial.size
				self.bestCombo[initial] +=1
			size -= currSize
		tempValue = 0
		tempItem = None

		if len(tracker) != 0:
			for item in tracker:
				if item.size < size and item.value > tempValue:
					tempItem = item
					tempValue = item.value
			if tempItem == None:
				return self.finalOutput()
			tracker.remove(tempItem)

			if tempValue != 0:
				return self.getMax(tempItem, tracker, size)

		return self.finalOutput()

	def finalOutput(self):
		finalMap = {}
		worth = 0
		weight = 0
		for key, value in self.bestCombo.items():
			finalMap[key.name] = value
			worth += (key.value * value)
			weight += (key.size * value)

		return finalMap, worth, weight
			
	def getLocalMax(self):
		initial, tracker = self.climbHill()
		return self.getMax(initial, tracker, self.sizeLimit)
	
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

	print(a.getLocalMax())

Initializer("15items.txt")