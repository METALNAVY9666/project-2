"""Module qui gère les attaques spéciales"""
import pygame as pg


class Special(pg.sprite.Sprite):
    """Docstring à faire"""
    def __init__(self, game):
        super().__init__()
        self.game = game
        print('la spé de', self.game.name, 'est chargée.')

    def spe(self):
        "Docstring à faire"
        if self.game.name == 'luffy':
            self.game.name = 'gear4'
            self.game.player_0.vals['strike'] = 30
        elif self.game.name == 'gear4':
            self.game.name = 'luffy'
