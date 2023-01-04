'''Ce module gère la fenêtre afin de tester les personnages etc...'''
import pygame as pg
from modules.menu import Menu
from modules.game import Jeu
from modules.texture_loader import images

pg.joystick.init() #initialise le module joystick
joysticks = [pg.joystick.Joystick(i) for i in range(pg.joystick.get_count())]
#Permet de savoir le nombre de manettes utilisés
for joystick in joysticks:
    print(joystick.get_name()) #Permet de connaitre la manette utilisée.



def fps_moy(tab):
    '''Cette fonction permet de calculer la moyenne des fps'''
    # Renvoi la somme des valeurs divisée par la longueur du tableau
    return int(sum([element for element in tab]) / len(tab))


def screen_menu():
    '''Fonction qui renvoie l'écran.'''
    pg.display.set_caption('Moissan Fighter Z')
    screen = pg.display.set_mode((1080, 720))
    return screen


def quit_game(EVENTS, test):
    '''Fonction qui vérifie si l'on appuie sur le bouton pour quitter.'''
    for event in EVENTS:
        if event.type == pg.QUIT:
            print('\nVous êtes sortis du jeu.')
            test = False
    return test


def main_window():
    '''Fonction qui lance la fenêtre principale.'''
    pg.init()
    clock = pg.time.Clock()
    list_fps = []
    # Elements de la fenêtre
    screen = screen_menu()
    # Redimensionne le fond d'écran
    background = images["background"]
    square = Menu()
    jeu = Jeu(name='hello')
    # Création d'une liste afin de la mettre à jour
    liste_update = square.liste_rect
    # Boucle du jeu
    test = True
    # dlt est le delta time: càd le temps entre 2 frames
    dlt = clock.tick(jeu.fps)
    while test:
        # Ajoute les fps
        list_fps.append(int(clock.get_fps()))
        EVENTS = pg.event.get()
        # Ajout du fond dans la liste de chose à mettre à update
        liste_update.append(screen.blit(background, (0, 0)))
        if square.name == 'hello':
            # On change par le nom du perso choisi
            jeu.name = square.menu_update(screen, EVENTS)
        elif jeu.name != 'hello':
            # Mise à jour du jeu
            liste_update.append(jeu.update(screen, dlt))
            liste_update.append(jeu.update_objects(screen))
        pg.display.update(liste_update)
        liste_update = []
        pg.display.set_caption(f'FPS: {int(clock.get_fps())}')
        # On vérifie si le test est sur True ou False constemment
        test = quit_game(EVENTS, test)
        dlt = clock.tick(jeu.fps)
    # Affiche la moyenne des fps
    pg.quit()
    print("\nMoyenne des fps:", fps_moy(list_fps))


main_window()
