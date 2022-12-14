import sys
import pygame
from feur import *
import player
from pygame.locals import *
pygame.init()

def joy():
    pygame.joystick.init() #initialise le module joystick
    joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
    #Permet de savoir le nombre de manettes utilisés
    for joystick in joysticks:
        print(joystick.get_name()) #Permet de connaitre la manette utilisée.
    return joysticks

#A compléter en fonction de l'action qui doit être effectuée
def touches(event):
    """
    Permet d'effectuer l'action une action lorsqu'une touche est pressée.
    """
    if event.button == 0:
        print(event)
        
        
        
    if event.button == 1:
        print(event)


    if event.button == 2:
        print(event)

    if event.button == 3:
        print(event)

    if event.button == 4:
        print(event)
