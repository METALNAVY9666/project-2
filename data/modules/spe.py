"""Module qui gère les attaques spéciales"""
import pygame as pg


class Special(pg.sprite.Sprite):
    """Docstring à faire"""
    def __init__(self, game):
        super().__init__()
        self.game = game
        print('la spé de', self.game.name, 'est chargée.')
        self.pl1_speed = self.game.player_1.pkg["dimensions"][0] / 1920 * 3
        

    def spe(self):
        "Docstring à faire"
        if self.game.name == 'luffy':
            if self.game.player_0.vals["percent_ult"] >= 130:
                self.game.name = 'gear4'
                self.game.player_0.vals['strike'] = 30
        elif self.game.name == 'gear4':
            self.game.name = 'luffy'
        elif self.game.name == 'itachi':
            self.game.player_1.physics["speed"] = self.pl1_speed
