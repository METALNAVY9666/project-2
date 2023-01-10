
""" Module qui est chargé d'importer les images qui serviront pour le module Menu et Choix_Perso """

import pygame

pygame.display.init()
surface = pygame.display.set_mode((1280, 720))

# Importation de l'image qui feras office de Menu du jeu
fond1 = pygame.image.load("img/fond3.jpg").convert()

# Import de l'image de fond du module Choix_Perso
fond2 = pygame.image.load("img/fond_choix2.jpg").convert()

# Import des cadres pour le choix des personnages à jouer
cadre1 = pygame.image.load("img/cadre3.png").convert_alpha()
cadre2 = pygame.image.load("img/cadre3.png").convert_alpha()

# Import des image des perso sélectionnés
goku = pygame.image.load("img/goku.png").convert_alpha()
goku = pygame.transform.scale(goku, (131,215))

vegeta = pygame.image.load("img/vegeta.png").convert_alpha()
vegeta = pygame.transform.scale(vegeta, (131,215))

