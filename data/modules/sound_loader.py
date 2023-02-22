from os import listdir
import pygame
from data.modules.settings import read_settings, read_levels

SFX = {}
pygame.mixer.init()

# initialise les sons de kim
PATH = "data/sfx/kim/"
for file in listdir(PATH):
    name = file[0:-4]
    SFX[name] = pygame.mixer.Sound(PATH + file)
    if name == "shoot":
        SFX[name].set_volume(0.25)
