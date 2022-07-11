import math
import random

class SimulatedAnnealing:
	
	def __init__(self) -> None:
		self.START_COORDINATE = -2
		self.END_COORDINATE = 2
		self.START_TEMPRATURE = 100
		self.END_TEMPRATURE = 1
		self.COOLLING_RATE = 0.02
		self.currentCoor = self.getRandom(self.START_COORDINATE, self.END_COORDINATE)
		self.bestCoor = self.currentCoor

	def getRandom(self, start , end):
		return random.uniform(start, end)
		
	def getEnergy(self, x):
		return self.f(x)
	
	def f(self, x):
		res = (x-0.3)*(x-0.3)*(x-0.3)-5*x+x*x-2
		return res
	def acceptanceProb(self, energy, newEnergy, temprature):
		if(newEnergy < energy):
			return 1
		return math.exp((energy-newEnergy)/temprature)
	
	def findOptimum(self):
		temprature = self.START_TEMPRATURE

		while(temprature>self.END_TEMPRATURE):
			nextCoor = self.getRandom(self.START_COORDINATE, self.END_COORDINATE)
			currentEnergy = self.getEnergy(self.currentCoor)
			nextEnergy = self.getEnergy(nextCoor)

			if self.acceptanceProb(currentEnergy, nextEnergy, temprature) > self.getRandom(0,1):
				self.currentCoor = nextCoor
				# print("cuurent Coordinate: ", self.currentCoor)
			
			# print("initial-Best: ", self.bestCoor)
			if self.f(self.currentCoor) > self.f(self.bestCoor):
				self.bestCoor = self.currentCoor
				
			temprature = temprature - (temprature*self.COOLLING_RATE)
		
		return self.bestCoor


a = SimulatedAnnealing()
print("The global maximum according to SA is: \t", a.findOptimum())