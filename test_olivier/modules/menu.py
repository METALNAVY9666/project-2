import pygame as pg


class Menu:
    def __init__(self):
        self.image = pg.image.load('test_olivier/gfx/images/square.png')
        self.image = pg.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect()
        self.rect.x = 120
        self.rect.y = 70
