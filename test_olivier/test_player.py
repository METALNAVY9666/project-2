import pygame as pg
from modules.menu import Menu
from modules.game import Jeu


def button_pressed():
    joy = []
    for i in range(pg.joystick.get_count()):
        joy.append(pg.joystick.Joystick(i))
    return joy


def choice_lines(lines, event, square):
    '''Cette fonction permet de renvoyer le numéro de la ligne
    sur laquelle le joueur est.'''
    if event.key == pg.K_RIGHT and lines < 3:
        lines += 1
        square.rect.x += 110
        print(lines)
    elif event.key == pg.K_LEFT and lines >= 0:
        if lines < 0:
            lines = 0
        else:
            print(lines)
            square.rect.x -= 110
            lines -= 1
    return lines


def choice_column(column, event, square):
    '''Cette fonction permet de renvoyer le numéro de la colonne
    sur laquelle le joueur est.'''
    if event.key == pg.K_DOWN and column < 2:
        square.rect.y += 100
        column += 1
        print(column)
    elif event.key == pg.K_UP and column > 0:
        square.rect.y -= 100
        column -= 1
        print(column)
    return column


def choice_perso(lines, column, event, menu):
    if event.key == pg.K_RETURN:
        menu = False
        tab = perso()
        print('Vous êtes sortis du menu.')
        print('Vous avez choisis le', tab[column][lines])
    return menu


def button_dict():
    dico = {
        'x': 0,
        'circle': 1,
        'square': 2,
        'triangle': 3,
        "share": 4,
        'PS': 5,
        'options': 6,
        'left_stick_click': 7,
        'right_stick_click': 8,
        'L1': 9,
        'R1': 10,
        'up_arrow': 11,
        'down_arrow': 12,
        'left_arrow': 13,
        'right_arrow': 14,
        'touchepad': 15
    }
    return dico


def perso():
    tab = [['Perso 1', 'Perso 2', 'Perso 3', 'Perso 4'],
           ['Perso 5', 'Perso 5(bis)', 'Perso 6', 'Perso 7'],
           ['Perso 8', 'Perso 9', 'Perso 10', 'Perso 11']
           ]
    return tab


def main_window():
    pg.init()
    clock = pg.time.Clock()
    '''
    joysticks = button_pressed()
    button_keys = button_dict()
    analog_key = {}
    for joystick in joysticks:
        joystick.init()'''
    # Elements de la fenêtre
    screen = pg.display.set_mode((1080, 720))
    background = pg.image.load('gfx/images/map_tuto.jpg')
    background = pg.transform.scale(background, (1080, 720))
    pg.display.set_caption('Moissan FIghters Z')
    lines = 0
    column = 0
    menu = False
    square = Menu()
    jeu = Jeu()
    # Boucle du jeu
    test = True
    while test:
        choice = pg.key.get_pressed()
        EVENTS = pg.event.get()
        screen.blit(background, (0, 0))
        if menu:
            screen.blit(square.image, (square.rect))
            for event in EVENTS:
                if event.type == pg.KEYDOWN:
                    lines = choice_lines(lines, event, square)
                    column = choice_column(column, event, square)
                    menu = choice_perso(lines, column, event, menu)
        elif jeu.is_playing:
            jeu.update(screen, EVENTS)
        pg.display.flip()
        for event in EVENTS:
            if event.type == pg.QUIT or choice[pg.K_ESCAPE]:
                print('Vous êtes sortis du jeu.')
                test = False
            elif choice[pg.K_a]:
                print('Le jeu va commencer.')
            elif choice[pg.K_z] and not menu:
                print('Vous rentrez dans le menu.')
                menu = True
            elif choice[pg.K_e] and not jeu.is_playing:
                jeu.is_playing = True
                print('vous allez rentrer dans le jeu.')
        clock.tick(jeu.fps)

    pg.quit()


main_window()
