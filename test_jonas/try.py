import pygame
pygame.init()


background = pygame.display.set_caption("JEU")
screen = pygame.display.set_mode((1080, 720))
background = pygame.image.load('test_jonas/assets/retro.jpg')
background = pygame.transform.scale(background, (500,300))
run = True

while run:
    screen.blit(background, (0, 0))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()