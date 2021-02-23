# Importing libraries used to program this script
from gpiozero import RGBLED
from colorzero import Color
from time import sleep
from time import time
import math

class Cell:
    colorSensitivity = 1    # set color sensitivity (higher number allows higher variance in color reading)
    certaintyLevel   = 4    # set higher value to ignore more ambient lighting when no piece is placed
    immuneDuration   = 6    # set to how many seconds before immune reset
    expValue         = 0.1  # set how aggressive to fade color, lower value keeps green on longer
    kValue           = math.log(1/expValue)
    
    def __init__(self, led, idx):
        self.idx = idx
        self.status = "healthy"
        self.led = led
        self.led.color = (0,0,0)
        self.lastImmunized = -1
        self.prevColor = ""
        self.hysterisisCount = 1
    #end of init
        
    def updateStatus(self, sensor, debug=False):
        color = self.checkColor(sensor, debug)     #runs checkColor function to get color reading (returns: "Green", "Red", "White", or "Invalid")
        if self.status == "healthy":
            None if self.led.is_lit else self.led.on()
            if color == "red":
                print("Cell "+str(self.idx)+" is now infected.") if debug else None
                self.status = "infected"
                self.led.color = (1,0,0)
            elif color == "green" or color == "white":
                print("Cell "+str(self.idx)+" is now immunized.") if debug else None
                self.status = "immune"
                self.lastImmunized = time()
                self.led.color = (0,1,0)
        elif self.status == "infected":
            if color == "green" or color == "white":
                print("Cell "+str(self.idx)+" is now immunized.") if debug else None
                self.status = "immune"
                self.lastImmunized = time()
                self.led.color = (0,1,0)
        elif self.status == "immune":
            elapsedTime = time()-self.lastImmunized
            elapsedTimePercent = elapsedTime/self.immuneDuration
            if elapsedTimePercent >= 1:
                print("Cell "+str(self.idx)+" immune duration is over. Reset to healthy.") if debug else None
                self.status = "healthy"
                self.led.color = (1,1,1)
            else:
                self.led.color = (self.expValue*math.exp(self.kValue*elapsedTimePercent), 1, self.expValue*math.exp(self.kValue*elapsedTimePercent))
                
    def checkColor(self, sensor, debug):
        # reads sensor color data and outputs color as string (red, green, white, invalid) might need tweaking to calibrate colors
        sensorColorRGB = sensor.color_rgb_bytes
                    
        if ((30-self.colorSensitivity <= sensorColorRGB[0] <= 43+self.colorSensitivity) and (8-self.colorSensitivity <= sensorColorRGB[1] <= 11+self.colorSensitivity) and (8-self.colorSensitivity <= sensorColorRGB[2] <= 11+self.colorSensitivity)) : #checking for red piece
            if self.prevColor == "red":
                self.hysterisisCount += 1
                if self.hysterisisCount >= self.certaintyLevel:
                    print("S"+str(self.idx)+" detected virus piece") if self.hysterisisCount == self.certaintyLevel else None                        
                    return "red"
            else:
                self.hysterisisCount = 0
            self.prevColor = "red"

        elif ((sensorColorRGB[0] <= 5+self.colorSensitivity) and (25-self.colorSensitivity <= sensorColorRGB[1] <= 31+self.colorSensitivity) and (17-self.colorSensitivity <= sensorColorRGB[2] <= 29+self.colorSensitivity)): #checking for green piece
            if self.prevColor == "green":
                self.hysterisisCount += 1
                if self.hysterisisCount >= self.certaintyLevel:
                    print("S"+str(self.idx)+" detected deactivated virus vaccine") if self.hysterisisCount == self.certaintyLevel else None            
                    return "green"
            else:
                self.hysterisisCount = 0
            self.prevColor = "green"            
            
        elif ((9-self.colorSensitivity <= sensorColorRGB [0] <= 13+self.colorSensitivity) and (18-self.colorSensitivity <= sensorColorRGB[1] <= 22+self.colorSensitivity) and (14-self.colorSensitivity <= sensorColorRGB[2] <= 22+self.colorSensitivity)): #checking for white piece
            if self.prevColor == "white":
                self.hysterisisCount += 1
                if self.hysterisisCount >= self.certaintyLevel:
                    print("S"+str(self.idx)+" detected mRNA messenger piece") if self.hysterisisCount == self.certaintyLevel else None
                    return "white"
            else:
                self.hysterisisCount = 0
            self.prevColor = "white"            

        else:
            self.hysterisisCount = 0 if self.prevColor != "invalid" else None
            self.prevColor = "invalid"
            return "invalid"
        
        print("S"+str(self.idx)+" color reading:",sensorColorRGB,"\t["+self.prevColor+"]") if debug else None            # this will print the rgb sensor color reading in (r,g,b) values
            
    def debugColor(self, sensor):
        print("S"+str(self.idx)+" color reading:",sensor.color_rgb_bytes)
