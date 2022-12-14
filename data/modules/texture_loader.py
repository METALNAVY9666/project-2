"""stocke toutes les textures afin de ne pas faire beuger pygame"""
import pygame
from data.modules.settings import read_settings, read_levels


def load_image(path, dimensions):
    """charge l'image et modifie les dimensions de cette dernière"""
    temp = pygame.image.load(path+".png")
    if dimensions is not None:
        temp = pygame.transform.scale(temp, dimensions)
    return temp

levels = read_levels()
prop = read_settings()
X = prop["display"]["horizontal"]
Y = prop["display"]["vertical"]
win_scale = (X, Y)
fps = prop["display"]["FPS"]

pygame.display.init()
surface = pygame.display.set_mode(win_scale)


UI_PATH = "data/gfx/ui/"
LEVELS_PATH = "data/gfx/levels/"
EVENTS_PATH = "data/gfx/events/"

# convert permet de blit les images plus rapidement
# et convert_alpha fait la même chose pour les images transparentes

GFX = {}
GFX["loading"] = load_image(UI_PATH+"loading", win_scale).convert()
# affichage écran de chargement
loading_rect = surface.blit(GFX["loading"], (0, 0))
pygame.display.update(loading_rect)

# chargements des texures de menu
GFX["blur"] = load_image(UI_PATH+"blur", win_scale).convert_alpha()
GFX["exit"] = load_image(UI_PATH+"exit_btn", (X//8, Y//10)).convert()

# chargements de évènements
for number in ["one", "two", "three", "go"]:
    GFX[number] = load_image(UI_PATH+number, (X//6, Y//6)).convert_alpha()
GFX["ae86"] = load_image(EVENTS_PATH+"trueno_drift/ae86", (X//6, Y//6))
GFX["ae86"].convert_alpha()

# chargement des niveaux
for level in list(levels.keys()):
    GFX[level] = {}
    TEMP = LEVELS_PATH + level
    GFX[level]["bg"] = load_image(TEMP, levels[level]["scale"]).convert()

# textures test
GFX["players"] = {}
TEMP = "data/gfx/test/"
GFX["players"]["nyan"] = load_image(TEMP+"nyan_cat", (100, 100)).convert()
