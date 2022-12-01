'''Ce module permet de gérer le joueur, ses déplacements etc'''
import pygame as pg
from modules.texture_loader import persos


class Player(pg.sprite.Sprite):
    '''Cette classe permet de gérer les actions du joueur, ainsi que son apparence.'''

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.sprite = persos[self.game.name]
        self.rect = self.sprite.get_rect()
        self.rect.x, self.rect.y = 800, 500
        self.sprite_x = 50
        self.tab = []
        self.coord = self.coordinates_list()
        self.propertie = self.coord[0]
        # temps entre chaque sprite de l'animation idle en ms
        self.idle_speed = 300
        # somme des temps entres chaque frame
        self.delta_sum = 0

    def properties(self):
        tab = [111, 890, 113, 120]
        if self.game.name == 'vegeta':
            self.sprite = persos[self.game.name]
            tab = [200, 1210, 100, 120]
        return tab

    def move_right(self):
        '''Cette fonction gère les déplacements à droite.'''
        if self.rect.x <= 980:
            self.rect.x += 15

    def move_left(self):
        '''Cette fonction gère les déplacements à gauche.'''
        if self.rect.x > 0:
            self.propertie = self.coord[1]
            self.rect.x -= 20

    def blit_sprite(self, screen, dlt):
        '''Cette fonction sert à afficher le sprite du joueur en continu
        des coordonées demandes.'''
        screen.blit(self.sprite, (self.rect.x, self.rect.y),
                    (self.sprite_x * self.propertie[0],
                    self.propertie[1], self.propertie[2], self.propertie[3]))
        self.delta_sum += dlt
        # si la somme des temps entre les frames est plus grande que 300ms
        if self.delta_sum >= self.idle_speed:
            # changer le sprite
            self.sprite_x += 1
            # remettre la somme des temps à 0
            self.delta_sum = 0
        if self.sprite_x > 2:
            self.sprite_x = 0

    def coordinates_list(self):
        '''Coordonées du spritesheet'''
        self.tab = [[1, 2, 3, 4], [1, 3, 4, 5]]
        if self.game.name == 'goku':
            self.tab = [[111, 890, 113, 120],
                        [1, 1990, 140, 105]]
        elif self.game.name == 'vegeta':
            self.tab = [[200, 1210, 100, 120],
                        [1, 1970, 120, 105]]
        return self.tab
