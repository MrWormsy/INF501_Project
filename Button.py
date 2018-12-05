# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 19:47:50 2017

@author: lfoul, Antonin ROSA-MARTIN (aka MrWormsy) and IGIRANEZA Beda
"""

import pygame
from Emoticon import Emoticon

class Button:
    
    """
    A Button is represented as a Sensor and its location ( (0, 0) by default )
    """
    def __init__(self, sensor, x = 0, y = 0):
        self.sensor = sensor
        self.x = x
        self.y = y
    
    """
    Draw a button at its location, if the button is selected we draw it with bold borders
    draw : Button --> None
    """ 
    def draw(self):

        #If this button is the one selected we draw it with bold borders, else with thin borders
        if(self.sensor.sensorId == self.sensor.generalConfiguration.selectedSensor):
            pygame.draw.rect(self.sensor.generalConfiguration.screen, [224, 17, 95], [self.getPosition()[0], self.getPosition()[1], self.sensor.generalConfiguration.buttonWidth, self.sensor.generalConfiguration.buttonHeight], 6)
        else:
            pygame.draw.rect(self.sensor.generalConfiguration.screen, [224, 17, 95], [self.getPosition()[0], self.getPosition()[1], self.sensor.generalConfiguration.buttonWidth, self.sensor.generalConfiguration.buttonHeight], 1)
        
        #We use the given string formating pattern
        lines = "['', " + self.sensor.label +", '', " + str(self.sensor.read()) +"]"
        
        #We draw the lines inside the button
        self.drawLines(lines)
    
    """
    Get the position of the button
    getPosition : Button --> Point
    """ 
    def getPosition(self):
        return [self.x, self.y]
    
    """
    Set the position of the button
    setPosition : Button, Point --> None
    """
    def setPosition(self, position):
        self.x = position[0]
        self.y = position[1]
    
    """
    Draw the formating line inside the button
    drawLines : Button, String --> None
    """
    def drawLines(self, lines):
        #We first format the string (remove all the thing uneeded)
        newLines = lines.replace("[", "").replace("]", "")
        
        # Creates the font
        font = pygame.font.Font(None, 20)
        
        #We get the number of lines to draw and then get the space between each lines (in term of height)
        i = 0
        imax = newLines.split(',').__len__()
        spaceBetweenStrings = self.sensor.generalConfiguration.buttonHeight/imax
        
        #Then we split the formated string into several strings by using the split() method
        for str1 in newLines.split(','):
            #We say that we wont have a sring with more than 30 characteres, so with pad it and then we center it inside the button
            try:
                #We get the float value given by the sensor if we can convert the current sring into a float
                float(str1.replace("'", ""))
                #We create a text image with the string in it
                textImage = font.render(str1.replace("'", "").center(30, ' '), 1, Emoticon.color(self.sensor.getTransformedValue()))
            except:
                #Otherwise this string does not contain a float value
                #We create a text image with the string in it
                textImage = font.render(str1.replace("'", "").center(30, ' '), 1, [255, 255, 255])
            #We paste the text image on our screen at the right coordinates (centered within the button)
            self.sensor.generalConfiguration.screen.blit(textImage, [self.getPosition()[0] + (self.sensor.generalConfiguration.getButtonWidth() /2 - textImage.get_width()/2), self.getPosition()[1] + spaceBetweenStrings * i - (textImage.get_height()/2)])
            
            
            i+=1

