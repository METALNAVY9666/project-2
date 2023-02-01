'''Ce module permet de gérer le joueur, ses déplacements etc'''
import pygame as pg
from data.modules.texture_loader import sprites_images, sprite_tab


class Fighter(pg.sprite.Sprite):
    '''Cette classe permet de gérer les actions du joueur, ainsi que son apparence.'''

    def __init__(self, game, pkg, prop):
        super().__init__()
        self.game = game
        # Dictionnaire des attributs du personnage
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
            "pkg": pkg,
            "prop": prop
        }
        dims = self.vals["pkg"]["dimensions"]
        level = self.vals["prop"]["ground_level"]
        self.vals["ground"] = (level * dims[1]) // 100
        # Récupération du tableau des images du persos
        self.tab = sprite_tab(self.game.name, self.game.elms['side'])
        # Affectation de l'image
        self.image = self.tab[self.vals['nbr_sprite']]
        # Récupération du rectangle de l'image
        self.rect = self.image.get_rect()
        # Coordonées en x et y
        self.rect.x = self.vals['surface_height'] // 9
        self.rect.y = self.vals['surface_width'] // 3
        # Images complémentaires
        self.images_dict = sprites_images(self.game.name)
        # Tableau d'actions
        self.combo_tab = ['attack', 'combo',
                          'final', 'impact', 'spe']
        # Axe droite-gauche
        self.motion = [0]

    def move(self):
        '''Cette fonction gère les déplacements à droite ou à gauche.'''
        # Vérifie s'il n'y a pas de collisions
        test = not self.game.collision(self, self.game.all_objects)
        if test or (not test and self.rect.y <= self.vals['ground']):
            # Déplacement vers la gauche
            if self.game.elms['right'] and self.rect.x < self.vals['surface_width']-100:
                self.rect.x += 10
                # On change l'image du joueur
                if self.game.name in ['goku', 'vegeta']:
                    self.change_animation('right')
                    self.vals['pause'] = False
                else:
                    self.game.elms['side'] = 'run'
            # Déplacement vers la droite
            elif not self.game.elms['right'] and self.rect.x > 5:
                self.rect.x -= 10
                # Vérifie si le perso vole ou pas (si c'est vegeta ou goku)
                if self.game.name in ['goku', 'vegeta']:
                    # Si oui, il n'y a pas d'animation quand il se déplace
                    self.change_animation('left')
                    # Le joueur fait une action, donc on passe le bouléen sur False
                    self.vals['pause'] = False
                else:
                    self.game.elms['side'] = 'run'

    def move_controller(self, actions):
        "Cette fonction gère les déplacements de droite à gauche a la manette"
        # Vérifie s'il n'y a pas de collisions
        test = not self.game.collision(self, self.game.all_objects)
        if test:
            if actions.type == pg.JOYAXISMOTION and actions.axis == 0:
                if actions.value < -0.15 and self.rect.x > 0:
                    self.motion[actions.axis] = actions.value * 5
                    self.rect.x += self.motion[actions.axis]
                    self.vals['pause'] = False
                    # On change l'image du joueur
                    self.change_animation('left')

                elif actions.value > 0.15 and self.rect.x < 950:
                    self.motion[actions.axis] = actions.value * 5
                    self.rect.x += self.motion[actions.axis]
                    self.vals['pause'] = False
                    self.change_animation('right')

    def attack(self, event, choice):
        '''Cette fonction permet de gérer l'attaque d'un perso.'''
        collide = self.game.collision(self, self.game.all_objects)
        # Le joueur fait une action
        if event.key == pg.K_y:
            self.combo('attack', 'nbr_combo_q')
            self.attack_up(choice)
            self.attack_down(choice)
        elif event.key == pg.K_u:
            self.combo('impact', 'nbr_combo_w')
        if self.vals['nbr_combo_w'] == 2 and self.vals['nbr_combo_q'] == 2:
            # pg.time.wait(1000)
            print('AAAAAAAAH')
            self.game.elms['side'] = 'spe'
            self.game.object.rect.x -= 200
            self.vals['nbr_combo_w'] = 0
            self.vals['nb_combo_q'] = 0
        if not collide:
            self.vals['nbr_combo'] = 0
            self.vals['nbr_combo_w'] = 0
            self.vals['nbr_combo_q'] = 0
        # Augemente le nombre de combo
        # A voir ~~~~~

    def jump(self):
        '''Fonction saut'''
        # Vérfie si ale perso est inférieur à la hauteur de saut mx
        if self.vals['current_height'] <= self.vals['max_height']:
            # Vérifie si le perso n'a pas déjà sauté deux fois
            if self.vals['jumps'] < 2:
                # Saute
                self.rect.y -= 30
                self.vals['current_height'] += 30
            # Si le joueur a atteint la hauteur maximale, il redescend
            if self.vals['current_height'] >= self.vals['max_height']:
                self.vals['jumps'] = 3

    def jump_controller(self, actions):
        # Fonction saut a la manette
        if self.vals['current_height'] <= self.vals['max_height']:
            if self.vals['jumps'] < 2 and actions.type == pg.JOYBUTTONUP:
                if actions.button == 0:
                    # Vérifie si le perso n'a pas déjà sauté deux fois
                    if self.vals['jumps'] < 2:
                        # Saute
                        self.rect.y -= 25
                        self.vals['current_height'] += 25
                    # Si le joueur a atteint la hauteur maximale, il redescend
                    if self.vals['current_height'] >= self.vals['max_height']:
                        self.vals['jumps'] = 3

    def gravity(self):
        '''Fonction qui simule une gravité'''
        test = not self.game.collision(self, self.game.all_objects)
        # Le joueur tombe tant qu'il n'est pas au sol
        ground = self.vals["ground"]
        dims = self.vals["pkg"]["dimensions"]
        if self.vals['fall']:
            if self.rect.y <= dims[1] - dims[1]//12 - ground and test:
                self.rect.y += 10
                if not self.game.collision(self, self.game.all_objects):
                    self.change_animation('jump')
                # Change l'animation si on est à droite ou à gauche
                if self.game.elms['right']:
                    self.change_animation('jump_right')
            # Sinon, on réinitialise son nombre de sauts à zéro
            elif self.rect.y >= dims[1] - dims[1]//12 - ground or test:
                self.vals['jumps'] = 0
                # Réaffecte à zéro la hauteur actuelle
                self.vals['current_height'] = 0

    def gravity2(self):
        if self.rect.y < self.vals['surface_height']-100:
            self.rect.y += 5

    def change_animation(self, name):
        '''Fonction qui change l'image du personnage'''
        # On réaffecte le dictionnaire d'images
        self.images_dict = sprites_images(self.game.name)
        self.image = self.images_dict[name]
        # On redimensionne les images d'Itachi
        # ouais pour l'instant non :)
        """if self.game.name in ['itachi']:
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
                # Si le joueur ne fait pas d'attaque, on remet l'animation de base
                self.game.elms['side'] = 'left'

    def position(self):
        '''Fonction qui change le tableau d'image en fonction de la position du persos'''
        # Vérifie si le personnage est à droite ou à gauche
        self.tab = sprite_tab(self.game.name, self.game.elms['side'])
        # Réaffecte l'image en fonction de la position
        self.image = self.tab[self.vals['nbr_sprite']]
        # Inverse les images en cas d'attaque à droite
        if self.game.elms['right']:
            self.image = pg.transform.flip(
                self.tab[self.vals['nbr_sprite']], True, False)
        # Change l'image si le personnage est itachi
        """if self.game.name in ['itachi']:
            if self.game.elms['side'] in ['left', 'right', 'run', 'vanish']:
                return pg.transform.scale(self.image, (70, 120))
            return pg.transform.scale(self.image, (120, 120))"""
        return self.image

    def vanish(self, event):
        '''Fonction qui actionne une esquive, le personnage peut esquiver une attaque 4 fois'''
        # L'esquve se fait que si le joueur se prend des dégats
        if self.game.collision(self, self.game.all_objects):
            # On vérifie le ombre de tentatives autorisées
            if self.vals['nbr_vanish'] > 0 and event.key == pg.K_a:
                # Relance l'animation à zéro
                self.vals['nbr_sprite'] = 0
                # Change l'animation
                self.game.elms['side'] = 'vanish'
                # Si le joueuer appuie sur la touche, on diminue le nombre de tentative
                self.vals['nbr_vanish'] -= 1
                # Effectue l'esquive en fonction de la position du perso (droite/gauche)
                if self.game.elms['right'] and self.rect.x > 5:
                    self.rect.x -= 100
                elif not self.game.elms['right'] and self.rect.x < 950:
                    self.rect.x += 100

    def attack_up(self, choice):
        '''Attaque en l'air'''
        if choice[pg.K_UP] and self.game.collision(self, self.game.all_objects):
            self.game.elms['side'] = 'up'
            self.game.object.rect.y = 250
        if self.game.collision(self, self.game.all_objects):
            self.vals['fall'] = False
            if self.vals['nbr_combo_q'] > 1 and self.rect.y <= 400:
                self.game.elms['side'] = 'impact'
                self.vals['fall'] = False
                self.game.object.rect.x -= 100

    def damages(self):
        '''Fonction qui gère les dommages'''
        if self.game.collision(self, self.game.all_objects):
            """if not self.vals['attacked']:
                self.vals['health'] -= 1"""
            pass

    def block(self):
        '''Fonction qui empêche de se prendre des dégats durant une attaque'''
        self.vals['attacked'] = True
        self.change_animation('shield')
        if self.game.elms['right']:
            self.change_animation('shield_right')

    def combo(self, atk_name, key_name):
        '''Fonction attaque qui prend en paramètre le nom de la touche preéssée,
        et qui fait les animations ainsi que le comptage des combos'''
        collide = self.game.collision(self, self.game.all_objects)
        self.vals['nbr_sprite'] = 0
        self.game.elms['side'] = atk_name
        if collide:
            # attaque en l'air
            # self.attack_up(choice)
            self.vals[key_name] += 1
            print(self.vals[key_name])
        # Actionne la mécanique de dégats quand il y a une collision
        self.game.strike_collision()

    def attack_down(self, choice):
        if choice[pg.K_DOWN] and self.game.collision(self, self.game.all_objects):
            self.game.elms['side'] = 'down'
            while self.game.object.rect.y <= 500:
                self.game.object.rect.y += 1

    def update_pv(self):
        return [[self.game.name, self.vals['health']],
                ['punchingball', self.game.object.stats['health']]]
