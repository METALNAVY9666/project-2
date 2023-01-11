import pygame 
from pygame.locals import *
pygame.init()


pygame.joystick.init() #initialise le module joystick
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
#Permet de savoir le nombre de manettes utilisés
for joystick in joysticks:
    print(joystick.get_name()) #Permet de connaitre la manette utilisée.