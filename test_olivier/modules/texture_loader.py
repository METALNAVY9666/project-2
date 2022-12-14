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
# Images pour le menu
images["background"] = load_image(
    BG_PATH+'map_tuto.jpg', (1080, 720)).convert()
images["square"] = load_image(BG_PATH+'square.png', (120, 120))

# Chargement des images pour les joueurs
persos = {}
persos["goku"] = pg.image.load('test_olivier/gfx/goku/base_left.png')
persos["vegeta"] = pg.image.load('test_olivier/gfx/base/vegeta_base.png')
persos["hello"] = pg.image.load('test_olivier/gfx/base/goku_base.png')
# Images retournées
persos["vegeta_right"] = pg.transform.flip(persos["vegeta"], True, False)
persos["goku_right"] = pg.image.load('test_olivier/gfx/goku/base_right.png')


def sprites_images(name):
    '''Cette fonction récupère les chemins des images des persos.'''
    dict = {'attack': pg.image.load(f'test_olivier/gfx/{name}/attack.png'),
            'right': pg.image.load(f'test_olivier/gfx/{name}/right.png'),
            'left': pg.image.load(f'test_olivier/gfx/{name}/left.png'), }
    return dict
