""" Modules qui gère les manettes. """
import pygame as pg
import pygame._sdl2
from pygame._sdl2.controller import Controller
from pygame.locals import *
from data.modules.settings import read_settings
from data.modules.keyboard import azerty_to_qwerty
pg._sdl2.controller.init()
pg.joystick.init()
pg.init()

def manage_joysticks():
    """renvoie les manettes utilisés"""
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


class SimpleController:
    """permet de simuler des pressions de touches avec la manette"""
    def __init__(self, number):
        self.buttons = {
            "B": "l_attack",
            "Y": "h_attack",
            "A": "jump",
            "X": "block"
        }
        self.keys = read_settings()["keys"][number]

    def get_pressed(self, controller):
        """renvoie un dico de boutons pressés"""
        pressed = {
            "B": bool(controller.get_button(1)),
            "A": bool(controller.get_button(0)),
            "X": bool(controller.get_button(2)),
            "Y": bool(controller.get_button(3)),
            "LB": bool(controller.get_button(4)),
            "RB": bool(controller.get_button(5)),
            "BACK": bool(controller.get_button(6)),
            "START": bool(controller.get_button(7)),
            "Lstick_pressed": bool(controller.get_button(8)),
            "Rstick_pressed": bool(controller.get_button(9)),
            "Lstick_x": round(controller.get_axis(0), 3),
            "Lstick_y": round(-controller.get_axis(1), 3),
            "Rstick_x": round(controller.get_axis(2), 3),
            "Rstick_y": round(-controller.get_axis(3), 3),
                }
        return pressed       

    def check_buttons(self, pressed):
        """fait les actions et agit en conséquence"""
        buttons = []
        for button in pressed.keys():
            key = self.get_key(button)
            button_type = type(pressed[button]).__name__
            if button_type == "bool":
                if pressed[button]:
                    buttons.append(key)
            else:
                if button == "Lstick_x":
                    if abs(pressed[button]) > 20000:
                        if pressed[button] < 0:
                            buttons.append("left")
                        else:
                            buttons.append("right")
        return buttons

    def get_key(self, button):
        """renvoie la clé correspondant au bouton appuyé"""
        try:
            return self.buttons[button]
        except KeyError:
            return None
        
    def clean_nones(self, old_list):
        """supprime tout les Nones d'une liste"""
        new_list = []
        for element in old_list:
            if not element is None:
                new_list.append(element)
        return new_list

    def update(self):
        """met presses les touches des boutons de la manette pressés"""
        contro = manage_controller([])
        plugged = not contro is None
        if plugged:
            controller = contro[0]
            pressed = self.get_pressed(controller)
            buttons = self.check_buttons(pressed)
            buttons = self.clean_nones(buttons)
        return buttons
