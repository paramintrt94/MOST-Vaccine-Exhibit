# Importing libraries used to program this script
from gpiozero import RGBLED
from colorzero import Color
from time import sleep

# Initializing RPI board and I2C ports
import board
import busio
import adafruit_tcs34725
i2c = busio.I2C(board.SCL, board.SDA)
print("Debug")
print(i2c)
sensor = adafruit_tcs34725.TCS34725(i2c)

# Specifying RGB Pins using GPIO#   # RGB PIN EQUIVALENT
led1 = RGBLED(5,6,13)               # RGB LED1 PINS: RED PIN 29, GREEN PIN 31, BLUE PIN 33
led2 = RGBLED(19,26,12)             # RGB LED2 PINS: RED PIN 35, GREEN PIN 37, BLUE PIN 32
led3 = RGBLED(16,20,21)             # RGB LED3 PINS: RED PIN 36, GREEN PIN 38, BLUE PIN 40

def colorCheck(rgb_bytes):
    if (rgb_bytes[0] > 90 and (rgb_bytes[1]+rgb_bytes[2])<10):
        print("Detected virus piece")
        return Color("red")
    elif ((40 < rgb_bytes[1] < 50) and (rgb_bytes[0] < 5) and (0 < rgb_bytes[2] < 30)):
        print("Detected deactivated virus vaccine")
        return Color("green")
    elif ((10 < rgb_bytes[0] < 16) and (20 < rgb_bytes[1] < 25) and (10 < rgb_bytes[2] < 20)):
        print("Detected mRNA messenger piece")
        return Color("green")
    else:
        print("Not detecting anything or you tryna fool me?...")
        return Color("white")
    
print("Starting Vaccine Exhibit")

while True:
    color = sensor.color_rgb_bytes
    print(color)
    led1.color = colorCheck(color)
    sleep(1)

