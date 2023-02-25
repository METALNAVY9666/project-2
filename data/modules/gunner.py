"""contient la classe d'un joueur"""
import pygame as pg
from copy import copy
from random import randint
from data.modules.texture_loader import GFX
from data.modules.audio import SFX
from data.modules.keyboard import NUMPAD
from data.modules.settings import read_settings


class Gunner(pg.sprite.Sprite):
    """créee un objet joueur"""

    def __init__(self, game, pkg, prop, id):
        """initialise les propriétés du joueur"""
        super().__init__()
        self.pkg = pkg
        self.prop = prop

        self.init_physics()
        self.init_player(id)
        self.init_graphics()
        self.init_weapons()
        self.game = game
        self.number = id

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
        self.player["name"] = "Kim"
        self.player["hp"] = 20
        self.player["old_hp"] = 20
        self.player["size"] = [width // 8, height // 6]
        self.player["weapon"] = "fist"
        self.player["block"] = False
        self.player["id"] = id
        self.player["keys"] = read_settings()["keys"][id]
        self.player["cooldown"] = {
            "barrett": 0,
            "kick": 0,
            "rocket": 0
        }
        self.player["bullets"] = []
        self.player["combos"] = []
        self.player["ult"] = {}
        self.player["ult"]["power"] = 100
        self.player["ult"]["status"] = False
        self.player["ult"]["time"] = 0
        self.player["ult"]["load"] = 7 * self.pkg["FPS"]
        self.player["ult"]["delta"] = self.pkg["FPS"] // 14
        self.player["ult"]["music"] = True

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
        self.gfx["animations"] = {}
        self.gfx["animations"]["kick"] = 166
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
        match animation:
            case "wait":
                sprite = GFX["kim"]["wait"]
            case "shoot":
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
            case "run":
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
        return sprite

    def blit_sprite(self, sprite, pos):
        """affiche le sprite sur la surface de jeu"""
        side = self.physics["side"]
        if side == -1:
            sprite = self.flip(sprite)
        return self.pkg["surface"].blit(sprite, pos)

    def damage_self(self, dmg):
        '''permet de s'infliger des dégtas'''
        dmg = copy(dmg)
        if self.player["block"]:
            dmg // 2
        self.player["hp"] -= dmg

    # ------ Attaques ------

    def barrett_shoot(self, dlt):
        """tire une balle de calibre 50"""
        return self.play_animation("shoot", dlt)

    def update_bullets(self, pause, other):
        """met à jour la position de la balle tirée"""
        bullets = []
        rects = []
        ground_lvl = self.physics["ground"]
        for bullet in self.player["bullets"]:
            if not bullet.specs["out"]:
                bullets.append(bullet)

        for bullet in bullets:
            rects.append(bullet.update(pause, other, ground_lvl))

        self.player["bullets"] = bullets

        return rects

    def update_cooldowns(self, dlt):
        """met à jour les cooldowns"""
        cooldown = self.player["cooldown"]
        keys = list(cooldown.keys())
        for key in keys:
            if cooldown[key] > 0 and key != "rocket":
                cooldown[key] -= dlt
        for animation in list(self.gfx["animations"]):
            if self.gfx["animations"][animation] > 0:
                # self.gfx["animations"][animation] -= dlt
                pass

    # ------ Physiques ------

    def move(self, dlt):
        """déplace le gunner
        l'ideal serait un truc du style:
        if not self.game.collision():
            side = self.physics["side"]
        speed = self.physics["speed"]
        pos = self.physics["pos"]
        print(self.game.collision())
        print(self.rect)
        pos[0] += int(speed * side)
        self.rect.x = pos[0]
        return self.play_animation("run", dlt)"""

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

    def check_combos(self, pause, busy):
        """vérifie les combos présents"""
        if not pause:
            combos = self.player["combos"]
            ultimate = "block" in combos and "h_attack" in combos
            if ultimate and self.player["ult"]["power"] >= 100:
                self.player["ult"]["time"] = self.pkg["FPS"] * 5
                self.player["ult"]["status"] = True

    def ult_animation(self, music, busy):
        fps = self.pkg["FPS"]
        frame = 7 * fps - self.player["ult"]["load"]
        rect = None
        if self.player["ult"]["music"]:
            SFX["kim"]["default_dance"].play()
            music.pause(True)
            busy = True
            self.player["ult"]["music"] = False

        if len(GFX["kim_dance"]) > frame:
            rect = self.blit_sprite(GFX["kim_dance"][frame], (0, 0))
        else:
            self.player["ult"]["load"] = 0
            music.pause(False)
            busy = False
        self.player["ult"]["delta"] -= 1
        if self.player["ult"]["delta"] == 0:
            self.player["ult"]["load"] -= 1
            self.player["ult"]["delta"] = fps // 14
        return rect

    def update_ulti(self, pause, music, busy):
        """met à jour l'ultime de kim"""
        if not pause:
            if self.player["ult"]["status"]:
                if self.player["ult"]["load"] == 0:
                    self.player["ult"]["time"] -= 1
                    if self.player["ult"]["time"] == 0:
                        self.player["ult"]["power"] = 0
                        self.player["ult"]["status"] = False
                    else:
                        if self.player["cooldown"]["rocket"] == 0:
                            side = self.gfx["side"]
                            dims = self.pkg["dimensions"]
                            pos = [randint(0, dims[0]), 0]
                            rocket = Bullet(self.pkg, "rocket",
                                            side, pos, 50, 0.2)
                            self.player["bullets"].append(rocket)
                            self.player["cooldown"]["rocket"] = self.pkg["FPS"] // 4
                        else:
                            self.player["cooldown"]["rocket"] -= 1
                else:
                    return self.ult_animation(music, busy)
            else:
                if self.player["old_hp"] != self.player["hp"]:
                    delta = self.player["old_hp"] - self.player["hp"]
                    self.player["ult"]["power"] += randint(delta, 20 * delta)

    def update_health(self):
        """met à jour la vie"""
        self.player["old_hp"] = copy(self.player["hp"])

    def update_keys(self, dlt, pause, busy, other):
        """met à jour les mouvements du joueur"""
        choice = self.pkg["key"].get_pressed()
        keys = self.player["keys"]

        self.player["block"] = False

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

        if pause is busy is False:
            sprite = GFX["kim"]["wait"]
            pack = []
            for couple in pressed:
                if couple[1]:
                    pack.append(couple[0])
                    self.player["combos"].append(pressed)
                    if couple[0] == "jump":
                        self.jump()
                    elif couple[0] == "block":
                        sprite = self.block()
                    elif couple[0] == "right":
                        self.physics["side"] = 1
                        sprite = self.move(dlt)
                    elif couple[0] == "left":
                        self.physics["side"] = -1
                        sprite = self.move(dlt)
                    elif couple[0] == "l_attack":
                        sprite = self.kick(other)
                    elif couple[0] == "h_attack":
                        sprite = self.barrett_shoot(dlt)
            self.gfx["sprite"] = sprite
            self.player["combos"] = pack

        return self.blit_sprite(self.gfx["sprite"], self.physics["pos"])

    def block(self):
        """indique que le gunner bloque"""
        self.player["block"] = True
        if self.gfx["side"] == -1:
            return GFX["kim"]["block"]
        return self.flip(GFX["kim"]["block"])

    def damage_player(self, player, dmg):
        """inflige des dommages à un joueur"""
        colliderect = self.pkg["Rect"].colliderect
        if colliderect(self.get_rect(), player):
            player_type = type(player).__name__
            if player_type == "Fighter":
                if player.vals["attacked"]:
                    dmg /= 4
                player.vals["health"] -= dmg
            elif player_type == "Gunner":
                if player.player["block"]:
                    dmg /= 4
                player.player["hp"] -= dmg

    def kick(self, rect):
        """coup de pied yahoo"""
        if self.player["cooldown"]["kick"] <= 0:
            self.player["cooldown"]["kick"] = 333
            SFX["kim"]["kick"].play()
            self.damage_player(rect, 10)
        if self.player["cooldown"]["kick"] >= self.gfx["animations"]["kick"]:
            return GFX["kim"]["kick_1"]
        return GFX["kim"]["kick_0"]

    def get_rect(self):
        """renvoie le rect du joueur"""
        rect = self.gfx["sprite"].get_rect()
        rect.x, rect.y = self.physics["pos"]
        return rect

    def update(self, dlt, pause, busy, other, music):
        """met à jour le sprite du joueur"""
        self.update_health()
        self.check_ground()
        self.gravity()
        self.update_jump()
        self.update_cooldowns(dlt)
        self.check_combos(pause, busy)
        rects = []
        rects.append(self.update_keys(dlt, pause, busy, other))
        rects += self.update_bullets(pause, other)
        rects.append(self.update_ulti(pause, music, busy))
        return rects


class Bullet:
    """classe pour la balle du joueur"""

    def __init__(self, pkg, texture, side, pos, damage=25, speed=1):
        dims = pkg["dimensions"]
        self.pkg = pkg
        self.pos = pos * 1
        self.specs = {
            "type": texture,
            "origin": pos * 1,
            "out": False,
            "life": 0,
            "speed": self.pkg["dimensions"][0] // 43 * speed,
            "damage": damage,
            "explosion": self.pkg["FPS"] // 2,
            "exploded": False,
            "show": True
        }
        self.textures = [GFX["bullets"][texture], GFX["nuzzle"]]
        if side == -1 and texture != "rocket":
            for ind in range(len(self.textures)):
                self.textures[ind] = self.flip(self.textures[ind])
        else:
            self.specs["origin"][0] += dims[0] // 18
        self.side = side
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
        if not None in (bullet_rect, player):
            colliderect = self.pkg["Rect"].colliderect
            damage = self.specs["damage"]
            rect = None
            if colliderect(bullet_rect, player.get_rect()):
                name = type(player).__name__
                self.speed = 0
                self.specs["show"] = False
                if name == "Fighter":
                    if self.specs["type"] == "rocket":
                        if not self.specs["exploded"]:
                            player.vals["health"] -= damage
                    else:
                        player.vals["health"] -= damage
                else:
                    if self.specs["type"] == "rocket":
                        if not self.specs["exploded"]:
                            player.player["hp"] -= damage
                    else:
                        player.player["hp"] -= damage
                if self.specs["type"] == "rocket":
                    self.explosion()
            return rect

    def nuzzle(self):
        """affiche une explosion de tir"""
        if self.specs["type"] != "rocket":
            self.specs["life"] += 1
            dims = self.pkg["dimensions"]
            pos = self.specs["origin"] * 1
            pos[1] += dims[1]//36
            if self.specs["life"] <= 15:
                return self.blit(self.textures[1], pos)

    def explosion(self):
        """kaboom"""
        if self.specs["explosion"] > 0:
            pos = self.pos * 1
            rect = self.blit(GFX["explosion"], pos)
            if not self.specs["exploded"]:
                SFX["explosion"].play()
                self.specs["exploded"] = True
            self.specs["explosion"] -= 1
            return rect
        self.specs["out"] = True

    def update(self, pause, other, ground_lvl):
        """met à jour la balle"""
        dims = self.pkg["dimensions"]
        ymax = dims[1]
        if self.specs["type"] == "rocket":
            ymax = dims[1] - ground_lvl
        in_horizontal = self.pos[0] > 0 and self.pos[0] <= dims[0]
        in_vertical = self.pos[1] > 0 and self.pos[1] <= ymax
        if in_horizontal and in_vertical:
            if not pause:
                if self.specs["type"] == "rocket":
                    self.pos[1] += self.specs["speed"]
                else:
                    self.pos[0] += self.specs["speed"] * self.side
                bullet_rect = None
                if self.specs["show"]:
                    bullet_rect = self.blit(self.textures[0], self.pos)
                return bullet_rect, self.nuzzle(), self.check_player(bullet_rect, other)
        else:
            if self.specs["type"] == "rocket":
                return self.explosion()
            self.specs["out"] = True
