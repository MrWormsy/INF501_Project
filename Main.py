# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 19:47:50 2017

@author: lfoul, Antonin ROSA-MARTIN (aka MrWormsy) and IGIRANEZA Beda
"""

import pygame
from GeneralConfiguration import GeneralConfiguration
from Sensor import Sensor

def main():

    # Creates an instance of the class GeneralConfiguration
    generalConfiguration = GeneralConfiguration()
    
    #Add all the sensors needed
    generalConfiguration.addSensor(
        Sensor(
            'http://www.polytech.univ-smb.fr/apps/myreader/capteur.php?capteur=epua_b204_clim', 
            'Temp. Clim B204',
            [20, 22, 23]
        )
    )
        
    generalConfiguration.addSensor(
        Sensor(
            'http://www.polytech.univ-smb.fr/apps/myreader/capteur.php?capteur=epua_b204_coursive', 
            'Temp. Coursive B204',
            [20, 22, 23]
        )
    )
        
    generalConfiguration.addSensor(
        Sensor(
            'http://www.polytech.univ-smb.fr/apps/myreader/capteur.php?capteur=epua_b204_centre', 
            'Temp. Centre B204',
            [20, 22, 23]
        )
    )
        
    generalConfiguration.addSensor(
        Sensor(
            'http://www.polytech.univ-smb.fr/apps/myreader/capteur.php?capteur=epua_toiture', 
            'Temp. Toiture',
            [30, 35, 40]
        )
    )
        
    generalConfiguration.addSensor(
        Sensor(
            'http://www.polytech.univ-smb.fr/apps/myreader/capteur.php?capteur=epua_onduleur1_watts', 
            'Puissance Ondulateur',
            [10000, 12000, 15000]
        )
    )
        
    #This method centers all the button (set their right position)
    generalConfiguration.centerButtons()
    
    # Infinite loop    
    while True:

        # Waits for an event
        event = pygame.event.wait()
        
        # Checks if the user wants to quit
        if event.type == pygame.QUIT:
            pygame.quit()
            break 
                               
        # Checks if the user has clicked with the mouse               
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Checks if the display of a new sensor is required
            generalConfiguration.checkIfSensorChanged(event.pos)
            
        #Else we display everything and update the graph
        else:
            generalConfiguration.display()
        
# Calls the main function
if __name__ == "__main__":
    main()    