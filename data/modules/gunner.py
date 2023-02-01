"""contient la classe d'un joueur"""
from data.modules.texture_loader import GFX
from data.modules.sound_loader import SFX
from data.modules.keyboard import NUMPAD
from data.modules.settings import read_settings


class Gunner():
    """créee un objet joueur"""

    def __init__(self, pkg, prop, id):
        """initialise les propriétés du joueur"""
        self.pkg = pkg
        self.prop = prop

        self.init_physics()
        self.init_player(id)
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
        self.physics["speed"] = self.pkg["dimensions"][0]/1920 * 16
        self.physics["side"] = 1
        level = self.prop["ground_level"]
        dims = self.pkg["dimensions"]
        self.physics["ground"] = (level * dims[1]) // 100

    def init_player(self, id):
        """initialise les propriétés du joueur"""
        width, height = self.pkg["dimensions"]
        self.player = {}
        self.player["hp"] = 20
        self.player["size"] = [width//8, height//6]
        self.player["weapon"] = "fist"
        self.player["keys"] = read_settings()["keys"][id]
        self.player["cooldown"] = {
            "barrett": 0,
            "kick": 0,
            }

    def init_graphics(self):
        """le nom est équivoque je pense"""
        self.gfx = {}
        self.gfx["frame"] = 0
        # cool est le temps à attendre entre 2 sprites
        self.gfx["cool"] = 0 
        self.gfx["side"] = False
        self.gfx["sprite"] = GFX["kim"]["wait"]
        self.gfx["old_sprite"] = ""
        self.gfx["delta_sum"] = 0
        self.gfx["current"] = "wait"
        # current est [nom_sprite, temps_animation]

    def init_weapons(self):
        """initialise l'arsenal"""
        self.player["weapons"] = {}
        self.player["reload"] = {}
        for weapon in ["makarov", "barrett", "kick"]:
            self.player["reload"][weapon] = 0

    def get_code(self, key):
        "renvoie la valeur de la touche"
        return self.pkg["key"].key_code(key)

    def flip(self, sprite):
        """renvoie le sprite retourné"""
        image = self.pkg["transform"].flip(sprite, True, False)
        return image.convert_alpha()

    def init_animation(self, animation):
        """initialise l'animation"""
        if self.gfx["current"] != animation:
            self.gfx["current"] = animation
            self.gfx["delta_sum"] = 0

    def play_animation(self, animation, dlt):
        """joue l'animation demandée"""
        self.gfx["delta_sum"] += dlt
        cooldown = self.player["cooldown"]
        # ------ attends ------
        if animation == "wait":
            sprite = GFX["kim"]["wait"]
        # ------ tire ------
        if animation == "shoot":
            if cooldown["barrett"] < 1:
                cooldown["barrett"] = 3000
                SFX[animation].play()
                sprite = GFX["kim"]["sneak"]
            elif cooldown["barrett"] >= 2500:
                sprite = GFX["kim"]["sneak"]
        # ------ cours ------
        if animation == "run":
            if self.gfx["delta_sum"] >= 100:
                self.gfx["delta_sum"] = 0
                self.gfx["frame"] += 1
            
            frame = self.gfx["frame"]
            key = "run_" + str(frame)
            try:
                sprite = GFX["kim"][key]
            except KeyError:
                self.gfx["frame"] = 0
                sprite = GFX["kim"]["run_0"]
        # ------ renvoie le sprite ------
        return sprite

    def barrett_shoot(self, dlt):
        """tire une balle de calibre 50"""
        return self.play_animation("shoot", dlt)

    def update_cooldowns(self, dlt):
        """met à jour les cooldowns"""
        cooldown = self.player["cooldown"]
        if cooldown["barrett"] > 0:
            cooldown["barrett"] -= dlt 

    def move(self, dlt):
        """déplace le gunner"""
        side = self.physics["side"]
        speed = self.physics["speed"]
        pos = self.physics["pos"]
        pos[0] += int(speed * side)
        return self.play_animation("run", dlt)

    def blit_sprite(self, sprite, pos):
        """affiche le sprite sur la surface de jeu"""
        side = self.physics["side"]
        if side == -1:
            sprite = self.flip(sprite)
        return self.pkg["surface"].blit(sprite, pos)

    def gravity(self):
        """applique la gravité au joueur"""
        pos = self.physics["pos"]
        dims = self.pkg["dimensions"]
        pos[1] += self.physics["gravity"]
        ground = self.physics["ground"]
        if pos[1] > dims[1] - dims[1]//12 - ground:
            pos[1] = dims[1] - dims[1]//12 - ground

    def update_keys(self, dlt, pause, busy):
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
                # car pygame ne prend pas en compte le numpad
                pressed.append([key, choice[NUMPAD[keys[key]]]])

        if not pause:
            sprite = GFX["kim"]["wait"]
            for couple in pressed:
                if couple[1]:
                    if couple[0] == "jump":
                        print("jump")
                    elif couple[0] == "block":
                        print("block")
                    elif couple[0] == "right":
                        self.physics["side"] = 1
                        sprite = self.move(dlt)
                    elif couple[0] == "left":
                        self.physics["side"] = -1
                        sprite = self.move(dlt)
                    elif couple[0] == "l_attack":
                        print("patate")
                    elif couple[0] == "h_attack":
                        sprite = self.barrett_shoot(dlt)
            self.gfx["sprite"] = sprite

        return self.blit_sprite(self.gfx["sprite"], self.physics["pos"])

    def update(self, dlt, pause, busy):
        """met à jour le sprite du joueur"""
        self.gravity()
        self.update_cooldowns(dlt)
        return self.update_keys(dlt, pause, busy)

    """def jump_start(self, force):
        if self.is_grounded:
            self.jump_frame = -int(force*10)
            self.y -= 2
            self.is_grounded = False
            self.isFalling = False

    def jump_check(self):
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
"""