""" Modules qui gère les manettes. """
import pygame as pg
import pygame._sdl2
from pygame._sdl2.controller import Controller
from pygame.locals import *
pg._sdl2.controller.init()
pg.joystick.init()
pg.init()


def manage_joysticks():
    return [pg.joystick.Joystick(i) for i in range(pg.joystick.get_count())]

def manage_controller(contro):
    """
    Permet de savoir combien et quelles manettes sont utilisées.
    """
    joysticks = [pg.joystick.Joystick(i)
                 for i in range(pg.joystick.get_count())]
    # Permet de savoir le nombre de manettes utilisés
    if joysticks != []:
        for joystick in joysticks:
            contro.append(Controller.from_joystick(joystick))
        return contro
    return None
print(manage_controller([]))

def removed_and_added_controller():
    """
    Permet de pouvoir ajouter/enlever une manette en cours de jeu.
    """
    for event in pg.event.get():
        if event.type in [pg.JOYDEVICEADDED, pg.JOYDEVICEREMOVED]:
            controller = manage_controller()
            if event.type == pg.JOYDEVICEADDED:
                print("Une manette à été ajouté.")
            else:
                print("Une manette à été déconnectée.")
    return controller
