# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 19:47:50 2017

@author: lfoul, Antonin ROSA-MARTIN (aka MrWormsy) and IGIRANEZA Beda
"""

import pygame
import math
from Sensor import Sensor

class Emoticon:

    """
    An Emoticon is represented as a sensor
    """
    def __init__(self, sensor) :
        self.sensor = sensor
    
    """
    Set all the parameters for the emoticon
    setEmoticonParameters : Emoticon, int --> None
    """
    def setEmoticonParameters(self, size) :
         self.eyeWidth = 0.1*size
         self.eyeHeight = 0.15*size
         self.eyeLeftPosition = [-0.15*size, 0.1*size]
         self.eyeRightPosition = [0.15*size, 0.1*size]
         self.mouthPosition = [0, -0.25*size]
         self.mouthMaxHeight = 0.3*size
         self.mouthMaxWidth = 0.55*size
         self.mouthAngle = math.pi/10

    """
    Draw the emoticon according to the value of x, which is the transformed value of the sensor (the mapped value)
    draw : Emoticon, int --> None
    """    
    def draw(self, x):
        #Head
        self.head(x)
        
        #Left eye
        self.eye(self.headToArea(self.eyeLeftPosition))
        
        #Right eye
        self.eye(self.headToArea(self.eyeRightPosition))
        
        #Mouth
        self.mouth(self.headToArea(self.mouthPosition), x)
    
    """
    Get the position of the given position into the orthonormal coordinate system of the Emoticon
    headToArea : Emoticon, Point --> Point
    """
    def headToArea(self, position):
        #Get the center of the Emoticon
        x = self.sensor.generalConfiguration.get_width()/2
        y = self.sensor.generalConfiguration.getButtonHeight() + self.sensor.generalConfiguration.emoticonBorder + int(self.sensor.generalConfiguration.emoticonSize / 2)
        
        #Then return the new position of the given position
        return [int(position[0]+x), int(-(position[1]-y))]
    
    """
    Get the color according to a float value between -1 and 1
    color : float --> Color
    """
    def color(x):
        #Blue is always 0
        b = 0
        
        #Then Red and Green change according to x
        if(x == 0):
            r = 255
            g = 255
        elif(x < 0):
            r = 255
            g = int(255 - int(Sensor.mapValue(-x, 0, 1, 0, 255)))
        else:
            g = 255
            r = int(255 - int(Sensor.mapValue(x, 0, 1, 0, 255)))
            
        #We return the Color
        return [r, g, b]
        
    """
    Draw the head of the emoticon according to a float value
    head : Emoticon, float --> None
    """
    def head(self, x):
        #draw the head
        pygame.draw.circle(self.sensor.generalConfiguration.screen, Emoticon.color(x), self.headToArea([0, 0]), int(self.sensor.generalConfiguration.emoticonSize / 2))
    
    """
    Draw an eye at the given position
    eye : Emoticon, Point --> None
    """
    def eye(self, position):
        #Draw an eye
        pygame.draw.ellipse(self.sensor.generalConfiguration.screen, [0, 0, 0], [position[0] - self.eyeWidth/2, position[1] - self.eyeHeight, self.eyeWidth, self.eyeHeight], 0)
    
    """
    Draw the mouth at the given position according to a float value
    eye : Emoticon, Point, float --> None
    """
    def mouth(self, position, x):
        #We draw it differently according to the float value
        if(x >= -0.15 and x <= 0.15):
            pygame.draw.line(self.sensor.generalConfiguration.screen, [0, 0, 0], [position[0] - int(self.mouthMaxWidth/2), position[1]], [position[0] + int(self.mouthMaxWidth/2), position[1]], 1)
        elif(x > 0):
            pygame.draw.arc(self.sensor.generalConfiguration.screen, [0, 0, 0], [position[0] - int(self.mouthMaxWidth/2), position[1] - int((x*self.mouthMaxHeight)/2) - int(math.cos(self.mouthAngle)), self.mouthMaxWidth, self.mouthMaxHeight * x], math.pi + self.mouthAngle, -self.mouthAngle, 1)
        else:
            pygame.draw.arc(self.sensor.generalConfiguration.screen, [0, 0, 0], [position[0] - int(self.mouthMaxWidth/2), position[1] - int((-x*self.mouthMaxHeight)/2) + int(math.cos(self.mouthAngle)), self.mouthMaxWidth, self.mouthMaxHeight * -x], self.mouthAngle, math.pi - self.mouthAngle, 1)