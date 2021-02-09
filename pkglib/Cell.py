class Cell:
	validStatus = ["immune","compromised","healthy"]

	def __init__(self, status):
		self.status = status
		self.color = "white"
	#end of __init__

	def setLEDColor(self):
		if self.status == "immune":
			self.color = "green"
		elif self.status == "compromised":
			self.color = "red"
		else:
			self.color = "white"

	def getLEDColor(self):
		return self.color

	def setStatus(self, status):
		if status in self.validStatus:
			self.status = status
			print("Cell is now "+ status)
			self.setLEDColor()
			self.printInfo()
		else:
			print("You have entered an invalid status. Please try again.")
	#end of setStatus

	def printInfo(self):
		return "Current cell status is "+ self.status +".\nLED Color: "+self.color
	#end of printInfo

#end of Cell class