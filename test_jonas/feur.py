import sys
import pygame
from pygame.locals import *
pygame.init()
"""
import pygame as pg

def button_pressed(self):
        '''A rajouter'''
        joy = []
        for i in range(pg.joystick.get_count()):
            joy.append(pg.joystick.Joystick(i))
        return joy

def button_dict(self):
    '''En faire un fichier Json'''
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

def analog_keys(self):
    '''A rajouter'''
    dict = {0: 0, 1: 0, 3: 0, 4: -1, 5: -1}
    return dict

def joy(self):
    
    A rajouter
    

    joysticks = button_pressed()
    button_keys = button_dict()
    analog_key = {0: 0, 1: 0, 3: 0, 4: -1, 5: -1}
    for joystick in joysticks:
        joystick.init()
"""

pygame.display.set_caption('game base')
screen = pygame.display.set_mode((500, 500), 0, 32)
clock = pygame.time.Clock()

pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
print(joysticks)
for joystick in joysticks:
    print(joystick.get_name())

my_square = pygame.Rect(50, 50, 50, 50)
my_square_color = 0
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
motion = [0, 0]

while True:

    screen.fill((0, 0, 1))

    pygame.draw.rect(screen, colors[my_square_color], my_square)
    if abs(motion[0]) < 0.1:
        motion[0] = 0
    if abs(motion[1]) < 0.1:
        motion[1] = 0
    my_square.x += motion[0] * 10
    my_square.y += motion[1] * 10
    print(my_square)

    for event in pygame.event.get():
        if event.type == JOYBUTTONDOWN:
            print(event)
            if event.button == 0:
                my_square_color = (my_square_color + 1) % len(colors)
        if event.type == JOYBUTTONUP:
            print(event)
        if event.type == JOYAXISMOTION:
            print(event)
            if event.axis < 2:
                motion[event.axis] = event.value
        if event.type == JOYHATMOTION:
            print(event)
        if event.type == JOYDEVICEADDED:
            joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
            for joystick in joysticks:
                print(joystick.get_name())
        if event.type == JOYDEVICEREMOVED:
            joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

    pygame.display.update()
    clock.tick(60)