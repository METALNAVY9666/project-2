"""ce module contient le lanceur de jeu"""
import pygame
from data.modules.levels import BaseLevel
from data.modules.settings import read_settings, read_levels
from data.modules.debug import FPS
from data.modules.controllers import manage_controller, manage_joysticks
import pygame._sdl2
pygame.joystick.init()
pygame.init()

contro = []
contro = manage_controller(contro)
joysticks = manage_joysticks()


game_settings = read_settings()
x = game_settings["display"]["horizontal"]
y = game_settings["display"]["vertical"]
dimensions = [x, y]


pack_pygame = {
    "pygame": pygame,
    "FPS": game_settings["display"]["FPS"],
    "display": pygame.display,
    "surface": pygame.display.set_mode(dimensions),
    "Rect": pygame.Rect,
    "mixer": pygame.mixer,
    "clock": pygame.time.Clock(),
    "time": pygame.time,
    "mouse": pygame.mouse,
    "rect": pygame.Rect,
    "key": pygame.key,
    "transform": pygame.transform,
    "dimensions": dimensions
}

icon = pygame.image.load("data/gfx/icon.png")

pygame.init()
pygame.mixer.init()
pygame.display.set_icon(icon)
y
WIN = True

level = read_levels()["tenkaichi_budokai"]

current_map = BaseLevel(pack_pygame, level, game_settings)
fps = FPS(pack_pygame)

while WIN:
    # dt est le temps qui s'écoule entre chaque image,
    # important pour que le jeu reste fluide
    dlt = pack_pygame["clock"].tick(pack_pygame["FPS"])
    current_map.delta = dlt
    # Récupère les événements courants
    actions = pygame.event.get()
    # vérifie les évènements
    for event in actions:
        if event.type == pygame.QUIT:
            WIN = False
        if event.type == pygame.KEYDOWN:
            # vérifie si la touche F11 est enfoncée et met en plein écran
            if event.key == pygame.K_F11:
                current_map.pkg["display"].toggle_fullscreen()
    # actualise la map, si elle renvoie "quit", alors quitter
    if current_map.update(dlt, actions, contro) == "exit":
        WIN = False
    fps.record_fps()

print(fps.end())
pygame.quit()
# os.system("clear")
