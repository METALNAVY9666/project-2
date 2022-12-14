from re import S
import pygame 
from controllers import *
pygame.init()

class square():

    def __init__(self):
        self.my_square = pygame.Rect(50, 50, 50, 50)
        self.my_square_color = 0 #Create the sqare's color
        self.colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        self.motion = [0, 0]
        self.controllers = touches(event)

    def change(self):
        if self.controllers == 0:
            self.my_square_color = (self.my_square_color + 1) % len(self.colors)
        