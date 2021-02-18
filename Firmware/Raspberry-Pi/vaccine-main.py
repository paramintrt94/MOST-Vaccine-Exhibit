# Importing libraries used to program this script
from gpiozero import RGBLED, Button
from colorzero import Color
from time import sleep
from cell import Cell
from signal import pause

# Initializing RPI board and I2C ports
import board
import busio
import adafruit_tcs34725
i2c = busio.I2C(board.SCL, board.SDA)
print(i2c)
sensor = adafruit_tcs34725.TCS34725(i2c)

# Specifying RGB Pins using GPIO#   # RGB PIN EQUIVALENT
led1 = RGBLED(5,6,13)               # RGB LED1 PINS: RED PIN 29, GREEN PIN 31, BLUE PIN 33
led2 = RGBLED(19,26,12)             # RGB LED2 PINS: RED PIN 35, GREEN PIN 37, BLUE PIN 32
led3 = RGBLED(16,20,21)             # RGB LED3 PINS: RED PIN 36, GREEN PIN 38, BLUE PIN 40
ledArray = [led1,led2,led3]
ledColorCycle = [(1,0,0),(0,1,0),(0,0,1)]

# Toggle Switch
button = Button(4)

# Create Array of "Cells"
number_of_groups = 3
cellArray = []
for i in range(number_of_groups):
    cellArray.append(Cell(ledArray[i]))

def startupCheck():
    # Will turn on each group of LEDs to white and then off
    for cell in cellArray:
        cell.led.on()
        sleep(0.5)
    for cell in cellArray:
        cell.led.off()
        
def cleanup():
    # turns off LEDs and resets Cells to healthy
    for cell in cellArray:
        cell.led.off()
        cell.status = "healthy"

print("Starting Vaccine Exhibit...")
startupCheck()

while True:
    if(button.is_pressed):
        for cell in cellArray:
            print(cell)
            cell.updateStatus(sensor)           # uncomment for production
            #sleep(3)                           # uncomment for single sensor mode
            #cell.updateStatus(sensor, True)    # uncomment for debugging
    else:
        cleanup()
        sleep(5)
    #sleep(3)
