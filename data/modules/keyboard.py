"""cotient les fonctions permettant de gérer les touches du claiver"""

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
        if key not in qwerty:
            return key
        ind = qwerty.index(key)
        return azerty[ind]
    if key not in azerty:
        return key
    ind = azerty.index(key)
    return qwerty[ind]


def get_numpad():
    """renvoie les touches associées au numpad"""
    numpad = {}
    code = 1073741922
    for nombre in range(10):
        cle = f"kp_{nombre}"
        numpad[cle] = code
        code += 1
    return numpad
