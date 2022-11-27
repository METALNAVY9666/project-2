"""ce module contient le lanceur de jeu"""
import pygame
from data.modules import levels

pack_pygame = {
    "pygame": pygame,
    "FPS": 60,
    "display": pygame.display,
    "surface": pygame.display.set_mode([1280, 720]),
    "mixer": pygame.mixer,
    "clock": pygame.time.Clock(),
    "time": pygame.time
}

pygame.init()
pygame.mixer.init()

FPS = pack_pygame["FPS"]
WIN = True

levels_options = {
            "NeoTokyo": {
                "scale": (1280, 720),
                "bg": "data/gfx/levels/neo_tokyo.png",
                "music": "data/sfx/music/neo_tokyo.mp3"}
                }

level = levels_options["NeoTokyo"]

current_map = levels.BaseLevel(pack_pygame, level)

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
