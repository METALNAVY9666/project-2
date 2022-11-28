import pygame as pg
from modules.player import Player


class Jeu:
    def __init__(self):
        self.player = Player()
        self.is_playing = False
        self.fps = 25

    def handle_input(self):
        choice = pg.key.get_pressed()
        if choice[pg.K_RIGHT]:
            self.player.move_right()
        elif choice[pg.K_LEFT]:
            self.player.move_left()
            self.player.i = 11
            self.player.change_nanimation()
        elif choice[pg.K_r]:
            self.player.change_nanimation()
        else:
            self.player.i = 0
            self.player.image = self.player.images_attack('goku', self.player.i)

    def update(self, screen, EVENTS):
        screen.blit(self.player.image, self.player.rect)
        self.handle_input()
