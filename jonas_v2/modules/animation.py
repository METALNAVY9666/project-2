'''Ce module gère les animations des personnages.'''
import pygame as pg
from random import randint as rd


class AnimateSprite(pg.sprite.Sprite):
    '''Cett classe a pour but d'animer un sprite.'''

    def __init__(self, name):
        super().__init__()
        self.image = pg.image.load(f'gfx/{name}/hero_base/{name}.png')
        self.pos_image = rd(0, 1)
        self.images = self.load_images_dict().get(name)
        self.animation = False

    def start_animation(self):
        self.animation = True

    def update_animation(self):
        self.animate()

    def animate(self):
        if self.animation:
            self.pos_image += 1
            if self.pos_image >= len(self.images):
                self.pos_image = 0
                self.animation = False
            self.image = self.images[self.pos_image]
            print(self.pos_image)

    def load_sprite(self, name, number):
        '''Cette fonction a pour but de génerer un tableau
        contenant les chemins relatifs permettant d'accéder aux sprites.'''
        images = []
        path = f'gfx/{name}/{name}'
        for element in range(1, number):
            image_path = path + str(element) + '.png'
            images.append(pg.image.load(image_path))
        return images

    def load_images_dict(self):
        '''Cette fonction permet de charger les images des sprites.'''
        animations = {
            'goku': self.load_sprite('goku', 11)
        }
        return animations
