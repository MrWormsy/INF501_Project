# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 19:47:50 2017

@author: lfoul, Antonin ROSA-MARTIN (aka MrWormsy) and IGIRANEZA Beda
"""

import http.client
from urllib.parse import urlparse
import socket

class Sensor:
    
    """
    A Sensor is represented as a URL, a label and a list of threshold
    """
    def __init__(self, url, label, thresholds):
        self.url = url
        self.label = label
        self.thresholds = thresholds

    """
    Set a GeneralConfiguration to the Sensor
    setGeneralConfiguration : Sensor, GeneralConfiguration --> None
    """
    def setGeneralConfiguration(self, generalConfiguration):
        self.generalConfiguration = generalConfiguration

    """
    Set an Emoticon to the Sensor with the emoticon parameters
    setEmoticon : Sensor, Emoticon --> None
    """
    def setEmoticon(self, emoticon):
        self.emoticon = emoticon
        self.emoticon.setEmoticonParameters(self.generalConfiguration.getEmoticonSize())

    """
    Set a Button to the Sensor
    setButton : Sensor, Button --> None
    """
    def setButton(self, button):
        self.button = button

    """
    Set a id to the Sensor
    setSensorId : Sensor, int --> None
    """
    def setSensorId(self, sensorId):
        self.sensorId = sensorId
        
    """
    Set a value to the Sensor
    setSensorValue : Sensor, float --> None
    """
    def setSensorValue(self, sensorValue):
        self.sensorValue = sensorValue

    """
    Get the GeneralConfiguration of the Sensor
    getGeneralConfiguration : Sensor --> GeneralConfiguration
    """
    def getGeneralConfiguration(self):
        return self.generalConfiguration

    """
    Get the id of the Sensor
    getSensorId : Sensor --> int
    """
    def getSensorId(self):
        return self.sensorId

    """
    Get the label of the Sensor
    getLabel : Sensor --> String
    """
    def getLabel(self):
        return self.label
    
    """
    Get the value of the Sensor
    getSensorValue : Sensor --> float
    """
    def getSensorValue(self):
        return self.sensorValue
    
    """
    Get the thresholds of the Sensor
    getSensorValue : Sensor --> List
    """
    def getThresholds(self):
        return self.thresholds
                     
    """
    Checks if the connection to the sensor is set (return True if set, False otherwise)
    isConnectedToUrl : Sensor --> boolean
    """
    def isConnectedToUrl(self):
        self.parsedUrl = urlparse(self.url)
        self.connection = http.client.HTTPSConnection(self.parsedUrl.netloc)
        try:
            self.connection.request('GET', self.url)
        except socket.error:
            return False
        else: 
            self.response = self.connection.getresponse()
        return self.response.status == http.client.OK
        
    """
    Reads the sensor and return the float value if the connection is set
    read : Sensor --> float
    """
    def read(self):
        if self.isConnectedToUrl():
            #We replace b and ' with nothing to get the float value
            return float(str(self.response.read()).replace("b", "").replace("'", ""))
        else:
            return None
    
    """
    Map a value between two starting values to a value between two target values
    mapValue : float, float, float, float, float --> float
    """
    def mapValue(value, minA, maxA, minB, maxB):
        return minB + (((value - minA)*(maxB - minB))/(maxA - minA))
        
    """
    Map the value read by the sensor according to what the instructions and return it beween -1 and 1
    getTransformedValue : Sensor --> float
    """
    def getTransformedValue(self):
        
        value = float(self.read())
        
        if (value == self.thresholds[1]) :
            return 0
        elif (value < self.thresholds[0]):
            return -1
        elif (value > self.thresholds[2]):
            return 1
        elif (value > self.thresholds[0] and value < self.thresholds[1]):
            return (Sensor.mapValue(value, self.thresholds[0], self.thresholds[1], 0.0, 1.0) - 1)
        else:
            return (Sensor.mapValue(value, self.thresholds[1], self.thresholds[2], 0.0, 1.0))
        
        
        
    """
    Draws the Emoticon of the Sensor according to the transformed value
    drawEmoticon : Sensor --> None
    """
    def drawEmoticon(self):
        self.emoticon.draw(self.getTransformedValue())

    """
    Draws the Button of the Sensor
    drawButton : Sensor --> None
    """
    def drawButton(self):
        self.button.draw()
            
                   
        