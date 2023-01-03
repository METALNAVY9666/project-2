'''Ce module permet de gérer le joueur, ses déplacements etc'''
import pygame as pg
from modules.texture_loader import sprites_images, sprite_tab


class Player(pg.sprite.Sprite):
    '''Cette classe permet de gérer les actions du joueur, ainsi que son apparence.'''

    def __init__(self, game):
        super().__init__()
        self.game = game
        # Numéro du sprite que l'on doit blit
        self.sprite_x = 0
        # Récupération du tableau des images du persos
        self.tab = sprite_tab(self.game.name, self.game.side)
        # Affectation de l'image
        self.image = self.tab[self.sprite_x]
        # Récupération du rectangle de l'image
        self.rect = self.image.get_rect()
        # Variable en plus
        self.init_plus()
        self.strike = 10
        # Nombre de sauts max
        self.jumps = 1
        # Hauteur max
        self.max_height = 400
        # Hauteur actuelle
        self.current_height = 0
        # Bouléen pour savoir si le joueur fait rien ou pas
        self.pause = True

    def init_plus(self):
        '''Cette fonction permet d'initialiser des élements
        suplémentaires.'''
        self.rect.x, self.rect.y = 900, 400
        # Temps entre chaque sprite de l'animation idle en ms
        self.idle_speed = 125
        # Somme des temps entres chaque frame
        self.delta_sum = 0
        # Images complémentaires
        self.images_dict = sprites_images(self.game.name)
        # Nombre de combos
        self.combo = 0
        # Tableau d'actions
        self.combo_tab = ['attack', 'combo',
                          'final', 'impact']
        # Nombre maximum d'esquive
        self.nbr_vanish = 4

    def move_right(self):
        '''Cette fonction gère les déplacements à droite.'''
        if self.rect.x <= 950:
            if not self.game.collision(self, self.game.all_objects):
                self.rect.x += 10
                # On change l'image du joueur
                self.change_animation('right')
                # Le joueur fait une action, donc on passe le bouléen sur False
                self.pause = False

    def move_left(self):
        '''Cette fonction gère les déplacements à gauche.'''
        if self.rect.x > 5:
            if not self.game.collision(self, self.game.all_objects):
                self.rect.x -= 10
                # On change l'image du joueur
                self.change_animation('left')
                # Change l'état du personnage
                self.pause = False

    def attack(self, event):
        '''Cette fonction permet de gérer l'attaque d'un perso.'''
        # Le joueur fait une action
        if event.key == pg.K_q:
            self.sprite_x = 0
            # Si il y a une collision, on lance une attaque spécial
            if self.game.collision(self, self.game.all_objects):
                if self.combo == 3:
                    self.game.object.rect.y -= 100
                    self.game.object.rect.x -= 100
                    self.rect.x += 20
            # On récupère les images d'attaques du perso en fonction duu combo
            self.game.side = self.combo_tab[self.combo]
            # Actionne la mécanique de dégats quand il y a une collision
            self.game.strike_collision()
            # Augemente le nombre de combo
            self.combo_strike()

    def jump(self):
        '''Fonction saut'''
        # Vérfie si le perso est inférieur à la hauteur de saut max
        if self.current_height <= self.max_height:
            # Vérifie si le perso n'a pas déjà sauté deux fois
            if self.jumps < 2:
                # Saute
                self.rect.y -= 25
                self.current_height += 25
            # Si le joueur a atteint la hauteur maximale, il redescend
            if self.current_height >= self.max_height:
                self.jumps = 3

    def gravity(self):
        '''Fonction qui simule une gravité'''
        # Le joueur tombe tant qu'il n'est pas au sol
        if self.rect.y <= 500 and not self.game.collision(self, self.game.all_objects):
            # fait tomber le perso et change l'image
            self.pause = False
            self.rect.y += 4
            self.change_animation('jump')
            # Change l'animation si on est à droite ou à gauche
            if self.game.right:
                self.change_animation('jump_right')
        # Sinon, on réinitialise son nombre de sauts à zéro
        elif self.rect.y >= 500 or self.game.collision(self, self.game.all_objects):
            self.jumps = 0
            # Réaffecte à zéro la hauteur actuelle
            self.current_height = 0

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
        if self.pause:
            # Changement d'image
            self.image = self.position()
            self.delta_sum += dlt
            # si la somme des temps entre les frames est plus grande que 300ms
            if self.delta_sum >= self.idle_speed:
                # changer le sprite
                self.sprite_x += 1
                # remettre la somme des temps à 0
                self.delta_sum = 0
            if self.sprite_x >= 5:
                self.sprite_x = 0
                # Si le joueur ne fait pas d'attaque, on remet l'animation de base
                self.game.side = 'left'

    def position(self):
        '''Fonction qui change le tableau d'image en fonction de la position du persos'''
        # Vérifie si le personnage est à droite ou à gauche
        self.tab = sprite_tab(self.game.name, self.game.side)
        # Réaffecte l'image en fonction de la position
        self.image = self.tab[self.sprite_x]
        # Inverse les images en cas d'attaque à droite
        if self.game.right:
            self.image = pg.transform.flip(
                self.tab[self.sprite_x], True, False)
        return self.image

    def combo_strike(self):
        '''Fonction qui a pour but de simuler un combo entier,
        on prend en compte le nobre de fois que le jouueur appuie sur la touche q'''
        # A chaque fois que l'utlisateur lance une attaque, augmente le nombre de combo
        if self.combo < 3:
            # Max d'attaque
            self.combo += 1
            if not self.game.collision(self, self.game.all_objects) and self.combo >= 2:
                self.combo = 0
        else:
            # Fin du combo
            print('fin de combo')
            self.combo = 0
        print(self.combo)

    def vanish(self, event):
        '''Fonction qui actionne une esquive, le personnage peut esquiver une attaque 4 fois'''
        # L'esquve se fait que si le joueur se prend des dégats
        if self.game.collision(self, self.game.all_objects):
            # On vérifie le ombre de tentatives autorisées
            if self.nbr_vanish > 0 and event.key == pg.K_d:
                # Change l'animation
                self.game.side = 'vanish'
                # Si le joueuer appuie sur la toouche, on diminue le nombre de tentative
                self.nbr_vanish -= 1
                # Effectue l'esquive en fonction de la position du perso (droite/gauche)
                if self.game.right and self.rect.x > 5:
                    self.rect.x -= 100
                elif not self.game.right and self.rect.x < 950:
                    self.rect.x += 100
