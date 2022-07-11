import math
import random

class Item:
	def __init__(self, name, size, value) -> None:
		self.name = name   #string
		self.size = size  #float
		self.value = value  #int

class SimulatedAnnealing:
	
	def __init__(self, size) -> None:
		self.items = []
		self.sizeLimit = size
		self.START_TEMPRATURE = 100
		self.END_TEMPRATURE = 1
		self.COOLLING_RATE = 0.00002
		self.currentCombo = self.getRandom()
		self.bestCombo = self.currentCombo
	
	def addItem(self, item):
		if not isinstance(item, Item):
			raise Exception("not instantiated")
		self.items.append(item)	

	def getRandom(self):
		randomSelection = random.sample(range(0, len(self.items)), len(self.items))
		tempSize = 0
		count = 0
		validList = []
		for selection in randomSelection:
			if tempSize + self.items[selection].size > self.sizeLimit:
				break
			count+=1
			tempSize += self.items[selection].size
			print(tempSize)
			validList.append(self.items[selection])

		return validList
	
	def getValue(self, combination):
		value = 0
		for item in combination:
			value += item.value
		return value


	def acceptanceProbaility(self, value, newValue, temprature):
		if(newValue > value):
			return 1
		return math.exp((newValue-value)/temprature)
	
	def findOptimum(self):
		temprature = self.START_TEMPRATURE

		while(temprature>self.END_TEMPRATURE):
			nextCoor = self.getRandom()
			currentValue = self.getValue(self.currentCombo)
			nextValue = self.getValue(nextCoor)

			if self.acceptanceProbaility(currentValue, nextValue, temprature) > random.uniform(0,1):
				self.currentCombo = nextCoor
				# print("cuurent Coordinate: ", self.currentCombo)
			
			# print("initial-Best: ", self.bestCombo)
			if self.getValue(self.currentCombo) > self.getValue(self.bestCombo):
				self.bestCombo = self.currentCombo
				
			temprature = temprature - (temprature*self.COOLLING_RATE)
		
		best = []
		bestValue = 0
		for item in self.bestCombo:
			best.append(item.name)
			bestValue += item.value
		

		return best, bestValue



x= Item("x", 5, 6)
y= Item("y", 15, 10)
z= Item("z", 1, 10)
w= Item("w", 2, 2)
p= Item("p", 9, 8)
q= Item("q", 3, 3)
r= Item("r", 2, 1)
s= Item("s", 7, 20)

a = SimulatedAnnealing(10)

a.addItem(x)
a.addItem(y)
a.addItem(z)
a.addItem(w)
a.addItem(p)
a.addItem(q)
a.addItem(r)
a.addItem(s)

print(a.findOptimum())