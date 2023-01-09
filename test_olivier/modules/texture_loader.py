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
    sprites_dict = {'right': pg.image.load(f'test_olivier/gfx/{name}/right.png'),
                    'left': pg.image.load(f'test_olivier/gfx/{name}/left.png'),
                    'jump': pg.image.load(f'test_olivier/gfx/{name}/jump_left.png'),
                    'jump_right': pg.image.load(f'test_olivier/gfx/{name}/jump_right.png')}
    return sprites_dict


# Chargements des images pour le fond d'écran
BG_PATH = 'test_olivier/gfx/images/'
images = {}
# Images pour le menu
images["background"] = load_image(
    BG_PATH+'map_tuto.jpg', (1080, 720)).convert()
images["square"] = load_image(BG_PATH+'square.png', (160, 160))
images['punchingball'] = load_image(BG_PATH+'image.png', (120, 120))
images['hit'] = load_image(BG_PATH+'punched.png', (120, 120))
images['goku_face'] = load_image(BG_PATH+'face_goku.png', (90, 90))
images['vegeta_face'] = load_image(BG_PATH+'face_vegeta.png', (90, 90))

# Chargement des images pour les joueurs


def sprite_tab(name, position):
    '''Fonction qui permet de charger les images à gauche ou à gauche
    A besoin d'un nom de perso, ainsi que du nom de l'action qu'il réalise'''
    # Name est le nom du perso, position permet de savoir si il est à gauche ou non
    tab = [pg.image.load(f'test_olivier/gfx/{name}/base_{position}0.png'),
           pg.image.load(f'test_olivier/gfx/{name}/base_{position}1.png'),
           pg.image.load(f'test_olivier/gfx/{name}/base_{position}2.png'),
           pg.image.load(f'test_olivier/gfx/{name}/base_{position}3.png'),
           pg.image.load(f'test_olivier/gfx/{name}/base_{position}4.png'),
           pg.image.load(f'test_olivier/gfx/{name}/base_{position}5.png')]
    return tab

bro_tab = ["C'est quoi la blague ?",
           "C'est un peu bêbête",
           "You fuck my wife ?",
           "C'est un truc d'autiste ça",
           "Alors, j'enlève cette merde",
           "Au procès, je gagne !",
           "Je vais faire sonner le gros Ben",
           "Je fais donc péter le logarithme",
           "Je fais donc péter l'exponentielle",]