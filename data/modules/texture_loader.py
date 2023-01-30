"""stocke toutes les textures afin de ne pas faire beuger pygame"""
from os import listdir
import pygame as pg
from data.modules.settings import read_settings, read_levels


def load_image(path=str, dimensions=None):
    """charge l'image et modifie les dimensions de cette dernière"""
    image = pg.image.load(path+".png")
    return resize(image, dimensions)

def resize(image, dimensions):
    """redimensionne l'image"""
    if dimensions is None:
        return image
    return pg.transform.scale(image, dimensions)

def load_dir(path=str, dimensions=tuple):
    """renvoie un dictionnaire nom/sprite de tout les sprites
    contenus dans un dossier"""
    sprites = {}
    for file in listdir(path):
        name = file[0:-4]
        image = load_image(path+name)
        image = resize(image, dimensions)
        image.convert_alpha()
        sprites[name] = image
    return sprites

def convert_alpha_dict(dicti):
    """renvoie le dictionnaire de sprites convertis"""
    keys = list(dicti.keys())
    new = {}
    for key in keys:
        new[key] = resize(dicti[key], (X//12, Y//12))
        new[key].convert_alpha()
    return new

def sprites_images(name):
    '''Cette fonction récupère les chemins des images des persos.'''
    sprites_dict = {'right': pg.image.load(f'test_olivier/gfx/{name}/right.png'),
                    'left': pg.image.load(f'test_olivier/gfx/{name}/left.png'),
                    'jump': pg.image.load(f'test_olivier/gfx/{name}/jump_left.png'),
                    'jump_right': pg.image.load(f'test_olivier/gfx/{name}/jump_right.png'),
                    'shield': pg.image.load(f'test_olivier/gfx/{name}/block.png'),
                    'shield_right': pg.image.load(f'test_olivier/gfx/{name}/block_right.png')}
    
    return convert_alpha_dict(sprites_dict)


def sprite_tab(name, position):
    '''Fonction qui permet de charger les images à gauche ou à gauche
    A besoin d'un nom de perso, ainsi que du nom de l'action qu'il réalise'''
    # Name est le nom du perso, position permet de savoir si il est à gauche ou non
    tab = [None] * 6
    scale = (X//12, Y//12)
    for ind in range(6):
        string = f'test_olivier/gfx/{name}/base_{position}{ind}'
        tab[ind] = load_image(string, scale)
        tab[ind].convert_alpha()
    return tab


levels = read_levels()
prop = read_settings()
X = prop["display"]["horizontal"]
Y = prop["display"]["vertical"]
win_scale = (X, Y)
fps = prop["display"]["FPS"]

pg.display.init()
surface = pg.display.set_mode(win_scale)


UI_PATH = "data/gfx/ui/"
LEVELS_PATH = "data/gfx/levels/"
EVENTS_PATH = "data/gfx/events/"
BG_PATH = "data/gfx/images/"

# convert permet de blit les images plus rapidement
# et convert_alpha fait la même chose pour les images transparentes

GFX = {}
GFX["loading"] = load_image(UI_PATH+"loading", win_scale).convert()

# affichage écran de chargement
loading_rect = surface.blit(GFX["loading"], (0, 0))
pg.display.update(loading_rect)

# chargement des texures du menu pause
GFX["blur"] = load_image(UI_PATH+"blur", win_scale).convert_alpha()
GFX["exit"] = load_image(UI_PATH+"exit_btn", (X//8, Y//10)).convert()

# chargement des évènements
for number in ["one", "two", "three", "go"]:
    GFX[number] = load_image(UI_PATH+number, (X//6, Y//6)).convert_alpha()
GFX["ae86"] = load_image(EVENTS_PATH+"trueno_drift/ae86", (X//6, Y//6))
GFX["ae86"].convert_alpha()

# chargement des niveaux
for level in list(levels.keys()):
    GFX[level] = {}
    TEMP = LEVELS_PATH + level
    GFX[level]["bg"] = load_image(TEMP, levels[level]["scale"]).convert()

# chargement des textures des obstacles
path = LEVELS_PATH+"platform"
GFX["platform"] = load_image(path, (X//1.5, Y//1.5)).convert_alpha()

# Images pour le menu
GFX['punchingball'] = load_image(BG_PATH+'image', (120, 120)).convert_alpha()
GFX['hit'] = load_image(BG_PATH+'punched', (120, 120)).convert_alpha()

bro_tab = ["C'est quoi la blague ?",
           "C'est un peu bêbête",
           "You fuck my wife ?",
           "C'est un truc d'autiste ça",
           "Alors, j'enlève cette merde",
           "Au procès, je gagne !",
           "Je vais faire sonner le gros Ben",
           "Je fais donc péter le logarithme",
           "Je fais donc péter l'exponentielle", ]

GFX["kim"] = load_dir("data/gfx/players/kim/", (X//12, Y//12))