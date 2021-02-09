class Sensor:
	validColors=["white","green","red"]

	def __init__(self):
		self.color = ""
	#end of __init__

	def setColor(self,color):
		if color in self.validColors:
			self.color = color
			print("Detected "+color+" piece")
		else:
			print("Not valid color detected")

	def getColor(self):
		if self.color in self.validColors:
			return self.color
		else:
			return "no piece"