"""this module contains the launcher of Moissan Fighter Z"""
import pygame
from data.levels import neo_tokyo

pygame.mixer.init()

pack_pygame = {
    "FPS" : 60,
    "display" : pygame.display,
    "mixer" : pygame.mixer,
    "clock" : pygame.time.Clock()
}

pygame.init()

FPS = pack_pygame["FPS"]

map = neo_tokyo.NeoTokyo(pack_pygame)

WIN = True

start_time = 0
while WIN:
    dt = pack_pygame["clock"].tick(FPS)
    #dt est le temps qui s'écoule entre chaque image

pygame.quit()
