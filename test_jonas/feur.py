#Partie de Jonas: les controles a la manette
from player import *
import sys
import pygame
from pygame.locals import *
pygame.init()


pygame.display.set_caption('test_manettes') #Create the name of the game
screen = pygame.display.set_mode((500, 500), 0, 32) #Create a screen
clock = pygame.time.Clock() #Create a clock for manage fps

pygame.joystick.init() #initialise le module joystick
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
#Permet de savoir le nombre de manettes utilisés
for joystick in joysticks:
    print(joystick.get_name()) #Permet de connaitre la manette utilisée.


#Create a square
carre = player()

while True:

    screen.fill((0, 0, 0))

    pygame.draw.rect(screen, carre.color[carre.square_color], carre.square)
    if abs(carre.motion[0]) < 0.1:
        carre.motion[0] = 0
    if abs(carre.motion[1]) < 0.1:
        carre.motion[1] = 0
    carre.square.x += carre.motion[0] * 10 #Modifie les abscisses (déplace l'objet)
    carre.square.y += carre.motion[1] * 10 #Modifie les ordonnées (déplace l'objet)
    #print(my_square.x, my_square.y)

    for event in pygame.event.get():

        if event.type == JOYBUTTONDOWN:
            print(event)


            if event.button == 0: #If button "0" is pressing:
                carre.square_color = (carre.square_color + 1) % len(carre.color) #Change square color

            if event.button == 1:
                pass
            if event.button == 2:
                pass
            if event.button == 3:
                pass
            if event.button == 4:
                pass
            if event.button == 5:
                pass



        if event.type == JOYBUTTONUP:
            """print(event)"""

        if event.type == JOYAXISMOTION: #If controller joys are moving:
            if event.axis < 2: #If joy left is moving
                if (abs(event.value) > 0.1 and carre.square.left > 0
                and carre.square.right < screen.get_width()
                and carre.square.y > 0
                and carre.square.bottom < screen.get_height()): #If axis > 0.1 (control dead zone)
                    print(event)
                    carre.motion[event.axis] = event.value #modify motion than allows move
                else:
                    carre.motion[event.axis] = 0 #modify motion than allow don't move
            """
            #same but with the joy right
            if event.axis >= 2 and event.axis < 4:
                if abs(event.value) > 0.1:
                    print("CA FONCTIONNE !!!")
                    motion[event.axis - 2] = event.value
                else:
                    motion[event.axis - 2] = 0
            """

        #Permet de savoir si une manette a été rajoutée
        if event.type == JOYDEVICEADDED:
            joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
            for joystick in joysticks:
                print(joystick.get_name())

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
