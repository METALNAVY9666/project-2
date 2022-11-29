'''Ce module permet de gérer le joueur, ses déplacements etc'''
import pygame as pg


class Player(pg.sprite.Sprite):
    '''Cette classe permet de gérer les actions du joueur, ainsi que son apparence.'''

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.sprite = pg.image.load(f'test_olivier/gfx/base/{self.game.name}_base.png')
        self.rect = self.sprite.get_rect()
        self.rect.x, self.rect.y = 800, 500
        self.sprite_x, self.frame = 50, 111
        self.column, self.line, self.cadre = 890, 97, 120
        # temps entre chaque sprite de l'animation idle en ms
        self.idle_speed = 300
        # somme des temps entres chaque frame
        self.delta_sum = 0

    def move_right(self):
        '''Cette fonction gère les déplacements à droite.'''
        if self.rect.x <= 980:
            self.rect.x += 15

    def move_left(self):
        '''Cette fonction gère les déplacements à gauche.'''
        if self.rect.x > 0:
            self.frame = 0.5
            self.column = 1990
            self.cadre = 100
            self.line = 140
            self.rect.x -= 20

    def blit_sprite(self, screen, dt):
        '''Cette fonction sert à afficher le sprite du joueur en continu
        des coordonées demandes.'''
        screen.blit(self.sprite, (self.rect.x, self.rect.y),
                   (self.sprite_x * self.frame, self.column, self.line, self.cadre))
        self.delta_sum += dt
        # si la somme des temps entre les frames est plus grande que 300ms
        if self.delta_sum >= self.idle_speed:
            # changer le sprite
            self.sprite_x += 1
            # remettre la somme des temps à 0
            self.delta_sum = 0
        if self.sprite_x > 5:
            self.sprite_x = 0
