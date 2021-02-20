from time import sleep
from signal import pause
from gpiozero import RGBLED, Button
import board
import busio
import adafruit_tcs34725    # RGB Sensors
led1 = RGBLED(5,6,13)               # RGB LED1 PINS: RED PIN 29, GREEN PIN 31, BLUE PIN 33
led2 = RGBLED(19,26,12)             # RGB LED2 PINS: RED PIN 35, GREEN PIN 37, BLUE PIN 32
led3 = RGBLED(16,20,21)             # RGB LED3 PINS: RED PIN 36, GREEN PIN 38, BLUE PIN 40
ledArray = [led1,led2,led3]
ledColorCycle = [(1,0,0),(0,1,0),(0,0,1)]

import adafruit_tcs34725    # RGB Sensors
import adafruit_tca9548a    # Multiplexer

i2c = busio.I2C(board.SCL, board.SDA)
# ~ mpx = adafruit_tca9548a.TCA9548A(i2c) # multiplexer
# ~ mpx_channels = [3,4,5]
# ~ sensorArray = []
# ~ for mpx_channel in mpx_channels:
    # ~ sensorArray.append(adafruit_tcs34725.TCS34725(mpx[mpx_channel]))

# ~ while True:
	# ~ for idx, mpx_channel in enumerate(mpx_channels):
		# ~ print(str(idx) + str(sensorArray[idx].color_rgb_bytes))
		# ~ sleep(1)

while True:
	led1.on()
	led2.on()
	led3.on()
