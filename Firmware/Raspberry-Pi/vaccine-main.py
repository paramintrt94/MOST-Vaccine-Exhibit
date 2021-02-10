import RPi.GPIO as GPIO
from time import sleep
from pkglib.Cell import Cell
from pkglib.Sensor import Sensor

print("Starting Vaccine Exhibit")

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(10, GPIO.IN)

while True: # Run forever
    if not (GPIO.input(10)):
        GPIO.output(8, GPIO.HIGH) # Turn on                # Sleep for 1 second
    else:
        GPIO.output(8, GPIO.LOW)  # Turn off                # Sleep for 1 second
    
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