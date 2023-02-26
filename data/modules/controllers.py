""" Modules qui gère les manettes. """
import keyboard
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


class SimController:
    """permet de simuler des pressions de touches avec la manette"""
    def __init__(self, number):
        self.keys = read_settings()["keys"][number]
        self.buttons = []

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
    
    def press(self, key, release=False):
        """simule la pression d'une touche, la lache si release = True, (convertit AZERTY en QWE)"""
        if not key is None:
            new_key = azerty_to_qwerty(key)
            print(new_key)
            if release:
                keyboard.release(new_key)
            else:
                keyboard.press(new_key)

    def check_buttons(self, pressed):
        """fait les actions et agit en conséquence"""
        press = self.press
        self.buttons = []
        for button in pressed.keys():
            key = self.get_key(button)
            button_type = type(pressed[button]).__name__
            if button_type == "bool":
                if pressed[button]:
                    press(key)
                    self.buttons.append(button)
                else:
                    press(key, True)
            else:
                if button == "Lstick_x":
                    if abs(pressed[button]) > 20000:
                        if pressed[button] < 0:
                            press("right", True)
                            press("left")
                        else:
                            press("left", True)
                            press("right")
                    else:
                        press("right", True)
                        press("left", True)

    def get_key(self, button):
        """renvoie la clé correspondant au bouton appuyé (ne convertit pas AZERTY en QWERTY)"""
        keys = self.keys
        match button:
            case "B":
                return keys["l_attack"]
            case "Y":
                return keys["h_attack"]
            case "Lstick_x":
                pass

    def update(self):
        """met presses les touches des boutons de la manette pressés"""
        contro = manage_controller([])
        plugged = not contro is None
        if plugged:
            controller = contro[0]
            pressed = self.get_pressed(controller)
            self.check_buttons(pressed)
