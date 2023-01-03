'''Ce module permet de gérer le joueur, ses déplacements etc'''
import pygame as pg
from modules.texture_loader import sprites_images, sprite_tab, sprite_tab_right


class Player(pg.sprite.Sprite):
    '''Cette classe permet de gérer les actions du joueur, ainsi que son apparence.'''

    def __init__(self, game):
        super().__init__()
        self.game = game
        # Numéro du sprite que l'on doit blit
        self.sprite_x = 0
        # Récupération du tableau des images du persos
        self.tab = sprite_tab(self.game.name)
        # Affectation de l'image
        self.image = self.tab[self.sprite_x]
        # Récupération du rectangle de l'image
        self.rect = self.image.get_rect()
        # Variable en plus
        self.init_plus()
        self.strike = 10
        # Nombre de sauts max
        self.jumps = 1


    def init_plus(self):
        '''Cette fonction permet d'initialiser des élements
        suplémentaires.'''
        self.rect.x, self.rect.y = 900, 400
        # Temps entre chaque sprite de l'animation idle en ms
        self.idle_speed = 300
        # Somme des temps entres chaque frame
        self.delta_sum = 0
        # Bouléen pour savoir si le joueur fait rien ou pas
        self.pause = True
        # Images complémentaires
        self.images_dict = sprites_images(self.game.name)
        # Nombre de combos
        self.combo = 0

    def move_right(self):
        '''Cette fonction gère les déplacements à droite.'''
        if self.rect.x <= 950:
            if not self.game.collision(self, self.game.all_objects):
                self.rect.x += 10
                # On change l'image du joueur
                self.change_animation('right')
                # Le joueur fait une action
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

    def attack(self):
        '''Cette fonction permet de gérer l'attaque d'un perso.'''
        # Le joueur fait une action
        self.pause = False
        self.change_animation('attack')
        if not self.game.collision(self, self.game.all_objects):
            self.rect.x -= 1

    def jump(self):
        '''Fonction saut'''
        # Vérfie si le perso est inférieur à la hauteur de saut max
        if self.rect.y >= 300:
            # Vérifie si le perso n'a pas déjà sauté deux fois
            if self.jumps < 2:
                # Saute
                self.rect.y -= 25
            # Si le joueur a atteint la hauteur maximale, il redescend
            if self.rect.y <= 300:
                self.jumps = 3

    def gravity(self):
        '''Fonction qui simule une gravité'''
        # Le joueur tombe tant qu'il n'est pas au sol
        if self.rect.y <= 500 and not self.game.collision(self, self.game.all_objects):
            # fait tomber le perso et change l'image
            self.pause = False
            self.rect.y += 4
            self.change_animation('jump')
            if self.game.right:
                self.change_animation('jump_right')
        # Sinon, on réinitialise son nombre de sauts à zéro
        elif self.rect.y >= 500 or self.game.collision(self, self.game.all_objects):
            self.jumps = 0

    def change_animation(self, name):
        '''Fonction qui change l'image du personnage'''
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
            # Affichage
            screen.blit(self.image, (self.rect.x, self.rect.y))
            self.delta_sum += dlt
            # si la somme des temps entre les frames est plus grande que 300ms
            if self.delta_sum >= self.idle_speed:
                # changer le sprite
                self.sprite_x += 1
                # remettre la somme des temps à 0
                self.delta_sum = 0
            if self.sprite_x >= 5:
                self.sprite_x = 0

    def position(self):
        '''Fonction qui change le tableau d'image en fonction de la position du persos'''
        self.tab = sprite_tab(self.game.name)
        # Vérifie si le personnage est à droite ou à gauche
        if self.game.right:
            self.tab = sprite_tab_right(self.game.name)
        # Réaffecte l'image en fonction de la position
        self.image = self.tab[self.sprite_x]
        return self.image
