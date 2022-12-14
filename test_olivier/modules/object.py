'''Module qui génère un punching ball'''
import pygame as pg
from modules.texture_loader import images


class PunchingBall(pg.sprite.Sprite):
    '''Cette classe permet de créer un item du jeu'''

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = images['punchingball']
        # Récupère le rectangle de l'image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 300, 510
        self.stats = {'health': 200, 'max_health': 200,
                      'fall': True, 'is_attacked': True}

    def damage(self):
        '''Fonction qui calcule les dégats reçus'''
        if self.stats['health'] > 0 and self.rect.x >= 0:
            self.stats['health'] -= 10
            # self.rect.x -= 30

    def forward(self):
        '''Cette fonction permet de déplacer l'objet'''
        if not self.game.collision(self, self.game.all_players):
            self.rect.x += 0.1

    def gravity_object(self):
        '''Gravité pour l'objet'''
        if self.rect.y < 500:
            self.rect.y += 5
