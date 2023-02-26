
'''Ce module permet de gérer le joueur, ses déplacements etc'''
import pygame as pg
from data.modules.texture_loader import sprites_images, sprite_tab
from data.modules.controllers import manage_controller
from data.modules.settings import read_settings
from data.modules.keyboard import azerty_to_qwerty


class Fighter(pg.sprite.Sprite):
    '''Cette classe permet de gérer les actions du joueur,
    ainsi que son apparence.'''

    def __init__(self, game, pkg, prop, number):
        super().__init__()
        self.game = game
        self.number = number
        # Dictionnaire des attributs du personnage
        print('Voici le perso:', number)
        self.init_dict(pkg, prop)
        self.init_perso()
        # Tableau d'actions
        self.actions_tab = ['attack', 'combo',
                            'final', 'impact', 'spe']
        # Axe droite-gauche
        self.motion = [0]
        if number == 1:
            self.rect.x = 200

    def init_dict(self, pkg, prop):
        """
        Dictionnaire
        """
        self.vals = {}
        self.vals["nbr_sprite"] = 0
        self.vals["strike"] = 10
        self.vals["max_height"] = 400
        self.vals["jumps"] = 1
        self.vals["current_height"] = 0
        self.vals["pause"] = True
        self.vals["idle_speed"] = 125
        self.vals["delta_sum"] = 0
        self.vals["health"] = 100
        self.vals["max_health"] = 100
        self.vals["attacked"] = False
        self.vals["fall"] = True
        self.vals["nbr_vanish"] = 4
        self.vals["nbr_combo_q"] = 0
        self.vals["nbr_combo_w"] = 0
        self.vals["surface_height"] = self.game.elms["pkg"]['surface'].get_height()
        self.vals["surface_width"] = self.game.elms["pkg"]['surface'].get_width()
        self.vals["pkg"] = pkg
        self.vals["prop"] = prop
        self.vals["tab"] = []
        self.vals["percent_ult"] = 130
        self.vals["sp_tab"] = []
        self.vals["jumping"] = True
        self.vals["dashing"] = [False, False]
        self.vals["name"] = self.game.name[self.number]
        self.settings = {}
        self.settings["dims"] = self.vals["pkg"]["dimensions"]
        self.settings["level"] = self.vals["prop"]["ground_level"]
        self.vals["ground"] = (self.settings['level'] *
                               self.settings['dims'][1]) // 100
        self.settings['size_max'] = self.settings['dims'][1] - \
            self.settings['dims'][1] // 12 - self.vals['ground']
        self.vals["keymap"] = read_settings()["keys"][self.number]

    def init_perso(self):
        self.tab = sprite_tab(
            self.game.name[self.number], self.game.elms["side"][self.number])
        # Affectation de l'image
        self.image = self.tab[self.vals['nbr_sprite']]
        # Récupération du rectangle de l'image
        self.rect = self.image.get_rect()
        # Coordonées en x et y
        self.rect.x = self.vals['surface_height'] // 9
        self.rect.y = self.vals['surface_width'] // 3
        # Images complémentaires
        self.images_dict = sprites_images(self.game.name[self.number])
    # Déplacement horizontal du joueur

    def is_gunner(self):
        """
        Vérifie quel joueur est un gunner ou un fighter
        """
        ennemy = self.game.player_1
        if self.number == 1:
            ennemy = self.game.player_0
        if ennemy.game.name[ennemy.number] == "kim":
            return ennemy.get_rect()
        return ennemy.rect

    def move(self):
        '''Cette fonction gère les déplacements à droite ou à gauche.'''
        # Vérifie s'il n'y a pas de collisions
        rect = self.is_gunner()
        test = not self.game.collision()
        self.settings['dims'] = self.vals["pkg"]["dimensions"]
        if test or (not test and self.rect.y < rect.y - 10):
            # Déplacement vers la gauche
            if self.game.elms["right"][self.number] and (
                    self.rect.x < self.vals['surface_width'] - 100):
                self.rect.x += 8
                # On change l'image du joueur
                if self.game.name[self.number] in ['goku', 'vegeta']:
                    self.change_animation('right')
                    self.vals['pause'] = False
                else:
                    self.game.elms["side"][self.number] = 'run'
            # Déplacement vers la droite
            elif not self.game.elms["right"][self.number] and self.rect.x > 5:
                self.rect.x -= 8
                if self.game.name[self.number] in ['goku', 'vegeta']:
                    self.change_animation('left')
                    # Le joueur fait une action, donc on passe le bouléen
                    # sur False
                    self.vals['pause'] = False
                else:
                    self.game.elms["side"][self.number] = 'run'
        if not test:
            self.move_collide(rect)

    def move_collide(self, rect):
        """
        Mouvement en cas de collision(s)
        """
        if (self.game.elms["right"][self.number] and
                rect.x < self.rect.x):
            self.rect.x += 6
            # On change l'image du joueur
            if self.game.name[self.number] in ['goku', 'vegeta']:
                self.change_animation('right')
                self.vals['pause'] = False
            else:
                self.game.elms["side"][self.number] = 'run'
        elif not self.game.elms["right"][self.number] and (
                rect.x > self.rect.x):
            self.rect.x -= 6
            if self.game.name[self.number] in ['goku', 'vegeta']:
                self.change_animation('left')
                self.vals['pause'] = False
            else:
                self.game.elms["side"][self.number] = 'run'

    def move_controller(self, valeur):
        "Cette fonction gère les déplacements de droite à gauche a la manette"
        # Vérifie s'il n'y a pas de collisions
        test = not self.game.collision()
        ennemy = self.game.player_1
        if self.number == 1:
            ennemy = self.game.player_0
        self.settings['dims'] = self.vals["pkg"]["dimensions"]
        if not self.vals["dashing"][self.number]:
            if test or (not test and self.rect.y < ennemy.rect.y - 10):
                if (not self.game.elms["right"][self.number] and
                        self.rect.x > 5):
                    self.motion[0] = valeur / 3000
                    self.rect.x += self.motion[0]
                    # On change l'image du joueur
                    if self.game.name[self.number] in ['goku', 'vegeta']:
                        self.change_animation('left')
                        self.vals['pause'] = False
                    else:
                        self.game.elms["side"][self.number] = 'run'

                elif self.game.elms["right"][self.number] and (
                        self.rect.x < self.vals['surface_width'] - 100):
                    # self.game.elms["right"][self.number] = True
                    self.motion[0] = valeur / 3000
                    self.rect.x += self.motion[0]
                    # On change l'image du joueur
                    if self.game.name[self.number] in ['goku', 'vegeta']:
                        self.change_animation('right')
                        self.vals['pause'] = False
                    else:
                        self.game.elms["side"][self.number] = 'run'

        if not test and not self.vals["dashing"][self.number]:
            self.move_collide(ennemy)

    # Saut du joueur
    def jump(self):
        '''Fonction saut'''
        if self.vals["jumping"]:
            # Vérfie si ale perso est inférieur à la hauteur de saut mx
            if self.vals['current_height'] <= self.vals['max_height']:
                # Vérifie si le perso n'a pas déjà sauté deux fois
                if self.vals['jumps'] < 2:
                    # Saute
                    self.rect.y -= 25
                    self.vals['current_height'] += 25
                # Si le joueur a atteint la hauteur maximale, il redescend
                if self.vals['current_height'] >= self.vals['max_height']:
                    self.vals['jumps'] = 3

    def jump_controller(self, jumpCount):
        # Fonction saut a la manette
        if jumpCount >= -8:
            self.rect.y -= (jumpCount * abs(jumpCount)) * 0.39
            self.vals['current_height'] += (jumpCount * abs(jumpCount)) * 0.39
            jumpCount -= 1
        else:
            jumpCount = 8

    def gravity(self):
        '''Fonction qui simule une gravité'''
        test = not self.game.collision()
        size_max = self.settings["size_max"]
        if not test and self.rect.y <= self.vals["ground"]:
            self.vals['fall'] = False
        # Le joueur tombe tant qu'il n'est pas au sol
        if self.vals['fall']:
            if self.rect.y <= size_max and test:
                self.rect.y += 10
                if self.vals['jumping']:
                    self.change_animation('jump')
                # Change l'animation si on est à droite ou à gauche
                    if self.game.elms["right"][self.number]:
                        self.change_animation('jump_right')
            # Sinon, on réinitialise son nombre de sauts à zéro
            elif self.rect.y >= size_max or not test:
                self.vals['jumps'] = 0
                # Réaffecte à zéro la hauteur actuelle
                self.vals['current_height'] = 0
                self.vals["jumping"] = True

    # Gestion de l'animation/affichage du joueur

    def change_animation(self, name):
        '''Fonction qui change l'image du personnage'''
        # On réaffecte le dictionnaire d'images
        self.images_dict = sprites_images(self.game.name[self.number])
        self.image = self.images_dict[name]
        # On redimensionne les images d'Itachi
        # ouais pour l'instant non :)
        """if self.game.name[self.number] in ['itachi']:
            self.image = pg.transform.scale(self.image, (120, 120))
            if name in ['shield', 'shield_right']:
                self.image = pg.transform.scale(self.image, (70, 120))"""

    def blit_sprite(self, screen, dlt, pause):
        '''Cette fonction sert à afficher le sprite du joueur en continu
        des coordonées demandes.'''
        # On affiche les actions que le joueur fait
        screen.blit(self.image, (self.rect))
        if not pause:
            # Changement d'image
            self.image = self.position()
            self.vals['delta_sum'] += dlt
            # si la somme des temps entre les frames est plus grande que 300ms
            if self.vals['delta_sum'] >= self.vals['idle_speed']:
                # changer le sprite
                self.vals['nbr_sprite'] += 1
                # remettre la somme des temps à 0
                self.vals['delta_sum'] = 0
            if self.vals['nbr_sprite'] >= 5:
                self.vals['nbr_sprite'] = 0
                self.game.elms["side"][self.number] = 'left'

    def get_rect(self):
        """renvoie le rect du fighter"""
        return self.rect

    def position(self):
        '''Fonction qui change le tableau d'image
        en fonction de la position du persos'''
        # Vérifie si le personnage est à droite ou à gauche
        self.tab = sprite_tab(
            self.game.name[self.number], self.game.elms["side"][self.number])
        # Réaffecte l'image en fonction de la position
        self.image = self.tab[self.vals['nbr_sprite']]
        # Inverse les images en cas d'attaque à droite
        if self.game.elms["right"][self.number]:
            self.image = pg.transform.flip(
                self.tab[self.vals['nbr_sprite']], True, False)
        return self.image

    # Gestion des attaques/combos

    def attack(self, event, choice):
        '''Cette fonction permet de gérer l'attaque d'un perso.'''
        ennemy = self.game.player_0
        if self.number == 0:
            ennemy = self.game.player_1
        self.single_tap(event, choice, ennemy)
        self.combo(ennemy)

    def attack_controller(self, choice, contro):
        '''
        Cette fonction permet de gérer l'attaque d'un perso à la manette.
        '''
        ennemy = self.game.player_0
        if self.number == 0:
            ennemy = self.game.player_1
        self.single_tap_controller(choice, contro, ennemy)
        self.combo(ennemy)

    def combo_tab(self, event):
        """
        Cette fonction récupère les touches actuellement
        préssées si il y a une collision.
        Tant qu'il y a moins de 10 éléments dans le tableau on en rajoute.
        """
        if self.game.collision():
            if len(self.vals['tab']) < 4:
                self.vals['tab'].append(event.key)
                print(self.vals['tab'])
            else:
                self.vals['tab'] = []
        else:
            self.vals["tab"] = []
        return self.vals['tab']

    def convert_key(self, key):
        """renvoie la classe pygame de la clé"""
        keymap = self.vals["keymap"]
        return pg.key.key_code(azerty_to_qwerty(keymap[key]))
    
    def single_tap(self, event, choice, ennemy):
        """
        Attaque normale de base selon les paramètres du joueur
        """
        keymap = self.vals["keymap"]
        l_attack = azerty_to_qwerty(keymap["l_attack"])
        h_attack = azerty_to_qwerty(keymap["h_attack"])
        l_attack = pg.key.key_code(l_attack)
        h_attack = pg.key.key_code(h_attack)

        dict_keys = {l_attack: "attack", h_attack: "impact"}
        # Le joueur fait une action
        if event.key in dict_keys:
            if self.game.elms["right"][self.number]:
                self.rect.x += 10
            else:
                self.rect.x -= 10
            self.game.strike_collision(ennemy)
            self.combo_tab(event)
            self.vals['nbr_sprite'] = 0
            self.game.elms["side"][self.number] = dict_keys[event.key]
            if event.key == l_attack or h_attack:
                self.attack_up(choice, ennemy)
                self.attack_down(choice, ennemy)

    # Docstrings a ajouter
    def single_tap_controller(self, choice, contro, ennemy):
        if contro.get_button(1):
            self.game.strike_collision(ennemy)
            self.vals['nbr_sprite'] = 0
            self.game.elms["side"][self.number] = 'attack'
            if self.game.collision():
                if len(self.vals['tab']) < 4:
                    self.vals['tab'].append(117)
                    print(self.vals['tab'])
                else:
                    self.vals['tab'] = []
            else:
                self.vals["tab"] = []
            return self.vals['tab']

        elif contro.get_button(2):
            self.game.strike_collision(ennemy)
            # self.combo_tab(choice)
            self.vals['nbr_sprite'] = 0
            self.game.elms["side"][self.number] = 'impact'
            if self.game.collision():
                if len(self.vals['tab']) < 4:
                    self.vals['tab'].append(121)
                    print(self.vals['tab'])
                else:
                    self.vals['tab'] = []
            else:
                self.vals["tab"] = []
            return self.vals['tab']

    def move_manager(self, event):
        """
        Gère les actions avec des inputs spécifiques
        """
        if len(self.vals['sp_tab']) < 9:
            self.vals['sp_tab'].append(event.key)
        else:
            temp = self.vals['sp_tab'][len(self.vals['tab'])-1]
            self.vals['sp_tab'] = []
            self.vals['sp_tab'].append(temp)
        # print(self.vals['sp_tab'])

    def dash_attack_up(self, choice, event):
        """
        Gère l'attaque rapide en l'air
        """
        jump = self.convert_key("jump")
        l_attack = self.convert_key("l_attack")
        if choice[jump] and event.key == l_attack:
            self.vals['jumping'] = False
            self.vals['nb_sprite'] = 0
            self.game.elms["side"][self.number] = 'attack'
            if self.game.elms["right"][self.number]:
                self.rect.x += 100
            else:
                self.rect.x -= 100

    def dash_attack_up_controller(self):
        """
        Gère l'attaque rapide en l'air à la manette
        """
        self.vals['jumping'] = False
        self.vals['nb_sprite'] = 0
        self.game.elms["side"][self.number] = 'attack'
        if self.game.elms["right"][self.number]:
            self.rect.x += 100
        else:
            self.rect.x -= 100

    def combo(self, ennemy):
        """
        Dégats du combo final
        """
        if self.vals['tab'] == [121, 121, 117, 117]:
            self.game.elms["side"][self.number] = 'spe'
            if self.game.name[ennemy.number] != "kim":
                self.game.elms["side"][ennemy.number] = "back"
                if self.game.elms["right"][self.number]:
                    ennemy.rect.x += 200
                else:
                    ennemy.rect.x -= 200
            self.vals['tab'] = []

    def attack_up(self, choice, ennemy):
        '''Attaque en l'air'''
        if choice[self.convert_key("jump")]:
            if self.game.collision():
                self.game.elms["side"][self.number] = 'up'
                if self.game.name[ennemy.number] == "kim":
                    print("kim va voler")
                else:
                    ennemy.rect.y = 250
        if self.game.collision():
            self.vals['fall'] = False
            if self.vals['nbr_combo_q'] > 1 and self.rect.y <= 400:
                self.game.elms["side"][self.number] = 'impact'
                self.vals['fall'] = False
                if self.game.name[ennemy.number] == "kim":
                    print("OH KIM PTN")
                else:
                    ennemy.rect.x -= 100

    def attack_down(self, choice, ennemy):
        """
        Attaque vers le bas
        """
        if choice[pg.K_DOWN] and (
                self.game.collision()):
            self.game.elms["side"][self.number] = 'down'
            if self.game.name[ennemy.number] == "kim":
                print("ALLO")
            else:
                while ennemy.rect.y <= self.settings['size_max']:
                    ennemy.rect.y += 1

    def attack_down_controller(self, ennemy):
        if self.game.collision():
            self.game.elms["side"][self.number] = 'down'
            while ennemy.rect.y <= self.settings['size_max']:
                ennemy.rect.y += 1

    def damages(self):
        '''Fonction qui gère les dommages'''
        if self.game.collision():
            if not self.vals['attacked']:
                self.vals['health'] -= 1

    # Gestion des mouvements spéciaux comme le bloquage, l'esquive etc...

    def block(self):
        '''Fonction qui empêche de se prendre des dégats durant une attaque'''
        self.vals['attacked'] = True
        self.change_animation('shield')
        if self.game.elms["right"][self.number]:
            self.change_animation('shield_right')

    def vanish(self, event):
        '''Fonction qui actionne une esquive,
        le personnage peut esquiver une attaque 4 fois'''
        # L'esquve se fait que si le joueur se prend des dégats
        if self.game.collision():
            # On vérifie le nombre de tentatives autorisées
            if self.vals['nbr_vanish'] > 0 and event.key == pg.K_e:
                # Relance l'animation à zéro
                self.vals['nbr_sprite'] = 0
                # Change l'animation
                self.game.elms["side"][self.number] = 'vanish'
                # on diminue le nombre de tentative
                self.vals['nbr_vanish'] -= 1
                # Effectue l'esquive en fonction de la position du perso
                if self.game.elms["right"][self.number] and self.rect.x > 5:
                    self.rect.x -= 100
                elif not self.game.elms["right"][self.number] and self.rect.x < 950:
                    self.rect.x += 100

    def charge(self):
        """Charge l'énergie"""
        if self.game.name[self.number] in ["goku", "revive"]:
            if self.vals["percent_ult"] < 130:
                self.vals["jumping"] = False
                self.vals["percent_ult"] += 0.1
                self.game.elms["side"][self.number] = "ki"
            else:
                self.vals["jumping"] = True

    def vanish_controller(self):
        '''Fonction qui actionne une esquive,
        le personnage peut esquiver une attaque 4 fois'''
        # L'esquve se fait que si le joueur se prend des dégats
        if self.game.collision():
            # On vérifie le nombre de tentatives autorisées
            if self.vals['nbr_vanish'] > 0:
                # Relance l'animation à zéro
                self.vals['nbr_sprite'] = 0
                # Change l'animation
                self.game.elms["side"][self.number] = 'vanish'
                # on diminue le nombre de tentative
                self.vals['nbr_vanish'] -= 1
                # Effectue l'esquive en fonction de la position du perso
                if self.game.elms["right"][self.number] and self.rect.x > 5:
                    self.rect.x -= 100
                elif not self.game.elms["right"][self.number] and self.rect.x < 950:
                    self.rect.x += 100

    def is_dashing(self, choice, event):
        """
        Autorise le dash avant
        """
        if self.number == 0:
            if choice[pg.K_q] or choice[pg.K_d]:
                if event.key == pg.K_s:
                    self.vals["dashing"][self.number] = True
        elif self.number == 1:
            if choice[self.game.get_code("left")] or (
                    choice[self.game.get_code("right")]):
                if choice[self.game.get_code("down")]:
                    self.vals["dashing"][self.number] = True

    def dash(self):
        """
        EFfectue le dash
        """
        if self.vals["dashing"][self.number]:
            if not self.game.collision():
                if self.game.elms["right"][self.number]:
                    self.game.elms["side"][self.number] = "dash"
                    if self.rect.x < self.vals["surface_width"] - 200:
                        self.rect.x += 30
                    else:
                        self.vals["dashing"][self.number] = False
                        # self.rect.x = self.vals["surface_width"] - 100
                else:
                    if self.rect.x > self.vals["surface_width"] // 100:
                        self.rect.x -= 30
                    else:
                        self.vals["dashing"][self.number] = False
            else:
                self.vals["dashing"][self.number] = False
    # Autres

    def update_pv(self):
        '''renvoi les pvs'''
        return [[self.game.name[self.number], self.vals['health']]]
