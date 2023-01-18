"""import pygame
import pygame._sdl2
from pygame._sdl2.controller import Controller

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
            """



import sys
import pygame
import pygame._sdl2
from pygame._sdl2.controller import Controller


pygame.init()
window = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Testing controllers")

font = pygame.font.Font(None, 30)

clock = pygame.time.Clock()

pygame._sdl2.controller.init()

def debug(info, y=10, x=20):
    display_surf = pygame.display.get_surface()
    debug_surf = font.render(str(info), False, 'white', 'black')
    debug_rect = debug_surf.get_rect(topleft=(x, y))
    display_surf.blit(debug_surf, debug_rect)

def reset_joysticks():
    return [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]


joysticks = reset_joysticks()

debug_messages = []

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()
        if event.type in [pygame.JOYDEVICEADDED, pygame.JOYDEVICEREMOVED]:
            joysticks = reset_joysticks()
    
    window.fill('white')
    
    for joystick in joysticks:
        controller = Controller.from_joystick(joystick)
        js = [joystick.get_guid(), joystick.get_name()]
        for button in range(joystick.get_numbuttons()):
            btn_message = 'Button ' + str(button) + ': ' + str(controller.get_button(button))
            js.append(btn_message)
        for axis in range(joystick.get_numaxes()):
            axis_message = 'Axis ' + str(axis) + ': ' + str(controller.get_axis(axis))
            js.append(axis_message)
        for hat in range(joystick.get_numhats()):
            
            hat_message = 'Hat ' + str(hat) + ': ' + str(joystick.get_hat(hat))
            js.append(hat_message)
        
        debug_messages.append(js)
    
    for js, dbg_messages in enumerate(debug_messages):
        for i, message in enumerate(dbg_messages):
            l = 20 if js == 0 else js * 420
            debug(message, i * 18, l)

    pygame.display.flip()
    clock.tick(60)
    debug_messages.clear()


"""
import pygame
import os
from time import sleep

pygame.init()
xboxController = pygame.joystick.Joystick(0)

def getInputs(controller:pygame.joystick.Joystick) -> dict:
    '''Returns a dict of each button mapped to its value'''
    return {
            "B": bool(controller.get_button(1)),
            "A": bool(controller.get_button(0)),
            "X": bool(controller.get_button(2)),
            "Y": bool(controller.get_button(3)),
            "LB": bool(xboxController.get_button(4)),
            "RB": bool(controller.get_button(5)),
            "BACK": bool(controller.get_button(6)),
            "START": bool(controller.get_button(7)),
            "Lstick_pressed": bool(controller.get_button(8)),
            "Rstick_pressed": bool(controller.get_button(9)),
            "Lstick_x": round(controller.get_axis(0), 3),
            "Lstick_y": round(-controller.get_axis(1), 3), #  value inverted so forward is positive
            "Rstick_x": round(controller.get_axis(2), 3),
            "Rstick_y": round(-controller.get_axis(3), 3), # value inverted so forward is positive
            "Ltrig": round((controller.get_axis(4)+1)/2, 3), # value mapped from (-1.0, 1.0) to (0.0, 1.0)
            "Rtrig": round((controller.get_axis(5)+1)/2, 3), # value mapped from (-1.0, 1.0) to (0.0, 1.0)

        }

def display():
    while True:
         # updates the controller input values
        pygame.event.get()
        controlMap = getInputs(xboxController)
            
        # clears the screen every frame. should work on both linux and windows
        os.system('cls' if os.name=='nt' else 'clear')
        
        # print each controller input with its value
        s = ''
        for item in controlMap:
            s = '{}\n{}: {}'.format(s, str(item), str(controlMap[item]))
        print(s)
        
        # hacky solution to reduce screen flickering
        # NOTE: this creates latency so the values shown in the console do not reflect actual response times
        sleep(0.05)
        
        
if __name__ == '__main__':
    display()
    """