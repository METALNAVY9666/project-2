'''Module qui génère un punching ball'''
import pygame as pg
from modules.texture_loader import images


class PunchingBall(pg.sprite.Sprite):
    '''cette classe permet de créer un item du jeu'''

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = images['punchingball']
        # Récupère le rectangle de l'image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 300, 500
        self.health = 1000
        # Vérifie si l'item est attaqué ou non
        self.is_attacked = False

    def damage(self):
        '''Fonction qui calcule les dégats reçus'''
        if self.health > 0 and self.rect.x >= 0:
            self.health -= 10
            self.rect.x -= 10

    def forward(self):
        '''Cette fonction permet de déplacer l'objet'''
        if not self.game.collision(self, self.game.all_players):
            self.rect.x += 0.1
