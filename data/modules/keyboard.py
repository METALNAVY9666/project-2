"""cotient les fonctions permettant de gérer les touches du claiver"""
import pygame


class KeyChecker:
    """contient les fonction permettant de tester les touches"""

    def __init__(self, pkg, pause_menu):
        self.pkg = pkg
        self.pause_menu = pause_menu
        self.keys = {}
        self.keys["new"] = self.pkg["pygame"].key.get_pressed()

    def check_key(self, key_name):
        """vérifie si la touche est touchée et relâchée"""
        pressed = {}
        pressed["old"] = self.keys["old"][key_name]
        pressed["new"] = self.keys["new"][key_name]
        if not pressed["old"] and pressed["new"]:
            return True
        return False

    def check_keys(self, keys):
        """vérifie quelles touches sont appuyées"""
        self.keys["old"] = self.keys["new"]
        self.keys["new"] = self.pkg["pygame"].key.get_pressed()
        for key in keys:
            if self.check_key(key):
                if self.pause_menu.bool:
                    self.pause_menu.bool = False
                else:
                    self.pause_menu.bool = True
                self.pause_menu.switch()


def azerty_to_qwerty(key, reverse=False):
    """convertit une lettre du clavier azerty en qwerty"""
    if len(key) != 1:
        return key
    azerty = 'azqwAZQW&é"\'(-è_çà)^$Mù,?;:!§1234567890'
    qwerty = 'qwazQWAZ1234567890-[]:\'mM,./?!@#$%^&*()'
    if reverse:
        if not key in qwerty:
            return key
        ind = qwerty.index(key)
        return azerty[ind]
    if not key in azerty:
            return key
    ind = azerty.index(key)
    return qwerty[ind]

NUMPAD = {
    "kp_0": pygame.K_KP0,
    "kp_1": pygame.K_KP1,
    "kp_2": pygame.K_KP2,
    "kp_3": pygame.K_KP3,
    "kp_4": pygame.K_KP4,
    "kp_5": pygame.K_KP5,
    "kp_6": pygame.K_KP6,
    "kp_7": pygame.K_KP7,
    "kp_8": pygame.K_KP8,
    "kp_9": pygame.K_KP9
}
