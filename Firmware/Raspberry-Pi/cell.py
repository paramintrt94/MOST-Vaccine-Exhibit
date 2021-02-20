# Importing libraries used to program this script
from gpiozero import RGBLED
from colorzero import Color
from time import sleep
from time import time

class Cell:
    immuneDuration = 5      #set to how many seconds before immune reset
    
    def __init__(self, led):
        self.status = "healthy"
        self.led = led
        self.led.color = (0,0,0)
        self.lastImmunized = -1
        self.prevColor = ""
    #end of init
        
    def updateStatus(self, sensor, debug=False):
        color = self.checkColor(sensor, debug)     #runs checkColor function to get color reading (returns: "Green", "Red", "White", or "Invalid")
        if self.status == "healthy":
            if not self.led.is_lit:
                self.led.color = (1,1,1)
            if color == "red":
                print("Cell is now infected.")
                self.status = "infected"
                self.led.color = Color("red")
            elif color == "green" or color == "white":
                print("Cell is now immunized.")
                self.status = "immune"
                self.lastImmunized = time()
                self.led.color = Color("green")
        elif self.status == "infected":
            if color == "green" or color == "white":
                print("Cell is now immunized.")
                self.status = "immune"
                self.lastImmunized = time()
                self.led.color = Color("green")
        elif self.status == "immune":
            if time()-self.lastImmunized > self.immuneDuration:
                print("Cell immune duration is over. Reset to healthy.")
                self.status = "healthy"
                self.led.color = Color("white")
                
    def checkColor(self, sensor, debug):
        # reads sensor color data and outputs color as string (red, green, white, invalid) might need tweaking to calibrate colors
        if debug:
            # this will print the rgb sensor color reading in (r,g,b) values
            print(sensor.color_rgb_bytes)
        if ((34 < sensor.color_rgb_bytes[0] < 45) and (5 < sensor.color_rgb_bytes[1] < 15) and (5 < sensor.color_rgb_bytes[2] < 15)) : #checking for red piece
            if not self.prevColor == "red" and debug:
                print("Detected virus piece")
                self.prevColor = "red"
            return "red"
        elif ((sensor.color_rgb_bytes[0] <= 5) and (23 < sensor.color_rgb_bytes[1] < 30) and (15 < sensor.color_rgb_bytes[2] < 30)): #checking for green piece
            if not self.prevColor == "green" and debug:
                print("Detected deactivated virus vaccine")
                self.prevColor = "green"
            return "green"
        elif ((6 < sensor.color_rgb_bytes [0] < 14) and (15 < sensor.color_rgb_bytes[1] < 25) and (13 < sensor.color_rgb_bytes[2] < 24)): #checking for white piece
            if not self.prevColor == "white" and debug:
                print("Detected mRNA messenger piece")
                self.prevColor = "white"
            return "white"
        else:
            if not self.prevColor == "invalid" and debug:
                print("Not detecting anything a valid piece")
                self.prevColor = "invalid"
            return "invalid"
