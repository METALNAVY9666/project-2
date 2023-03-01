"""ce module contient le lanceur de jeu"""
import pygame
import pygame._sdl2
from data.modules.levels import BaseLevel
from data.modules.settings import read_settings, read_levels
from data.modules.debug import FPS
from data.modules.controllers import manage_controller, manage_joysticks
from data.modules.menu.main import debut as menu
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
    "surface": pygame.display.set_mode([1280, 720]),
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

pygame.mixer.init()

while True:
    WIN = True

    level_name, players = menu()

    pack_pygame["surface"] = pygame.display.set_mode(dimensions)

    level = read_levels()[level_name]

    current_map = BaseLevel(pack_pygame, level, game_settings, players)
    fps = FPS(pack_pygame)

    pack_pygame["mouse"].set_visible(True)
    pack_pygame["display"].set_caption(f"Moissan Fighters - {level_name}")
    pygame.display.set_icon(icon)

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
        next_action = current_map.update(dlt, actions, contro, actions)
        if next_action == "exit":
            WIN = False
        fps.record_fps()
