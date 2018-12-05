# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 19:47:50 2017

@author: lfoul, Antonin ROSA-MARTIN (aka MrWormsy) and IGIRANEZA Beda
"""

import pygame
from Emoticon import Emoticon
from Button import Button
from Sensor import Sensor

class GeneralConfiguration:
    
    """
    A GeneralConfiguration is represented as a lot of variables
    """
    def __init__(self) :
        #We init Pygame
        self.initPygame()
    
        # Parameters for the buttons
        self.buttonWidth = 150
        self.buttonHeight = 80

        # Parameters for the emoticons
        self.emoticonSize = 400
        self.emoticonBorder = 20
        
         # Sensors list
        self.sensors = []
        
        #Id of the selected sensor
        self.selectedSensor = 0
        
        #List of the data gathered
        self.data = []

    """
    Initializes pygame
    initPygame : GeneralConfiguration --> None
    """
    def initPygame(self):
        #Initialization
        pygame.init()
        
        # Sets the screen size.
        pygame.display.set_mode((800, 600))    
       
        # Sets the timer to check event every 17 ms (60 frames per seconds (Kind of useless because Pygame lags a lot...))
        pygame.time.set_timer(pygame.USEREVENT, 17)
        
        # Gets pygame screen
        self.screen = pygame.display.get_surface()
        
        #Set a title
        pygame.display.set_caption("TP2 Emoticon - INF501")
            
    """
    Draw the Buttons and the current Emoticon pygame
    draw : GeneralConfiguration --> None
    """
    def draw(self):
        #Draw the current Emoticon 
        self.sensors[self.selectedSensor].drawEmoticon()
        #Draw all the sensors
        for sensor in self.sensors:
            sensor.drawButton()
    
    """
    Get the selected Sensor'd id
    getSelectedSensor : GeneralConfiguration --> int
    """
    def getSelectedSensor(self):
        return self.selectedSensor
    
    """
    Get the list of Sensor
    getSensors : GeneralConfiguration --> List of Sensor
    """
    def getSensors(self):
        return self.sensors
    
    """
    Set the selected sensor's id
    setSelectedSensor : GeneralConfiguration, int --> None
    """
    def setSelectedSensor(self, selectedSensor):
        self.selectedSensor = selectedSensor
        
    """
    Display the Pygame screen
    display : GeneralConfiguration --> None
    """
    def display(self):
        
        #We wipe everything on the screen
        self.screen.fill([0, 0, 0])
        
        #We draw the Emoticon and the Buttons
        self.draw()
        
        #We gather the data from all the sensors
        self.gatherData()
        
        #We draw the graph of the selected sensor
        self.drawGraph()
        
        #Pygame code to display...
        pygame.display.flip()
        pygame.event.clear(pygame.USEREVENT)
      
    """
    Get the width of the the drawing surface
    get_width : GeneralConfiguration --> int
    """
    def get_width(self):
        return self.screen.get_width()
    
    """
    Get the height of the the drawing surface
    get_height : GeneralConfiguration --> int
    """
    def get_height(self):
        return self.screen.get_height()
    
    """
    Get the screen of the the drawing surface
    getScreen : GeneralConfiguration --> Screen
    """
    def getScreen(self):
        return self.screen
    
    """
    Get the button's width of the the drawing surface
    getButtonWidth : GeneralConfiguration --> int
    """
    def getButtonWidth(self):
        return self.buttonWidth
    
    """
    Get the button's height of the the drawing surface
    getButtonHeight : GeneralConfiguration --> int
    """
    def getButtonHeight(self):
        return self.buttonHeight
    
    """
    Get the emoticon's size of the the drawing surface
    getEmoticonSize : GeneralConfiguration --> int
    """
    def getEmoticonSize(self):
        return self.emoticonSize
    
    """
    Get the emoticon's border of the the drawing surface
    getEmoticonBorder : GeneralConfiguration --> int
    """
    def getEmoticonBorder(self):
        return self.emoticonBorder
 
    """
    Set the GeneralConfiguration
    setGeneralConfiguration : GeneralConfiguration, GeneralConfiguration --> None
    """
    def setGeneralConfiguration(self, generalConfiguration) :
        self.generalConfiguration = generalConfiguration
        
    """
    Add a Sensor to the list of Sensors
    addSensor : GeneralConfiguration, Sensor --> None
    """   
    def addSensor(self, sensor):
        sensor.setGeneralConfiguration(self)
        sensor.setSensorId(len(self.sensors))
        sensor.setEmoticon(Emoticon(sensor))
        sensor.setButton(Button(sensor))
        self.sensors.append(sensor)

    """
    Checks if the display of a new sensor was requested (if a Button was clicked)
    checkIfSensorChanged : GeneralConfiguration, Point --> boolean
    """
    def checkIfSensorChanged(self, eventPosition):
        i = -1
        idSensor = 0
        #We check if the clicked position is inside the rectangle made by a Button, we get the id of the clicked Button
        for sensor in self.sensors:
            if ((eventPosition[0] >= sensor.button.getPosition()[0]) and (eventPosition[0] <= sensor.button.getPosition()[0] + self.getButtonWidth()) and (eventPosition[1] >= sensor.button.getPosition()[1]) and (eventPosition[1] <= sensor.button.getPosition()[1] + self.getButtonHeight())):
                break
            i += 1
            idSensor += 1
        
        #If the id of the sensor is between 0 and lenght we set the current sensor to the id (and if the id is 0 we check if i != -1 because this is the first iteration) else we let the current id
        if ((i != -1 or idSensor == 0) and idSensor < self.sensors.__len__()):
            self.setSelectedSensor(idSensor)
    
    """
    Center all the Button on the screen
    centerButtons : GeneralConfiguration --> None
    """
    def centerButtons(self):
        #We first get the number of Buttons
        nbOfButtons = self.sensors.__len__()
        
        #Get the maximum space bewteen each Buttons
        spacesBetweenButtons = ((self.get_width()) - (nbOfButtons * self.buttonWidth)) / nbOfButtons
        
        i = 0
        #Then for each Buttons we put their right position centered and with a certain amount of space
        for sensor in self.sensors:
            sensor.button.setPosition([i * (spacesBetweenButtons + self.buttonWidth) + (spacesBetweenButtons / 2), 0])
            i += 1
    
    """
    Method to gather the data every updates to plot a graph
    gatherData : GeneralConfiguration --> None
    """
    def gatherData(self):
        
        #If the size of data is 0, we create a set of list to save the data into a list
        if(self.data.__len__() == 0):
            for sensor in self.sensors:
                self.data.append([sensor.read()])
        else:
            idSensor = 0
            for sensor in self.sensors:
                #If the size of the list is greater than or equal to 200 we remove the first one
                if (self.data.__len__() >= 200):
                    self.data.pop(0)
                #We append the value at the end
                self.data[idSensor].append(sensor.read())
                idSensor += 1
                
    """
    Draw the chart of the selected sensor
    drawGraph : GeneralConfiguration --> None
    """
    def drawGraph(self):
        #Get the data of the selected sensor
        data = self.data[self.selectedSensor]
        
        #WE DO NOT USE THIS OPTION! This is used to see the thresholds and the values mapped by between them
        """
        #IMOROVE GRAPH WITH ALL THE THRESHOLD  
        thresholds = self.sensors[self.selectedSensor].getThresholds()
        """
        
        #We have to know at least 2 points
        if (data.__len__() < 2):
            return
        
        #We get the minimum value and the maximum one to map all the values bewteen them
        minData = min(data)
        maxData = max(data)
        
        #WE DO NOT USE THIS OPTION! This is used to see the thresholds and the values mapped by between them
        """
        #IMOROVE GRAPH WITH ALL THE THRESHOLDS
        if (thresholds[0] < minData):
            minData = thresholds[0]
            
        if (thresholds[2] > maxData):
            maxData = thresholds[2]
        """ 
        
        
        #We will plot the lines between the max and the min on the window within the space bewteen the emoticon and the bottom of the window
        spaceBetweenDots = self.get_width() - (2 * 10)
        spaceBetweenDots = (spaceBetweenDots / data.__len__())
        dotID = 0
        
        #The color
        color = [224, 17, 95]
        
        #Note: We let 10 pixels empty around the graph to see it clearly
        
        for d in data:
            #We begin the loop at the id 1
            if (dotID != 0):
                #Here 10 is the empty border width we use to see the graph clearly
                x1 = 10 + (spaceBetweenDots * (dotID - 1))
                x2 = 10 + (spaceBetweenDots * dotID)
                
                #If the maxData == minData then we reduce the maxData a little bit, not to have a division by zero when using the map method
                if (maxData == minData):
                    maxData += 0.01
                    
                #The heightMax value is the space between the bottom of the window and the bottom of the Emoticon (with an empty border of 10 pixels as we said earlier)
                heightMax = self.get_height() - (self.getButtonHeight() + 2 * self.emoticonBorder + self.emoticonSize + 2 * 10)
                
                y1 = self.get_height() - 10 - Sensor.mapValue(data[dotID - 1], minData, maxData, 0, heightMax)
                y2 = self.get_height() - 10 - Sensor.mapValue(data[dotID], minData, maxData, 0, heightMax)
                
                #Draw the lines of the graphs                
                pygame.draw.line(self.screen, color, [x1, y1], [x2, y2], 2)
                
                #WE DO NOT USE THIS OPTION! This is used to see the thresholds and the values mapped by between them
                """"
                First threshold
                pygame.draw.line(self.screen, [255, 255, 0], [10, (self.get_height() - 10 - Sensor.mapValue(thresholds[0], minData, maxData, 0, heightMax))], [self.get_width() - 10, (self.get_height() - 10 - Sensor.mapValue(thresholds[0], minData, maxData, 0, heightMax))], 2)
                
                Second threshold
                pygame.draw.line(self.screen, [255, 0, 255], [10, (self.get_height() - 10 - Sensor.mapValue(thresholds[1], minData, maxData, 0, heightMax))], [self.get_width() - 10, (self.get_height() - 10 - Sensor.mapValue(thresholds[1], minData, maxData, 0, heightMax))], 2)
                
                Last threshold
                pygame.draw.line(self.screen, [0, 255, 255], [10, (self.get_height() - 10 - Sensor.mapValue(thresholds[2], minData, maxData, 0, heightMax))], [self.get_width() - 10, (self.get_height() - 10 - Sensor.mapValue(thresholds[2], minData, maxData, 0, heightMax))], 2)
                """
                
            dotID += 1