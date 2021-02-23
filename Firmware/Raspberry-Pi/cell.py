# Importing libraries used to program this script
from gpiozero import RGBLED
from colorzero import Color
from time import sleep
from time import time

class Cell:
    colorSensitivity = 2    # set color sensitivity (higher number allows higher variance in color reading)
    certaintyLevel   = 5    # set higher value to ignore more ambient lighting when no piece is placed
    immuneDuration   = 5    # set to how many seconds before immune reset
    
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
                self.led.color = Color("red")
            elif color == "green" or color == "white":
                print("Cell "+str(self.idx)+" is now immunized.") if debug else None
                self.status = "immune"
                self.lastImmunized = time()
                self.led.color = Color("green")
        elif self.status == "infected":
            if color == "green" or color == "white":
                print("Cell "+str(self.idx)+" is now immunized.") if debug else None
                self.status = "immune"
                self.lastImmunized = time()
                self.led.color = Color("green")
        elif self.status == "immune":
            if time()-self.lastImmunized > self.immuneDuration:
                print("Cell "+str(self.idx)+" immune duration is over. Reset to healthy.") if debug else None
                self.status = "healthy"
                self.led.color = Color("white")
                
    def checkColor(self, sensor, debug):
        # reads sensor color data and outputs color as string (red, green, white, invalid) might need tweaking to calibrate colors
        sensorColorRGB = sensor.color_rgb_bytes
                    
        if ((34 < sensorColorRGB[0] < 45) and (5 < sensorColorRGB[1] < 15) and (5 < sensorColorRGB[2] < 15)) : #checking for red piece
            if self.prevColor == "red":
                self.hysterisisCount += 1
                if self.hysterisisCount >= self.certaintyLevel:
                    print("S"+str(self.idx)+" detected virus piece") if self.hysterisisCount == self.certaintyLevel else None                        
                    return "red"
            else:
                self.hysterisisCount = 0
            self.prevColor = "red"

        elif ((sensorColorRGB[0] <= 5) and (23 < sensorColorRGB[1] < 30) and (15 < sensorColorRGB[2] < 30)): #checking for green piece
            if self.prevColor == "green":
                self.hysterisisCount += 1
                if self.hysterisisCount >= self.certaintyLevel:
                    print("S"+str(self.idx)+" detected deactivated virus vaccine") if self.hysterisisCount == self.certaintyLevel else None            
                    return "green"
            else:
                self.hysterisisCount = 0
            self.prevColor = "green"            
            
        elif ((6 < sensorColorRGB [0] < 14) and (15 < sensorColorRGB[1] < 25) and (13 < sensorColorRGB[2] < 24)): #checking for white piece
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
