'''Ce module permet de gérer le joueur, ses déplacements etc'''
import pygame as pg
from modules.texture_loader import sprites_images, sprite_tab


class Player(pg.sprite.Sprite):
    '''Cette classe permet de gérer les actions du joueur, ainsi que son apparence.'''

    def __init__(self, game):
        super().__init__()
        self.game = game
        # Dictionnaire des attributs du personnage
        self.stats_dict = {
            'nbr_sprite': 0, 'strike': 10,
            'max_height': 400, 'jumps': 1,
            'current_height': 0, 'pause': True,
            'idle_speed': 125, 'delta_sum': 0,
            'nbr_combo': 0, 'nbr_vanish': 4,
            'max_health': 100, 'health': 100,
            'attacked': False}
        # Récupération du tableau des images du persos
        self.tab = sprite_tab(self.game.name, self.game.dict_game['side'])
        # Affectation de l'image
        self.image = self.tab[self.stats_dict['nbr_sprite']]
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
        self.stats_dict['pause'] = False

    def move_controller(self, actions):
        "Cette fonction gère les déplacements de droite à gauche a la manette"
        # Vérifie s'il n'y a pas de collisions
        test = not self.game.collision(self, self.game.all_objects)
        if test or (not test and self.rect.y <= 500):
            if self.rect.x < 950:
                if actions.type == pg.JOYAXISMOTION:
                    if actions.axis == 0:
                        self.motion[actions.axis] = actions.value * 10
                        self.rect.x += self.motion[actions.axis]
                        if actions.value < 0:
                            self.stats_dict['pause'] = False
                            # On change l'image du joueur
                            self.change_animation('right')
                        else:
                            self.stats_dict['pause'] = False
                            self.change_animation('left')

    def attack(self, event, choice):
        '''Cette fonction permet de gérer l'attaque d'un perso.'''
        # Le joueur fait une action
        if 0 <= self.stats_dict['nbr_combo'] < 3:
            if event.key == pg.K_q and self.stats_dict['nbr_combo'] < 1:
                self.stats_dict['nbr_sprite'] = 0
                self.game.dict_game['side'] = 'attack'
                self.attack_up(choice)
                if self.game.collision(self, self.game.all_objects) and self.stats_dict['nbr_combo'] < 1:
                    self.stats_dict['nbr_combo'] += 1
                    print(self.stats_dict['nbr_combo'])
                # Actionne la mécanique de dégats quand il y a une collision
                self.game.strike_collision()
            if event.key == pg.K_w and self.stats_dict['nbr_combo'] < 3:
                self.stats_dict['nbr_sprite'] = 0
                self.game.dict_game['side'] = 'impact'
                if self.game.collision(self, self.game.all_objects) and self.stats_dict['nbr_combo'] >= 1:
                    # Actionne la mécanique de dégats quand il y a une collision
                    self.stats_dict['nbr_combo'] += 1
                    print(self.stats_dict['nbr_combo'])
                    self.game.strike_collision()
        if self.stats_dict['nbr_combo'] >= 2:
            pg.time.wait(1000)
            self.game.dict_game['side'] = 'spe'
            self.game.object.rect.x -= 200
        if not self.game.collision(self, self.game.all_objects):
            self.stats_dict['nbr_combo'] = 0
        # Augemente le nombre de combo
        # A voir ~~~~~

    def jump(self):
        '''Fonction saut'''
        # Vérfie si le perso est inférieur à la hauteur de saut max
        if self.stats_dict['current_height'] <= self.stats_dict['max_height']:
            # Vérifie si le perso n'a pas déjà sauté deux fois
            if self.stats_dict['jumps'] < 2:
                # Saute
                self.rect.y -= 25
                self.stats_dict['current_height'] += 25
            # Si le joueur a atteint la hauteur maximale, il redescend
            if self.stats_dict['current_height'] >= self.stats_dict['max_height']:
                self.stats_dict['jumps'] = 3

    def gravity(self):
        '''Fonction qui simule une gravité'''
        # Le joueur tombe tant qu'il n'est pas au sol
        if self.rect.y <= 500 and not self.game.collision(self, self.game.all_objects):
            # fait tomber le perso et change l'image
            self.stats_dict['pause'] = False
            self.rect.y += 7
            self.change_animation('jump')
            # Change l'animation si on est à droite ou à gauche
            if self.game.dict_game['right']:
                self.change_animation('jump_right')
        # Sinon, on réinitialise son nombre de sauts à zéro
        elif self.rect.y >= 500 or self.game.collision(self, self.game.all_objects):
            self.stats_dict['jumps'] = 0
            # Réaffecte à zéro la hauteur actuelle
            self.stats_dict['current_height'] = 0

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
        if self.stats_dict['pause']:
            # Changement d'image
            self.image = self.position()
            self.stats_dict['delta_sum'] += dlt
            # si la somme des temps entre les frames est plus grande que 300ms
            if self.stats_dict['delta_sum'] >= self.stats_dict['idle_speed']:
                # changer le sprite
                self.stats_dict['nbr_sprite'] += 1
                # remettre la somme des temps à 0
                self.stats_dict['delta_sum'] = 0
            if self.stats_dict['nbr_sprite'] >= 5:
                self.stats_dict['nbr_sprite'] = 0
                # Si le joueur ne fait pas d'attaque, on remet l'animation de base
                self.game.dict_game['side'] = 'left'

    def position(self):
        '''Fonction qui change le tableau d'image en fonction de la position du persos'''
        # Vérifie si le personnage est à droite ou à gauche
        self.tab = sprite_tab(self.game.name, self.game.dict_game['side'])
        # Réaffecte l'image en fonction de la position
        self.image = self.tab[self.stats_dict['nbr_sprite']]
        # Inverse les images en cas d'attaque à droite
        if self.game.dict_game['right']:
            self.image = pg.transform.flip(
                self.tab[self.stats_dict['nbr_sprite']], True, False)
        return self.image

    def vanish(self, event):
        '''Fonction qui actionne une esquive, le personnage peut esquiver une attaque 4 fois'''
        # L'esquve se fait que si le joueur se prend des dégats
        if self.game.collision(self, self.game.all_objects):
            # On vérifie le ombre de tentatives autorisées
            if self.stats_dict['nbr_vanish'] > 0 and event.key == pg.K_d:
                # Relance l'animation à zéro
                self.stats_dict['nbr_sprite'] = 0
                # Change l'animation
                self.game.dict_game['side'] = 'vanish'
                # Si le joueuer appuie sur la touche, on diminue le nombre de tentative
                self.stats_dict['nbr_vanish'] -= 1
                # Effectue l'esquive en fonction de la position du perso (droite/gauche)
                if self.game.dict_game['right'] and self.rect.x > 5:
                    self.rect.x -= 100
                elif not self.game.dict_game['right'] and self.rect.x < 950:
                    self.rect.x += 100

    def attack_up(self, choice):
        '''Attaque en l'air'''
        if choice[pg.K_UP] and self.game.collision(self, self.game.all_objects):
            self.game.dict_game['side'] = 'combo'
            self.game.object.rect.y -= 100
            self.game.object.rect.x -= 100

    def damages(self):
        '''Focntion qui gère les dommages'''
        if self.game.collision(self, self.game.all_objects):
            if not self.stats_dict['attacked']:
                self.stats_dict['health'] -= 0.1

    def block(self):
        '''Fonction qui empêche de se prendre des dégats durant une attaque'''
        self.stats_dict['attacked'] = True
        self.change_animation('shield')
        if self.game.dict_game['right']:
            self.change_animation('shield_right')
