"""stocke toutes les textures afin de ne pas faire beuger pygame"""
import pygame
from data.modules.settings import read_settings


def load_image(path, dimensions):
    """charge l'image et modifie les dimensions de cette dernière"""
    temp = pygame.image.load(path+".png")
    temp = pygame.transform.scale(temp, dimensions)
    return temp

prop = read_settings()
win_scale = (prop["display"]["horizontal"], prop["display"]["vertical"])
fps = prop["display"]["FPS"]

pygame.display.init()
pygame.display.set_mode(win_scale)

UI_PATH = "data/gfx/ui/"
LEVELS_PATH = "data/gfx/levels/"

# convert permet de blit les images plus rapidement
# et convert_alpha fait la même chose pour les images transparentes

TEXTURES = {}
# chargements des texures de menu
TEXTURES["blur"] = load_image(UI_PATH+"blur", win_scale).convert_alpha()
TEXTURES["loading"] = load_image(UI_PATH+"loading", win_scale).convert()
TEXTURES["exit"] = load_image(UI_PATH+"exit_btn", (360,180)).convert()

# chargement des textures de jeu
TEXTURES["neo_tokyo"] = {}
TEXTURES["neo_tokyo"]["bg"] = load_image(LEVELS_PATH+"neo_tokyo", win_scale).convert()