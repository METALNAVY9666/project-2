"""contient la classe d'un joueur"""
from data.modules.texture_loader import GFX
from data.modules.keyboard import NUMPAD
from data.modules.settings import read_settings


class Gunner():
    """créee un objet joueur"""

    def __init__(self, pkg, prop):
        """initialise les propriétés du joueur"""
        self.pkg = pkg
        self.prop = prop

        self.init_physics()
        self.init_player()
        self.init_graphics()
        self.init_weapons()

    def init_physics(self):
        """initialise les propriétés physiques du gunner"""
        self.physics = {}
        self.physics["gravity"] = 9.81*2
        self.physics["grounded"] = True
        self.physics["falling"] = False
        self.physics["jump_height"] = 0
        self.physics["jump_frame"] = round(-100*self.pkg["FPS"])//100
        self.physics["pos"] = [0, 0]

    def init_player(self):
        """initialise les propriétés du joueur"""
        width, height = self.pkg["dimensions"]
        self.player = {}
        self.player["hp"] = 20
        self.player["size"] = [width//8, height//6]
        self.player["weapon"] = "fist"
        self.player["keys"] = read_settings()["keys"][1]

    def init_graphics(self):
        """le nom est équivoque je pense"""
        self.gfx = {}
        self.gfx["frame"] = 0
        self.gfx["side"] = False
        self.gfx["old_sprite"] = ""

    def init_weapons(self):
        """initialise l'arsenal"""
        self.player["weapons"] = {}
        self.player["reload"] = {}
        for weapon in ["makarov", "barrett", "kick"]:
            self.player["reload"][weapon] = 0

    def update(self):
        """met à jour le sprite du joueur"""
        self.update_keys()

    def update_keys(self):
        """met à jour les mouvements du joueur"""
        choice = self.pkg["key"].get_pressed()
        keys = self.player["keys"]

        pressed = []

        for key in list(keys.keys()):
            try:
                # renvoie un couple ("jump", True) si le joueur appuie
                # sur la touche assignée au saut dans settings.json
                pressed.append([key, choice[self.get_code(keys[key])]])
            except ValueError:
                # si le joueur appuie sur une touche du pavé numérique
                # alors renvoyer le code depuis un dictionnnaire
                # pygame ne prend pas en compte le numpad
                pressed.append([key, choice[NUMPAD[keys[key]]]])

        for couple in pressed:
            if couple[1]:
                if couple[0] == "jump":
                    print("jump")
                elif couple[0] == "block":
                    print("block")
                elif couple[0] == "left":
                    print("left")
                elif couple[0] == "right":
                    print("right")
                elif couple[0] == "l_attack":
                    print("patate")
                elif couple[0] == "h_attack":
                    print("grosse patate")

    def get_code(self, key):
        "renvoie la valeur de la touche"
        return self.pkg["key"].key_code(key)

    def handle_input(self):
        """gère les movuements du personnage"""

    def jump_start(self, force):
        """initialise la fonction de saut"""
        if self.is_grounded:
            self.jump_frame = -int(force*10)
            self.y -= 2
            self.is_grounded = False
            self.isFalling = False

    def jump_check(self):
        """vérifie l'état du saut du joueur"""
        if self.y >= ground_level:
            self.is_grounded = True
        else:
            self.is_grounded = False
        if self.is_grounded == False:
            self.x += int(kim.speed/1.5)
            self.y += self.gravity
            if self.jump_frame < 0:
                self.y -= int(abs(self.jump_frame)*0.75)
            self.jump_frame += 1
