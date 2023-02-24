"""stocke toutes les textures afin de ne pas faire beuger pygame"""
from os import listdir
import pygame as pg
from data.modules.settings import read_settings, read_levels



def load_image(filepath=str, dimensions=None):
    """charge l'image et modifie les dimensions de cette dernière"""
    image = pg.image.load(filepath + ".png")
    return resize(image, dimensions)


def resize(image, dimensions):
    """redimensionne l'image"""
    if dimensions is None:
        return image
    return pg.transform.scale(image, dimensions)


def load_dir(filepath=str, dimensions=tuple):
    """renvoie un dictionnaire nom/sprite de tout les sprites
    contenus dans un dossier"""
    sprites = {}
    for file in listdir(filepath):
        name = file[0:-4]
        image = load_image(filepath + name)
        image = resize(image, dimensions)
        image.convert_alpha()
        sprites[name] = image
    return sprites

def convert_alpha_dict(dicti, size):
    """renvoie le dictionnaire de sprites convertis"""
    keys = list(dicti.keys())
    new = {}
    for key in keys:
        new[key] = resize(dicti[key], size)
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
    dict_size = {"itachi": (X // 9, Y // 8),
                 "goku": (X // 9,  Y // 10),
                 "luffy": (X // 9, Y // 10),
                 "gear4": (X // 9, Y // 10),
                 "vegeta": (X // 9, Y // 10),
                 "revive": (X // 14, Y // 8)}
    size = dict_size[name]
    return convert_alpha_dict(sprites_dict, size)


def sprite_tab(name, position):
    '''Fonction qui permet de charger les images à gauche ou à gauche
    A besoin d'un nom de perso, ainsi que du nom de l'action qu'il réalise'''
    # Name est le nom du perso, position permet de savoir si il est à gauche
    # ou non
    dict_size = {"itachi": (X // 10, X // 12),
                 "goku": (X // 9, X // 10),
                 "luffy": (X // 9, X // 10),
                 "gear4": (X // 9, X // 10),
                 "vegeta": (X // 9, X // 10),
                 "revive": (X // 14, X // 12)}
    tab = [None] * 6
    scale = dict_size[name]
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
EFFECTS_PATH = "data/gfx/effects/"
BUTTONS_PATH = UI_PATH + "buttons/"

# convert permet de blit les images plus rapidement
# et convert_alpha fait la même chose pour les images transparentes

GFX = {}
GFX["loading"] = load_image(UI_PATH + "loading", win_scale).convert()

# affichage écran de chargement
loading_rect = surface.blit(GFX["loading"], (0, 0))
pg.display.update(loading_rect)

# charge la police
pg.font.init()
GFX["font"] = pg.font.Font('test_olivier/gfx/fonts/04B_19__.TTF', 60)
GFX["paladins"] = pg.font.Font('data/gfx/fonts/paladins.ttf', 60)

# chargement des boutons et du menu pause.
GFX["blur"] = load_image(UI_PATH + "blur", win_scale).convert_alpha()
GFX["btn"] = load_dir(BUTTONS_PATH, (X // 8, Y // 10))

# chargement des évènements
for number in ["one", "two", "three", "go"]:
    GFX[number] = (load_image(UI_PATH + number, (X // 6, Y // 6)).convert_alpha())
GFX["ae86"] = load_image(EVENTS_PATH + "trueno_drift/ae86", (X // 6, Y // 6))
GFX["ae86"].convert_alpha()

GFX["kim_ult"] = load_image(EVENTS_PATH + "kim_ult/meme", (X // 2, Y // 2))
GFX["kim_ult"].convert()

# chargement des effets visuels
GFX["nuzzle"] = load_image(EFFECTS_PATH + "nuzzle", (X // 54, Y // 54))
GFX["nuzzle"].convert_alpha()

GFX["explosion"] = load_image(EFFECTS_PATH + "explosion", (X // 16, Y // 8))
GFX["explosion"].convert_alpha()

GFX["bullets"] = {}
GFX["bullets"]["makarov"] = load_image(EFFECTS_PATH + "bullet_makarov", (X // 40, Y // 40))
GFX["bullets"]["makarov"].convert_alpha()

GFX["bullets"]["barrett"] = load_image(EFFECTS_PATH + "bullet_barrett", (X // 64, Y // 144))
GFX["bullets"]["barrett"].convert_alpha()

GFX["bullets"]["rocket"] = load_image(EFFECTS_PATH + "rocket", (X // 32, Y // 8))
GFX["bullets"]["rocket"].convert_alpha()

# chargement des niveaux
for level in list(levels.keys()):
    GFX[level] = {}
    TEMP = LEVELS_PATH + level
    GFX[level]["bg"] = load_image(TEMP, levels[level]["scale"]).convert()

# chargement des textures des obstacles
TEMP = LEVELS_PATH + "platform"
GFX["platform"] = load_image(TEMP, (X // 1.5, Y // 1.5)).convert_alpha()

# Images pour le menu
GFX['punchingball'] = load_image(BG_PATH + 'image', (120, 120)).convert_alpha()
GFX['hit'] = load_image(BG_PATH + 'punched', (120, 120)).convert_alpha()
GFX['stats_box'] = load_image(
    "test_olivier/gfx/box/" + "stats_box", (X // 3, X // 8)).convert_alpha()
GFX["skill_box"] = load_image(
    "test_olivier/gfx/box/" + "stats_box", (X // 2, X // 9)).convert_alpha()

bro_tab = ["C'est quoi la blague ?",
           "C'est un peu bêbête",
           "You fuck my wife ?",
           "C'est un truc d'autiste ça",
           "Alors, j'enlève cette merde",
           "Au procès, je gagne !",
           "Je vais faire sonner le gros Ben",
           "Je fais donc péter le logarithme",
           "Je fais donc péter l'exponentielle", ]

GFX["kim"] = load_dir("data/gfx/players/kim/", (X // 12, Y // 12))
GFX["luffy"] = load_image("test_olivier/gfx/box/" +
                          "luffy", (X // 15, X // 15)).convert_alpha()
GFX["itachi"] = load_image("test_olivier/gfx/box/" +
                           "itachi", (X // 15, X // 15)).convert_alpha()
GFX["goku"] = load_image("test_olivier/gfx/box/" +
                         "goku", (X // 15, X // 15)).convert_alpha()
GFX["vegeta"] = load_image("test_olivier/gfx/box/" +
                           "vegeta", (X // 15, X // 15)).convert_alpha()
GFX["gear4"] = load_image("test_olivier/gfx/box/" +
                          "gear4", (X // 15, X // 15)).convert_alpha()
GFX["revive"] = load_image("test_olivier/gfx/box/" +
                           "revive", (X // 15, X // 15)).convert_alpha()

TEMP = EVENTS_PATH+"kim_ult/"
GFX["kim_dance"] = [load_image(TEMP + filename[0:-4], (X, Y)) for filename in listdir(TEMP)]