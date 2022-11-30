"""ce module contient le lanceur de jeu"""
import pygame
from data.modules.levels import BaseLevel
from data.modules.settings import read_settings

game_settings = read_settings()
x = game_settings["display"]["horizontal"]
y = game_settings["display"]["vertical"]
dimensions = (x, y)

pack_pygame = {
    "pygame": pygame,
    "FPS": game_settings["display"]["FPS"],
    "display": pygame.display,
    "surface": pygame.display.set_mode(dimensions),
    "mixer": pygame.mixer,
    "clock": pygame.time.Clock(),
    "time": pygame.time,
    "mouse": pygame.mouse,
    "rect": pygame.Rect
}

icon = pygame.image.load("data/gfx/icon.png")

pygame.init()
pygame.mixer.init()
pygame.display.set_icon(icon)

WIN = True

levels_options = {
            "neo_tokyo": {
                "scale": dimensions,
                "bg": "neo_tokyo",
                "music": "data/sfx/music/neo_tokyo.mp3"}
                }

level = levels_options["neo_tokyo"]

current_map = BaseLevel(pack_pygame, level, game_settings)

while WIN:
    # dt est le temps qui s'écoule entre chaque image,
    # important pour que le jeu reste fluide
    dt = pack_pygame["clock"].tick(pack_pygame["FPS"])
    current_map.dt = dt
    # vérifie les évènements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            WIN = False
        if event.type == pygame.KEYDOWN:
            # vérifie si la touche F11 est enfoncée et met en plein écran
            if event.key == pygame.K_F11:
                current_map.pkg["display"].toggle_fullscreen()
    # actualise la map, si elle renvoie "quit", alors quitter
    if current_map.update() == "exit":
        WIN = False

pygame.quit()
# os.system("clear")
