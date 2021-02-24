from time import sleep
from signal import pause
from gpiozero import RGBLED
import board
import busio
import adafruit_tcs34725    # RGB Sensors
import adafruit_tca9548a    # Multiplexer

led1 = RGBLED(5,6,13)               # RGB LED1 PINS: RED PIN 29, GREEN PIN 31, BLUE PIN 33
led2 = RGBLED(19,26,12)             # RGB LED2 PINS: RED PIN 35, GREEN PIN 37, BLUE PIN 32
led3 = RGBLED(16,20,21)             # RGB LED3 PINS: RED PIN 36, GREEN PIN 38, BLUE PIN 40
ledArray = [led1,led2,led3]
ledColorCycle = [(1,0,0),(0,1,0),(0,0,1)]

i2c = busio.I2C(board.SCL, board.SDA)
mpx = adafruit_tca9548a.TCA9548A(i2c) # multiplexer
mpx_channels = [3,4,5]
sensorArray = []

ledTest = True
mpxTest = False
rgbSensorTest = True

if mpxTest or rgbSensorTest:
    for mpx_channel in mpx_channels:
        sensorArray.append(adafruit_tcs34725.TCS34725(mpx[mpx_channel]))
        print("Initialized mpx channel",str(mpx_channel),)

def getColorRange(trys):
    currentTry = 0
    sensorArray = []
    reds = []
    greens = []
    blues = []
    for mpx_channel in mpx_channels:
        sensorArray.append(adafruit_tcs34725.TCS34725(mpx[mpx_channel]))
    while currentTry < trys:
        for sensor in sensorArray:
            reds.append(sensor.color_rgb_bytes[0])
            greens.append(sensor.color_rgb_bytes[1])
            blues.append(sensor.color_rgb_bytes[2])
        currentTry += 1
    print("COLOR\tMIN\tMAX")
    print("RED\t"+str(min(reds))+"\t"+str(max(reds)))
    print("GREEN\t"+str(min(greens))+"\t"+str(max(greens)))
    print("BLUE\t"+str(min(blues))+"\t"+str(max(blues)))
            

while ledTest or rgbSensorTest:
    if ledTest:
        for led in ledArray:
            led.toggle()
    if rgbSensorTest:
        print(sensorArray[0].color_rgb_bytes,"\t",sensorArray[1].color_rgb_bytes,"\t",sensorArray[2].color_rgb_bytes)
    sleep(0.5)

def led_off():
    for led in ledArray:
        led.off()

led_off()
# ~ getColorRange(50)
