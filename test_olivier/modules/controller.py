import pygame as pg
from pygame._sdl2.controller import Controller
pg._sdl2.controller.init()


def manage_controller():
    joysticks = [pg.joystick.Joystick(i) for i in range(pg.joystick.get_count())]
    #Permet de savoir le nombre de manettes utilisés
    for joystick in joysticks:
        controller = Controller.from_joystick(joystick)
        return controller

