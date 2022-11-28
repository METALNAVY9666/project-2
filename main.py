"""ce module contient le lanceur de jeu"""
import pygame
from data.modules import levels
from data.modules.settings import read_settings

game_settings = read_settings()
x = game_settings["display"]["horizontal"]
y = game_settings["display"]["vertical"]
dimensions = (x, y)

pack_pygame = {
    "pygame": pygame,
    "FPS": 60,
    "display": pygame.display,
    "surface": pygame.display.set_mode(dimensions),
    "mixer": pygame.mixer,
    "clock": pygame.time.Clock(),
    "time": pygame.time
}

icon = pygame.image.load("data/gfx/icon.png")

pygame.init()
pygame.mixer.init()
pygame.display.set_icon(icon)

FPS = pack_pygame["FPS"]
WIN = True

levels_options = {
            "NeoTokyo": {
                "scale": dimensions,
                "bg": "data/gfx/levels/neo_tokyo.png",
                "music": "data/sfx/music/neo_tokyo.mp3"}
                }

level = levels_options["NeoTokyo"]

current_map = levels.BaseLevel(pack_pygame, level, game_settings)

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
