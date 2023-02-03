'''Ce module permet de gérer le joueur, ses déplacements etc'''
import pygame as pg
from modules.texture_loader import sprites_images, sprite_tab
from modules.controller import manage_controller


class Player(pg.sprite.Sprite):
    '''Cette classe permet de gérer les actions du joueur, ainsi que son apparence.'''

    def __init__(self, game):
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
            'nbr_combo_q': 0, 'nbr_combo_w': 0}
        # Récupération du tableau des images du persos
        self.tab = sprite_tab(self.game.name, self.game.dict_game['side'])
        # Affectation de l'image
        self.image = self.tab[self.vals['nbr_sprite']]
        # Récupération du rectangle de l'image
        self.rect = self.image.get_rect()
        # Coordonées en x et y
        self.rect.x, self.rect.y = 900, 400
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
        if test or (not test and self.rect.y <= 500):
            # Déplacement vers la gauche
            if self.game.dict_game['right'] and self.rect.x < 950:
                self.rect.x += 10
                # On change l'image du joueur
                self.change_animation('right')
            # Déplacement vers la droite
            elif not self.game.dict_game['right'] and self.rect.x > 5:
                self.rect.x -= 10
                self.change_animation('left')
        # Le joueur fait une action, donc on passe le bouléen sur False
        self.vals['pause'] = False

    def move_controller(self, valeur):
        "Cette fonction gère les déplacements de droite à gauche a la manette"
        # Vérifie s'il n'y a pas de collisions
        test = not self.game.collision(self, self.game.all_objects)
        if test:
                if valeur / 1500 < -0.15 and self.rect.x > 0:
                    self.motion[0] = valeur / 2500
                    self.rect.x += self.motion[0]
                    # On change l'image du joueur
                    self.change_animation('left')
                    self.vals['pause'] = False

                elif valeur / 1500 > 0.15 and self.rect.x < 950:
                    self.motion[0] = valeur / 2500
                    self.rect.x += self.motion[0]
                    self.vals['pause'] = False
                    self.change_animation('right')

    def attack(self, event, choice):
        '''Cette fonction permet de gérer l'attaque d'un perso.'''
        collide = self.game.collision(self, self.game.all_objects)
        # Le joueur fait une action
        if event.key == pg.K_q:
            self.combo('attack', 'nbr_combo_q')
            self.attack_up(choice)
            self.attack_down(choice)
        elif event.key == pg.K_w:
            self.combo('impact', 'nbr_combo_w')
        if self.vals['nbr_combo_w'] == 2 and self.vals['nbr_combo_q'] == 2:
            # pg.time.wait(1000)
            print('AAAAAAAAH')
            self.game.dict_game['side'] = 'spe'
            self.game.object.rect.x -= 200
            self.vals['nbr_combo_w'] = 0
            self.vals['nb_combo_q'] = 0
        if not collide:
            self.vals['nbr_combo'] = 0
            self.vals['nbr_combo_w'] = 0
            self.vals['nbr_combo_q'] = 0
        # Augemente le nombre de combo
        # A voir ~~~~~

    def attack_controller(self, choice):
            '''Cette fonction permet de gérer l'attaque d'un perso.'''
            collide = self.game.collision(self, self.game.all_objects)
            controller = manage_controller()
            # Le joueur fait une action
            if controller.get_button(2):
                self.combo('attack', 'nbr_combo_q')
                self.attack_up(choice)
                self.attack_down(choice)
            elif controller.get_button(1):
                self.combo('impact', 'nbr_combo_w')
            if self.vals['nbr_combo_w'] == 2 and self.vals['nbr_combo_q'] == 2:
                # pg.time.wait(1000)
                print('AAAAAAAAH')
                self.game.dict_game['side'] = 'spe'
                self.game.object.rect.x -= 200
                self.vals['nbr_combo_w'] = 0
                self.vals['nb_combo_q'] = 0
            print(self.vals['nbr_combo'], self.vals['nbr_combo_w'], self.vals['nbr_combo_q'])
            if not collide:
                self.vals['nbr_combo'] = 0
                self.vals['nbr_combo_w'] = 0
                self.vals['nbr_combo_q'] = 0

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

    def jump_controller(self, jumpCount):
        # Fonction saut a la manette
        if jumpCount >= -8:
            self.rect.y -= (jumpCount * abs(jumpCount)) * 0.5
            self.vals['current_height'] +=(jumpCount * abs(jumpCount)) * 0.5
            jumpCount -= 1
        else: 
            jumpCount = 8
            

    def gravity(self):
        '''Fonction qui simule une gravité'''
        # Le joueur tombe tant qu'il n'est pas au sol
        if self.vals['fall']:
            if self.rect.y <= 500 and not self.game.collision(self, self.game.all_objects):
                self.rect.y += 10
                if not self.game.collision(self, self.game.all_objects):
                    self.change_animation('jump')
                # Change l'animation si on est à droite ou à gauche
                if self.game.dict_game['right']:
                    self.change_animation('jump_right')
            # Sinon, on réinitialise son nombre de sauts à zéro
            elif self.rect.y >= 500 or self.game.collision(self, self.game.all_objects):
                self.vals['jumps'] = 0
                # Réaffecte à zéro la hauteur actuelle
                self.vals['current_height'] = 0

    def change_animation(self, name):
        '''Fonction qui change l'image du personnage'''
        # On réaffecte le dictionnaire d'images
        self.images_dict = sprites_images(self.game.name)
        self.image = self.images_dict[name]

    def blit_sprite(self, screen, dlt):
        '''Cette fonction sert à afficher le sprite du joueur en continu
        des coordonées demandes.'''
        # On affiche les actions que le joueur fait
        screen.blit(self.image, (self.rect))
        if self.vals['pause']:
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
                self.game.dict_game['side'] = 'left'

    def position(self):
        '''Fonction qui change le tableau d'image en fonction de la position du persos'''
        # Vérifie si le personnage est à droite ou à gauche
        self.tab = sprite_tab(self.game.name, self.game.dict_game['side'])
        # Réaffecte l'image en fonction de la position
        self.image = self.tab[self.vals['nbr_sprite']]
        # Inverse les images en cas d'attaque à droite
        if self.game.dict_game['right']:
            self.image = pg.transform.flip(
                self.tab[self.vals['nbr_sprite']], True, False)
        return self.image

    def vanish(self, event):
        '''Fonction qui actionne une esquive, le personnage peut esquiver une attaque 4 fois'''
        # L'esquve se fait que si le joueur se prend des dégats
        if self.game.collision(self, self.game.all_objects):
            # On vérifie le ombre de tentatives autorisées
            if self.vals['nbr_vanish'] > 0 and event.key == pg.K_d:
                # Relance l'animation à zéro
                self.vals['nbr_sprite'] = 0
                # Change l'animation
                self.game.dict_game['side'] = 'vanish'
                # Si le joueuer appuie sur la touche, on diminue le nombre de tentative
                self.vals['nbr_vanish'] -= 1
                # Effectue l'esquive en fonction de la position du perso (droite/gauche)
                if self.game.dict_game['right'] and self.rect.x > 5:
                    self.rect.x -= 100
                elif not self.game.dict_game['right'] and self.rect.x < 950:
                    self.rect.x += 100

    def attack_up(self, choice):
        '''Attaque en l'air'''
        if choice[pg.K_UP] and self.game.collision(self, self.game.all_objects):
            self.game.dict_game['side'] = 'up'
            self.game.object.rect.y = 250
        if self.game.collision(self, self.game.all_objects):
            self.vals['fall'] = False
            if self.vals['nbr_combo_q'] > 1 and self.rect.y <= 400:
                self.game.dict_game['side'] = 'impact'
                self.vals['fall'] = False
                self.game.object.rect.x -= 100

    def damages(self):
        '''Focntion qui gère les dommages'''
        if self.game.collision(self, self.game.all_objects):
            if not self.vals['attacked']:
                self.vals['health'] -= 0.1

    def block(self):
        '''Fonction qui empêche de se prendre des dégats durant une attaque'''
        self.vals['attacked'] = True
        self.change_animation('shield')
        if self.game.dict_game['right']:
            self.change_animation('shield_right')

    def combo(self, atk_name, key_name):
        '''Fonction attaque qui prend en paramètre le nom de la touche preéssée,
        et qui fait les animations ainsi que le comptage des combos'''
        collide = self.game.collision(self, self.game.all_objects)
        self.vals['nbr_sprite'] = 0
        self.game.dict_game['side'] = atk_name
        if collide:
            # attaque en l'air
            # self.attack_up(choice)
            self.vals[key_name] += 1
            print(self.vals[key_name])
        # Actionne la mécanique de dégats quand il y a une collision
        self.game.strike_collision()

    def attack_down(self, choice):
        if choice[pg.K_DOWN] and self.game.collision(self, self.game.all_objects):
            self.game.dict_game['side'] = 'down'
            while self.game.object.rect.y != 500:
                self.game.object.rect.y += 1

    def update_pv(self):
        return [[self.game.name, self.vals['health']],
                ['punchingball', self.game.object.stats['health']]]
