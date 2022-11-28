import pygame as pg
from modules import animation


class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.i = 0
        self.image = self.images_attack('goku', self.i)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 10, 500
    
    def images_attack(self, name, value):
        images = pg.image.load(f'gfx/{name}/{name}{value}.png')
        return images
        
        
    def move_right(self):
        if self.rect.x <= 980:
            self.rect.x += 15

    def move_left(self):
        if self.rect.x > 0:
            self.rect.x -= 15
    
    def indice(self, value):
        if 0 <= value < 10:
            value += 1
            if value == 10:
                value = 0
        elif value > 10:
            value = 11
        return value
    
    def change_nanimation(self):
        self.i = self.indice(self.i)
        self.image = self.images_attack('goku', self.i)
