"""stocke toutes les textures afin de ne pas faire beuger pygame"""
import pygame as pg

pg.display.init()
surface = pg.display.set_mode((1080, 720))
def load_image(path, dimensions):
    """charge l'image et modifie les dimensions de cette dernière"""
    temp = pg.image.load(path)
    temp = pg.transform.scale(temp, dimensions)
    return temp


# Chargements des images pour le fond d'écran
BG_PATH = 'test_olivier/gfx/images/'
images = {}
images["background"] = load_image(BG_PATH+'map_tuto.jpg', (1080, 720)).convert()
images["square"] = load_image(BG_PATH+'square.png', (120, 120))

# Chargement des images pour les joueurs
PL_PATH = 'test_olivier/gfx/base/'
persos = {}
persos["goku"] = pg.image.load('test_olivier/gfx/base/goku_base.png')
persos["vegeta"] = pg.image.load('test_olivier/gfx/base/vegeta_base.png')
