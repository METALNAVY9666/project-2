'''Ce module est le jeu, il gère les inputs, les collisions ainsi que
les différents événements dans le jeu.'''
import pygame as pg
from modules.player import Player


class Jeu:
    '''Cette classe a pour but de lancer le jeu, l'arrêter, de gérer les collisions,
    les dessins, les dégats etc...'''

    def __init__(self):
        self.name = 'goku'
        self.player = Player(self)
        self.is_playing = False
        self.fps = 18

    def handle_input(self, EVENTS):
        '''Cette fonction a pour but de récupérer les touches préssées.
        En fonction de celles-ci, on effectue des opération spécifiques.'''
        choice = pg.key.get_pressed()
        if choice[pg.K_RIGHT]:
            self.player.move_right()
        elif choice[pg.K_LEFT]:
            self.player.move_left()
        else:
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

    def update(self, screen, EVENTS, dt):
        '''Cette fonction petrmet de mettre à jour le jeu.'''
        # screen.blit(self.player.image, self.player.rect)
        self.player.blit_sprite(screen, dt)
        self.handle_input(EVENTS)

    def button_pressed():
        joy = []
        for i in range(pg.joystick.get_count()):
            joy.append(pg.joystick.Joystick(i))
        return joy

    def button_dict():
        dico = {
            'x': 0,
            'circle': 1,
            'square': 2,
            'triangle': 3,
            "share": 4,
            'PS': 5,
            'options': 6,
            'left_stick_click': 7,
            'right_stick_click': 8,
            'L1': 9,
            'R1': 10,
            'up_arrow': 11,
            'down_arrow': 12,
            'left_arrow': 13,
            'right_arrow': 14,
            'touchepad': 15
        }
        return dico

    def analog_keys():
        dict = {0: 0, 1: 0, 3: 0, 4: -1, 5: -1}
        return dict
