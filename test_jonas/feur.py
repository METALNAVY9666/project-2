#Partie de Jonas: les controles a la manette
from player import *
import sys
import pygame
from pygame.locals import *
import pygame._sdl2
from pygame._sdl2.controller import Controller
pygame.init()
pygame._sdl2.controller.init()


pygame.display.set_caption('test_manettes') #Create the name of the game
screen = pygame.display.set_mode((500, 500), 0, 32) #Create a screen
clock = pygame.time.Clock() #Create a clock for manage fps

pygame.joystick.init() #initialise le module joystick
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
#Permet de savoir le nombre de manettes utilisés

for joystick in joysticks:
    controller = Controller.from_joystick(joystick)
    



#Create a square
carre = player()
carre2 = player2()

while True:


    screen.fill((0, 0, 0))

    pygame.draw.rect(screen, carre.color[carre.square_color], carre.square)
    pygame.draw.rect(screen, carre2.color[carre2.square_color], carre2.square)
    

    if abs(carre.motion[0]) < 0.1:
        carre.motion[0] = 0
    if abs(carre.motion[1]) < 0.1:
        carre.motion[1] = 0
    carre.square.x += carre.motion[0] * 10 #Modifie les abscisses (déplace l'objet)
    carre.square.y += carre.motion[1] * 10 #Modifie les ordonnées (déplace l'objet)

    for event in pygame.event.get():

        
        if controller.get_button(1):
            print("Yo")
        

        if controller.get_button(0): #If button "0" is pressing:
            carre.square_color = (carre.square_color + 1) % len(carre.color) #Change square color
            pygame.time.get_ticks()


        if event.type == JOYBUTTONDOWN:
            if event.button == 2:
                pass
            if event.button == 3:
                pass
            if event.button == 4:
                pass
            if event.button == 5:
                pass

        if event.type == JOYAXISMOTION:
            if event.axis == 0:
                carre.motion[0] = controller.get_axis(0) / 14000
            if event.axis == 1:
                carre.motion[1] = controller.get_axis(1) / 14000


        if event.type == JOYBUTTONUP:
            print(event)

        
            

        #Permet de savoir si une manette a été rajoutée
        if event.type == JOYDEVICEADDED:
            joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

        #Permet de savoir si une manette a été enlevée
        if event.type == JOYDEVICEREMOVED:
            joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type in (KEYDOWN, QUIT):
            if event.key in (K_ESCAPE, QUIT):
                pygame.quit()
                sys.exit()

    pygame.display.update()
    clock.tick(60)
