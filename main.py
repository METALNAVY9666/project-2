"""this module contains the launcher of Moissan Fighter Z"""
import pygame
from data.levels import neo_tokyo

pack_pygame = {
    "pygame": pygame,
    "FPS": 60,
    "display": pygame.display,
    "surface": pygame.display.set_mode([1280, 720]),
    "mixer": pygame.mixer,
    "clock": pygame.time.Clock()
}

pygame.init()
pygame.mixer.init()

FPS = pack_pygame["FPS"]
WIN = True

current_map = neo_tokyo.NeoTokyo(pack_pygame)

while WIN:
    # dt est le temps qui s'écoule entre chaque image,
    # important pour que le jeu reste fluide
    dt = pack_pygame["clock"].tick(FPS)
    # vérifie les évènements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            WIN = False
    # actualise la map, si elle renvoie "quit", alors quitter
    if current_map.update() == "quit":
        WIN = False

pygame.quit()
