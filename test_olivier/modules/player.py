'''Ce module permet de gérer le joueur, ses déplacements etc'''
import pygame as pg
from modules.texture_loader import persos
from modules.texture_loader import sprites_images


class Player(pg.sprite.Sprite):
    '''Cette classe permet de gérer les actions du joueur, ainsi que son apparence.'''

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = persos[self.game.name]
        self.rect = self.image.get_rect()
        self.coord = self.coordinates_list()
        self.propertie = self.coord[0]
        self.init_plus()
        self.strike = 10

    def init_plus(self):
        '''Cette fonction permet d'initialiser des élements
        suplémentaires.'''
        self.rect.x, self.rect.y = 900, 500
        self.sprite_x = 50
        # temps entre chaque sprite de l'animation idle en ms
        self.idle_speed = 300
        # somme des temps entres chaque frame
        self.delta_sum = 0
        # Etat pour savoir si le joueur fait rien
        self.pause = True
        # Images complémentaires
        self.images_dict = sprites_images(self.game.name)

    def move_right(self):
        '''Cette fonction gère les déplacements à droite.'''
        if self.rect.x <= 950:
            self.rect.x += 10
            # On change l'image du joueur
            self.images_dict = sprites_images(self.game.name)
            self.image = self.images_dict['right']
            # Le joueur fait une action
            self.pause = False

    def move_left(self):
        '''Cette fonction gère les déplacements à gauche.'''
        if self.rect.x > 5:
            if not self.game.collision(self, self.game.all_objects):
                self.rect.x -= 10
                # On change l'image du joueur
                self.images_dict = sprites_images(self.game.name)
                self.image = self.images_dict['left']
                # Change les coordonnées du perso
                self.pause = False

    def attack(self):
        '''Cette fonction permet de gérer l'attaque d'un perso.'''
        # Le joueur fait une action
        self.pause = False
        self.images_dict = sprites_images(self.game.name)
        self.image = self.images_dict['attack']
        self.rect.x -= 1

    def blit_sprite(self, screen, dlt):
        '''Cette fonction sert à afficher le sprite du joueur en continu
        des coordonées demandes.'''
        if self.pause:
            screen.blit(self.image, (self.rect.x, self.rect.y),
                        (self.sprite_x * self.propertie[0],
                        self.propertie[1], self.propertie[2],
                        self.propertie[3]))
            self.delta_sum += dlt
            # si la somme des temps entre les frames est plus grande que 300ms
            if self.delta_sum >= self.idle_speed:
                # changer le sprite
                self.sprite_x += 1
                # remettre la somme des temps à 0
                self.delta_sum = 0
            if self.sprite_x > 2:
                self.sprite_x = 0
        else:
            # On affiche les actions que le joueur fait
            screen.blit(self.image, (self.rect.x, self.rect.y))

    def coordinates_list(self):
        '''Coordonées du spritesheet'''
        self.tab = [[1, 2, 3, 4], [1, 3, 4, 5]]
        self.image = persos[self.game.name]
        if self.game.name == 'goku':
            if self.game.right:
                # Inverse le sens du spritesheet
                self.image = persos['goku_right']
            self.tab = [[111, 0, 110, 130],
                        [111, 2, 1, 135],
                        [150, 2247, 139, 140]]
        # Change le personnage en fonction du nom
        elif self.game.name == 'vegeta':
            if self.game.right:
                self.image = persos['vegeta_right']
                print(self.game.name)
            self.tab = [[100, 0, 100, 120],
                        [1, 1970, 120, 105],
                        [150, 4400, 135, 140]]
        # Renvoi le tableau des coordonnées
        return self.tab
