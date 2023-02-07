
""" Module qui est chargé d'importer les images qui serviront pour le module Menu et Choix_Perso """

import pygame

pygame.display.init()
surface = pygame.display.set_mode((1280, 720))

# Importation de l'image qui feras office de Menu du jeu
fond1 = pygame.image.load("img/fond3.jpg").convert()

# Import de l'image de fond du module Choix_Perso
fond2 = pygame.image.load("img/fond_choix.jpg").convert()

# Import des cadres pour le choix des personnages à jouer
cadre1 = pygame.image.load("img/cadre3.png").convert_alpha()
cadre2 = pygame.image.load("img/cadre3.png").convert_alpha()

# Import des image des perso sélectionnés
goku = pygame.image.load("img/goku.png").convert_alpha()
goku = pygame.transform.scale(goku, (131,215))

vegeta = pygame.image.load("img/vegeta.png").convert_alpha()
vegeta = pygame.transform.scale(vegeta, (131,215))

# Import des logo des personnages
gokubleu = pygame.image.load("img/gokuBleu.jpg").convert_alpha()
gokured = pygame.image.load("img/gokuRed.png").convert_alpha()

vegetableu = pygame.image.load("img/vegetableu.jpg").convert_alpha()
vegetared = pygame.image.load("img/vegetaRed.jpg").convert_alpha()

kimbleu = pygame.image.load("img/kimbleu.png").convert_alpha()
kimred = pygame.image.load("img/kimred.png").convert_alpha()

luffybleu = pygame.image.load("img/luffybleu.png").convert_alpha()
luffyred = pygame.image.load("img/luffyred.png").convert_alpha()
luffybleu = pygame.transform.scale(luffybleu, (100, 100))
luffyred = pygame.transform.scale(luffyred, (100, 100))
