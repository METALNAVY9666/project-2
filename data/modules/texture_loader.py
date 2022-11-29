"""stocke toutes les textures afin de ne pas faire beuger pygame"""
import pygame
from data.modules.settings import read_settings


def load_image(path, dimensions):
    """charge l'image et modifie les dimensions de cette dernière"""
    temp = pygame.image.load(path+".png")
    temp = pygame.transform.scale(temp, dimensions)
    return temp


prop = read_settings()
X = prop["display"]["horizontal"]
Y = prop["display"]["vertical"]
win_scale = (X, Y)
fps = prop["display"]["FPS"]

pygame.display.init()
surface = pygame.display.set_mode(win_scale)


UI_PATH = "data/gfx/ui/"
LEVELS_PATH = "data/gfx/levels/"

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

# chargement des GFX de neo_tokyo
GFX["neo_tokyo"] = {}
TEMP = LEVELS_PATH+"neo_tokyo"
GFX["neo_tokyo"]["bg"] = load_image(TEMP, win_scale).convert()
