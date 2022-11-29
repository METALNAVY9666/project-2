'''Ce module gère la fenêtre afin de tester les personnages etc...'''
import pygame as pg
from modules.menu import Menu
from modules.game import Jeu


def image_maker(name, height, width):
    '''Cette fonction permet de renvoyer une image redimensionnée.
    Pour ce faire, l'utilisateur affecte le chemin d'une
    image à la place de la variable name. Ensuite il y entre les valeurs
    pour la nouvelle hauteur et largeur de la future image.
    Image.load charge l'image, et transform.scale redimensionne l'image.
    Pour finir, on renvoie l'image finale.'''
    image = pg.image.load(name)
    image = pg.transform.scale(image, (height, width))
    return image


def screen_win():
    '''Fonction qui renvoie l'écran.'''
    screen = pg.display.set_mode((1080, 720))
    pg.display.set_caption('Moissan Figg')
    return screen


def quit_game(EVENTS, test):
    '''Fonction qui vérifie si l'on appuie sur le bouton pour quitter.'''
    for event in EVENTS:
        if event.type == pg.QUIT:
            print('Vous êtes sortis du jeu.')
            test = False
    return test


def main_window():
    '''Fonction qui lance la fenêtre principale.'''
    pg.init()
    clock = pg.time.Clock()
    # Elements de la fenêtre
    screen = screen_win()
    # Redimensionne le fond d'écran
    background = image_maker('test_olivier/gfx/images/map_tuto.jpg', 1080, 720)
    square = Menu()
    jeu = Jeu(name='hello')
    # Boucle du jeu
    test = True
    # dlt est le delta time: càd le temps entre 2 frames
    dlt = clock.tick(jeu.fps)
    while test:
        EVENTS = pg.event.get()
        screen.blit(background, (0, 0))
        if square.name == 'hello':
            # On change par le nom du perso choisi
            jeu.name = square.menu_update(screen, EVENTS)
        elif jeu.name != 'hello':
            jeu.update(screen, EVENTS, dlt)
        pg.display.flip()
        # On vérifie si le test est sur True ou False constemment
        test = quit_game(EVENTS, test)
        dlt = clock.tick(jeu.fps)

    pg.quit()


main_window()
