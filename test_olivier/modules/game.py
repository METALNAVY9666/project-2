'''Ce module est le jeu, il gère les inputs, les collisions ainsi que
les différents événements dans le jeu.'''
import pygame as pg
from modules.player import Player


class Jeu:
    '''Cette classe a pour but de lancer le jeu, l'arrêter, de gérer les collisions,
    les dessins, les dégats etc...'''

    def __init__(self):
        self.player = Player(self)
        self.is_playing = False
        self.fps = 18

    def handle_input(self):
        '''Cette fonction a pour but de récupérer les touches préssées.
        En fonction de celles-ci, on effectue des opération spécifiques.'''
        choice = pg.key.get_pressed()
        if choice[pg.K_RIGHT]:
            self.player.move_right()
        elif choice[pg.K_LEFT]:
            self.player.move_left()
        else:
            self.player.image = pg.image.load('test_olivier/gfx/goku/hero_base/goku.png')
            self.player.frame, self.player.column = 111, 890
            self.player.line, self.player.cadre = 97, 120

    def collison(self, sprite, group):
        '''Cette fonction renvoi un bouléen,
        qui est sur True quand il y a une collision entre
        un sprite et un groupe de sprites. Le cas échéant, le
        bouléen est sur False.'''
        # Vérifie si il y a collision ou non
        return pg.sprite.spritecollide(sprite, group,
                                       False, pg.sprite.collide_mask)

    def update(self, screen, EVENTS):
        '''Cette fonction petrmet de mettre à jour le jeu.'''
        # screen.blit(self.player.image, self.player.rect)
        self.player.blit_sprite(screen)
        self.handle_input()
