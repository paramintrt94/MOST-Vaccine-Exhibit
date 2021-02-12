import RPi.GPIO as GPIO
from gpiozero import LED
from signal import pause
from time import sleep
from pkglib.Cell import Cell
from pkglib.Sensor import Sensor

print("Starting Vaccine Exhibit")

testLED = LED(7)
testLED.on()
sleep(1000)
green1 = LED(16)
green2 = LED(15)
green3 = LED(14)
red1 = LED(11)
red2 = LED(12)
red3 = LED(13)
green4 = LED(33)
green5 = LED(35)
green6 = LED(36)
red4 = LED(37)
red5 = LED(38)
red6 = LED(39)

red1.on()
sleep(0.5)
green1.on()
red1.off()
sleep(0.5)

# initializing board
# numCells		number of white blood cells on board
# numPerGroup 	number of white blood cells per column
# numSensors	how many RGB sensors you will be using (opt autocalculated)
numCells = 6
numPerPair = 2
#numSensors = numCells/numPerPair
numSensors = 3

#list of all the white blood cells on board (might change depending on library)
cellList = []

#list of all the sensors
sensorList = []

#populate CellList (initialize WBC status and LED lights)
for i in range(numCells):
	cellList.append(Cell("healthy"))

print("\nCELL STATUS")
for index,cell in enumerate(cellList):
	print("Cell #"+str(index)+":\n"+cell.printInfo())

for i in range(numSensors):
	sensorList.append(Sensor())

print("\nSENSOR READINGS")
for index,sensor in enumerate(sensorList):
	print("Sensor #"+str(index)+" is reading "+sensor.getColor())

print("\nTEST SCENARIO")
#Test Scenarios
print("1.Placing infected virus on board in 2nd column")
sensorList[1].setColor("red")