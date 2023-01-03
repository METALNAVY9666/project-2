"""stocke toutes les textures avant le lancement du jeu"""
import pygame as pg

pg.display.init()
surface = pg.display.set_mode((1080, 720))


def load_image(path, dimensions):
    """charge l'image et modifie les dimensions de cette dernière"""
    temp = pg.image.load(path)
    temp = pg.transform.scale(temp, dimensions)
    return temp


def sprites_images(name):
    '''Cette fonction récupère les chemins des images des persos.'''
    dict = {'attack': pg.image.load(f'test_olivier/gfx/{name}/attack.png'),
            'right': pg.image.load(f'test_olivier/gfx/{name}/right.png'),
            'left': pg.image.load(f'test_olivier/gfx/{name}/left.png'),
            'jump': pg.image.load(f'test_olivier/gfx/{name}/jump_left.png'),
            'jump_right': pg.image.load(f'test_olivier/gfx/{name}/jump_right.png')}
    return dict


# Chargements des images pour le fond d'écran
BG_PATH = 'test_olivier/gfx/images/'
images = {}
# Images pour le menu
images["background"] = load_image(
    BG_PATH+'map_tuto.jpg', (1080, 720)).convert()
images["square"] = load_image(BG_PATH+'square.png', (120, 120))
images['punchingball'] = load_image(BG_PATH+'image.png', (120, 120))
images['hit'] = load_image(BG_PATH+'punched.png', (120, 120))

# Chargement des images pour les joueurs
def sprite_tab(name):
    tab = [pg.image.load(f'test_olivier/gfx/{name}/base_left0.png'),
           pg.image.load(f'test_olivier/gfx/{name}/base_left1.png'),
           pg.image.load(f'test_olivier/gfx/{name}/base_left2.png'),
           pg.image.load(f'test_olivier/gfx/{name}/base_left3.png'),
           pg.image.load(f'test_olivier/gfx/{name}/base_left4.png'),
           pg.image.load(f'test_olivier/gfx/{name}/base_left5.png')]
    return tab
# Chargement image de droite
def sprite_tab_right(name):
    tab = [pg.image.load(f'test_olivier/gfx/{name}/base_right0.png'),
           pg.image.load(f'test_olivier/gfx/{name}/base_right1.png'),
           pg.image.load(f'test_olivier/gfx/{name}/base_right2.png'),
           pg.image.load(f'test_olivier/gfx/{name}/base_right3.png'),
           pg.image.load(f'test_olivier/gfx/{name}/base_right4.png'),
           pg.image.load(f'test_olivier/gfx/{name}/base_right5.png')]
    return tab