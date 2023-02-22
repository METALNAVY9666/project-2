
'''Ce module permet de gérer le joueur, ses déplacements etc'''
import pygame as pg
from data.modules.texture_loader import sprites_images, sprite_tab
from data.modules.controllers import (manage_controller,
                                      removed_and_added_controller)


class Fighter(pg.sprite.Sprite):
    '''Cette classe permet de gérer les actions du joueur,
    ainsi que son apparence.'''

    def __init__(self, game, pkg, prop, number):
        super().__init__()
        self.game = game
        self.number = number
        # Dictionnaire des attributs du personnage
        print('Voici le perso:', number)
        self.vals = {
            'nbr_sprite': 0, 'strike': 10,
            'max_height': 400, 'jumps': 1,
            'current_height': 0, 'pause': True,
            'idle_speed': 125, 'delta_sum': 0,
            'nbr_combo': 0, 'nbr_vanish': 4,
            'max_health': 100, 'health': 100,
            'attacked': False, 'fall': True,
            'nbr_combo_q': 0, 'nbr_combo_w': 0,
            'surface_height': self.game.elms['pkg']['surface'].get_height(),
            'surface_width': self.game.elms['pkg']['surface'].get_width(),
            "pkg": pkg, "prop": prop,
            'tab': [], 'percent_ult': 130,
            'sp_tab': [], 'jumping': True,
            "dashing": [False, False, False]
        }
        self.settings = {
            'dims': self.vals["pkg"]["dimensions"],
            'level': self.vals["prop"]["ground_level"],

        }
        self.vals["ground"] = (self.settings['level'] *
                               self.settings['dims'][1]) // 100
        self.settings['size_max'] = self.settings['dims'][1] - \
            self.settings['dims'][1] // 12 - self.vals['ground']
        # Récupération du tableau des images du persos
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
        # Tableau d'actions
        self.actions_tab = ['attack', 'combo',
                            'final', 'impact', 'spe']
        # Axe droite-gauche
        self.motion = [0]
        if number == 2:
            self.rect.x = 200

    # Déplacement horizontal du joueur

    def move(self):
        '''Cette fonction gère les déplacements à droite ou à gauche.'''
        # Vérifie s'il n'y a pas de collisions
        test = not self.game.collision()
        self.settings['dims'] = self.vals["pkg"]["dimensions"]
        if test or (not test and self.rect.y < self.game.object.rect.y):
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
            self.move_collide()

    def move_collide(self):
        """
        Mouvement en cas de collision(s)
        """
        if (self.game.elms["right"][self.number] and
                self.game.object.rect.x < self.rect.x):
            self.rect.x += 6
            # On change l'image du joueur
            if self.game.name[self.number] in ['goku', 'vegeta']:
                self.change_animation('right')
                self.vals['pause'] = False
            else:
                self.game.elms["side"][self.number] = 'run'
        elif not self.game.elms["right"][self.number] and (
                self.game.object.rect.x > self.rect.x):
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
        self.settings['dims'] = self.vals["pkg"]["dimensions"]
        if not self.vals["dashing"][self.number]:
            if test or (not test and self.rect.y < self.game.object.rect.y):
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
            self.move_collide()

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
        size_max = self.settings['dims'][1] - \
            self.settings['dims'][1] // 12 - self.vals['ground']
        if not test and self.rect.y < self.vals['ground']:
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
        self.single_tap(event, choice)
        self.combo()

    def attack_controller(self, choice):
        '''
        Cette fonction permet de gérer l'attaque d'un perso à la manette.
        '''
        self.single_tap_controller(choice)
        self.combo()

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

    def single_tap(self, event, choice):
        """
        Attaque normale de base avec y et u
        """
        dict_keys = {pg.K_y: 'attack', pg.K_u: 'impact'}
        # Le joueur fait une action
        if event.key in dict_keys:
            if self.game.elms["right"][self.number]:
                self.rect.x += 5
            else:
                self.rect.x -= 5
            self.game.strike_collision()
            self.combo_tab(event)
            self.vals['nbr_sprite'] = 0
            self.game.elms["side"][self.number] = dict_keys[event.key]
            if event.key == pg.K_y:
                self.attack_up(choice)
                self.attack_down(choice)

    # Docstrings a ajouter
    def single_tap_controller(self, choice):
        controller = manage_controller()
        if controller.get_button(1):
            self.game.strike_collision()
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

        elif controller.get_button(2):
            self.game.strike_collision()
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
        if choice[self.game.get_code('z')] and event.key == pg.K_y:
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

    def combo(self):
        """
        Dégats du combo final
        """
        if self.vals['tab'] == [121, 121, 117, 117]:
            self.game.elms["side"][self.number] = 'spe'
            self.game.object.rect.x -= 200
            self.vals['tab'] = []

    def attack_up(self, choice):
        '''Attaque en l'air'''
        if choice[pg.K_UP]:
            if self.game.collision():
                self.game.elms["side"][self.number] = 'up'
                self.game.object.rect.y = 250
        if self.game.collision():
            self.vals['fall'] = False
            if self.vals['nbr_combo_q'] > 1 and self.rect.y <= 400:
                self.game.elms["side"][self.number] = 'impact'
                self.vals['fall'] = False
                self.game.object.rect.x -= 100

    def attack_down(self, choice):
        """
        Attaque vers le bas
        """
        if choice[pg.K_DOWN] and (
                self.game.collision()):
            self.game.elms["side"][self.number] = 'down'
            while self.game.object.rect.y <= self.settings['size_max']:
                self.game.object.rect.y += 1

    def attack_down_controller(self):
        if self.game.collision():
            self.game.elms["side"][self.number] = 'down'
            while self.game.object.rect.y <= self.settings['size_max']:
                self.game.object.rect.y += 1

    def damages(self):
        '''Fonction qui gère les dommages'''
        if self.game.collision():
            if not self.vals['attacked']:
                self.vals['health'] -= 1
            # pass

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
        if choice[pg.K_q] or choice[pg.K_d]:
            if event.key == pg.K_s:
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
        return [[self.game.name[self.number], self.vals['health']],
                ['punchingball', self.game.object.stats['health']]]
