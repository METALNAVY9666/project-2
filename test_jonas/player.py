import pygame
pygame.init()


class player():

    def __init__(self):
        self.square = pygame.Rect(50, 50, 50, 50)
        self.square_color = 0
        self.color = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        self.motion = [0, 0]
        self.square_rect_x = self.square.x
        self.square_rect_y = self.square.y
        


    def change_color(self):
        self.sqare_color = (self.square_color + 1) % (len(self.color))

    def jump(self):
        while self.square_rect_y > 10:
            self.square.y += 10