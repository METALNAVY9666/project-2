"""Module qui gère les attaques spéciales"""
import pygame as pg


class Special(pg.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        print('la spé de', self.game.name, 'est chargée.')

    def spe(self, lock):
        if self.game.name == 'luffy' and lock:
            self.game.name = 'gear4'
        elif self.game.name == 'gear4':
            self.game.name = 'luffy'