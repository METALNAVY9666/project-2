"""Module qui gère les attaques spéciales"""
import pygame as pg


class Special(pg.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game

    def spe_luffy(self):
        if self.game.name == 'luffy':
            print('La spé de luffy est chargées.')

    def spe_goku(self):
        if self.game.name == 'goku':
            print('La spé de luffy est chargée.')

    def spe_itachi(self):
        if self.game.name == 'itachi':
            print('La spé d\'itachi est chargée')

    def spe_kim(self):
        if self.game.name == 'kim':
            print('La spé de kim est chargéee')

    def spe_vegeta(self):
        if self.game.name == 'vegeta':
            print('La spé de vegeta est lancée')
