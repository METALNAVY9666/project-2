""" Modules qui gère les manettes. """
import pygame as pg
from pygame._sdl2.controller import Controller
from pygame.locals import *
pg._sdl2.controller.init()
pg.init()


def manage_joysticks():
    pg.joystick.init() #initialise le module joystick
    joysticks = [pg.joystick.Joystick(i) for i in range(pg.joystick.get_count())]
    #Permet de savoir le nombre de manettes utilisés
    dict_controller = {}

def manage_controller():
    """
    Permet de savoir combien et quelles manettes sont utilisées.
    """
    joysticks = [pg.joystick.Joystick(i) 
    for i in range(pg.joystick.get_count())]
    #Permet de savoir le nombre de manettes utilisés
    for joystick in joysticks:
        controller = Controller.from_joystick(joystick)
        return controller


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