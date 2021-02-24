# Importing libraries used to program this script
from gpiozero import RGBLED, Button
from time import sleep
from cell import Cell

# Initializing RPI board and I2C ports
import board
import busio
import adafruit_tcs34725  # RGB Sensor Library
import adafruit_tca9548a  # Multiplexer Library

i2c = busio.I2C(board.SCL, board.SDA)  # Initiate I2C object
mpx = adafruit_tca9548a.TCA9548A(i2c)  # multiplexer object

# Specify which channels on the TCA9548A multiplexer are being used
mpx_channels = [3, 4, 5]
sensor_array = []
for mpx_channel in mpx_channels:
    sensor_array.append(adafruit_tcs34725.TCS34725(mpx[mpx_channel]))

# Specifying RGB Pins using GPIO#   # RGB PIN EQUIVALENT
led1 = RGBLED(5, 6, 13)  # RGB LED1 PINS: RED PIN 29, GREEN PIN 31, BLUE PIN 33
led2 = RGBLED(19, 26, 12)  # RGB LED2 PINS: RED PIN 35, GREEN PIN 37, BLUE PIN 32
led3 = RGBLED(16, 20, 21)  # RGB LED3 PINS: RED PIN 36, GREEN PIN 38, BLUE PIN 40
ledArray = [led1, led2, led3]

# Toggle Switch
button = Button(4)

# Create Array of "Cells"
number_of_groups = 3
cell_array = []
for i in range(number_of_groups):
    cell_array.append(Cell(ledArray[i], i))


def startup_check():
    # Will turn on each group of LEDs to white and then off
    for cell in cell_array:
        cell.led.on()
        sleep(0.5)
    for cell in cell_array:
        cell.led.off()


def cleanup():
    # turns off LEDs and resets Cells to healthy
    for cell in cell_array:
        cell.led.off()
        cell.status = "healthy"


print("Starting Vaccine Exhibit...")
startup_check()

debug = False  # set to debug level

while True:
    if button.is_pressed:
        for i, cell in enumerate(cell_array):
            cell.update_status(sensor_array[i], debug)
        sleep(1) if debug else None
    else:
        cleanup()
