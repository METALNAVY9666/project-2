"""contient la classe d'un joueur"""
from data.modules.texture_loader import GFX
from data.modules.audio import SFX
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
        self.physics["gravity"] = 9.81 * 2
        self.physics["grounded"] = True
        self.physics["jump_height"] = self.pkg["dimensions"][1] // 3
        self.physics["pos"] = [0, 0]
        self.physics["jump_state"] = False
        self.physics["falling"] = False
        self.physics["speed"] = self.pkg["dimensions"][0] / 1920 * 16
        self.physics["side"] = 1
        level = self.prop["ground_level"]
        dims = self.pkg["dimensions"]
        self.physics["ground"] = (level * dims[1]) // 100

    def init_player(self, id):
        """initialise les propriétés du joueur"""
        width, height = self.pkg["dimensions"]
        self.player = {}
        self.player["hp"] = 20
        self.player["size"] = [width // 8, height // 6]
        self.player["weapon"] = "fist"
        self.player["id"] = id
        self.player["keys"] = read_settings()["keys"][id]
        self.player["cooldown"] = {
            "barrett": 0,
            "kick": 0,
                    }
        self.player["bullets"] = []

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
                SFX["kim"]["shoot"].play()
                side = self.physics["side"]
                pos = self.physics["pos"]
                bullet = Bullet(self.pkg, "barrett", side, pos)
                self.player["bullets"].append(bullet)
                sprite = GFX["kim"]["sneak"]
                self.physics["pos"][0] -= 32 * side
            elif cooldown["barrett"] >= 2500:
                sprite = GFX["kim"]["sneak"]
            else:
                sprite = self.gfx["sprite"]
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

    def blit_sprite(self, sprite, pos):
        """affiche le sprite sur la surface de jeu"""
        side = self.physics["side"]
        if side == -1:
            sprite = self.flip(sprite)
        return self.pkg["surface"].blit(sprite, pos)

    # ------ Attaques ------

    def barrett_shoot(self, dlt):
        """tire une balle de calibre 50"""
        return self.play_animation("shoot", dlt)

    def update_bullets(self, pause, other):
        """met à jour la position de la balle tirée"""
        bullets = []
        rects = []

        for bullet in self.player["bullets"]:
            if not bullet.out:
                bullets.append(bullet)

        for bullet in bullets:
            rects.append(bullet.update(pause, other))

        self.player["bullets"] = bullets

        return rects

    def update_cooldowns(self, dlt):
        """met à jour les cooldowns"""
        cooldown = self.player["cooldown"]
        if cooldown["barrett"] > 0:
            cooldown["barrett"] -= dlt

    # ------ Physiques ------

    def move(self, dlt):
        """déplace le gunner"""
        side = self.physics["side"]
        speed = self.physics["speed"]
        pos = self.physics["pos"]
        pos[0] += int(speed * side)
        return self.play_animation("run", dlt)
    
    def gravity(self):
        """applique la gravité au joueur"""
        pos = self.physics["pos"]
        dims = self.pkg["dimensions"]
        pos[1] += self.physics["gravity"]
        ground = self.physics["ground"]
        if pos[1] > (dims[1] - dims[1] // 12 - ground):
            pos[1] = dims[1] - dims[1] // 12 - ground

    def check_ground(self):
        """vérifie si le joueur est au sol"""
        pos = self.physics["pos"]
        dims = self.pkg["dimensions"]
        ground = self.physics["ground"]
        self.physics["grounded"] = pos[1] >= dims[1] - dims[1] // 12 - ground

    def jump(self):
        """fait sauter le joueur"""
        grounded = self.physics["grounded"]
        pos = self.physics["pos"]
        ground = self.physics["ground"]
        dims = self.pkg["dimensions"]
        gravity = self.physics["gravity"]
        if grounded:
            self.physics["jump_state"] = True
            pos[1] = dims[1] - dims[1] // 12 - ground - (10 + gravity)

    def update_jump(self):
        """met à jour le saut du joueur"""
        grounded = self.physics["grounded"]
        pos = self.physics["pos"]
        gravity = self.physics["gravity"]
        jump_height = self.physics["jump_height"]
        jump_state = self.physics["jump_state"]
        if not grounded:
            delta = pos[1] - jump_height
            if jump_state:
                pos[1] -= (gravity + delta**(1/2))
                if pos[1] <= jump_height:
                    self.physics["jump_state"] = False
                    self.physics["falling"] = True
            else:
                if self.physics["falling"]:
                    pos[1] -= ((jump_height-delta)**(1/2))*0.9
        else:
            self.physics["falling"] = False
            
    # ------ Touches ------

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
                try:
                    pressed.append([key, choice[NUMPAD[keys[key]]]])
                except KeyError:
                    print(f"Problème de touche ({keys[key]})")
        
        if not pause:
            sprite = GFX["kim"]["wait"]
            for couple in pressed:
                if couple[1]:
                    if couple[0] == "jump":
                        self.jump()
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

    def get_rect(self):
        """renvoie le rect du joueur"""
        rect = self.gfx["sprite"].get_rect()
        rect.x, rect.y = self.physics["pos"]
        return rect

    def update(self, dlt, pause, busy, other):
        """met à jour le sprite du joueur"""
        self.check_ground()
        self.gravity()
        self.update_jump()
        self.update_cooldowns(dlt)
        rects = []
        rects.append(self.update_keys(dlt, pause, busy))
        rects = rects + self.update_bullets(pause, other)
        return rects

class Bullet:
    """classe pour la balle du joueur"""
    def __init__(self, pkg, texture, side, pos):
        dims = pkg["dimensions"]
        self.pkg = pkg
        self.pos = pos * 1
        self.textures = [GFX["bullets"][texture], GFX["nuzzle"]]
        self.origin = pos * 1
        if side == -1:
            for ind in range(len(self.textures)):
                self.textures[ind] = self.flip(self.textures[ind])
        else:
            self.origin[0] += dims[0] // 18
        
        self.side = side
        self.out = False
        self.life = 0
        self.speed = self.pkg["dimensions"][0] // 43
        self.pos[1] += self.pkg["dimensions"][1] // 36
    
    def flip(self, sprite):
        """renvoie le sprite retourné"""
        image = self.pkg["transform"].flip(sprite, True, False)
        return image.convert_alpha()

    def blit(self, texture, pos):
        """affiche sur la surface la texture"""
        blit_texture = self.pkg["surface"].blit
        rect = blit_texture(texture, pos)
        return rect

    def check_player(self, bullet_rect, player):
        """vérifie si le rect entre en collision avec la balle"""
        colliderect = self.pkg["Rect"].colliderect
        if colliderect(bullet_rect, player.get_rect()):
            name = type(player).__name__
            if name == "Fighter":
                player.vals["health"] -= 25
            else:
                player.player["hp"] -= 25
            self.out = True

    def nuzzle(self):
        """affiche une explosion de tir"""
        self.life += 1
        dims = self.pkg["dimensions"]
        pos = self.origin * 1
        pos[1] += dims[1]//36
        if self.life <= 15:
            return self.blit(self.textures[1], pos)

    def update(self, pause, other):
        """met à jour la balle"""
        if self.pos[0] > -720 and self.pos[0] < 7680:
            if not pause:
                dims = self.pkg["dimensions"]
                self.pos[0] += self.speed * self.side
                bullet_rect = self.blit(self.textures[0], self.pos)
                self.check_player(bullet_rect, other)
                return bullet_rect, self.nuzzle()
        else:
            self.out = True
        