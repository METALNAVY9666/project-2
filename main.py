"""ce module contient le lanceur de jeu"""
import pygame
from data.modules.levels import BaseLevel
from data.modules.settings import read_settings, read_levels
from data.modules.debug import FPS
from data.modules.controllers import manage_controller, manage_joysticks
from data.modules.menu.main import debut as menu
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
    "dimensions": dimensions,
    "events": pygame.event.get
}

icon = pygame.image.load("data/gfx/icon.png")

pygame.init()
pygame.mixer.init()
pygame.display.set_icon(icon)

WIN = True

level_name, players = menu()

level = read_levels()[level_name]

current_map = BaseLevel(pack_pygame, level, game_settings, players)
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
        if event.type in [pygame.JOYDEVICEADDED, pygame.JOYDEVICEREMOVED]:
            joysticks = manage_joysticks()
            contro = manage_controller([])
    # actualise la map, si elle renvoie "quit", alors quitter
    if current_map.update(dlt, actions, contro) == "exit":
        WIN = False
    fps.record_fps()

print(fps.end())
pygame.quit()
# os.system("clear")
