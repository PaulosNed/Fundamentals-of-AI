import math
import random

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
	
	def getLocalMax(self, size):
		index = self.values.index(max(self.values))
		if self.itemsList[index].size < size:
			self.bestCombo[self.itemsList[index]] = 1
			currSize = self.itemsList[index].size
			while(currSize + self.itemsList[index].size < size):
				currSize += self.itemsList[index].size
				self.bestCombo[self.itemsList[index]] +=1
			# print(size, currSize)
			size -= currSize
		self.values.pop(index)
		self.itemsList.pop(index)
		if len(self.itemsList) > 0:
			return self.getLocalMax(size)

		finalMap = {}
		worth = 0
		weight = 0
		for key, value in self.bestCombo.items():
			finalMap[key.name] = value
			worth += (key.value * value)
			print(worth)
			weight += (key.size * value)

		return finalMap, worth, weight
			
			


    
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

	print(a.getLocalMax(a.sizeLimit))

Initializer("20items.txt")