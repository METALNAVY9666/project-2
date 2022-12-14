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
