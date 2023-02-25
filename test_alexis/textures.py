
""" Module qui est chargé d'importer les images qui serviront pour le module Menu et Choix_Perso """

import pygame

pygame.display.init()
surface = pygame.display.set_mode((1280, 720))

# Importation de l'image qui feras office de Menu du jeu
fond1 = pygame.image.load("img/fond3.jpg").convert()

# Import de l'image de fond du module Choix_Perso
fond2 = pygame.image.load("img/fond_choix.jpg").convert()

fond_map = pygame.image.load("img/fond2.jpg").convert()
fond_map = pygame.transform.scale(fond_map, (1280, 720))

# Import des cadres pour le choix des personnages à jouer
cadre1 = pygame.image.load("img/cadre3.png").convert_alpha()
cadre2 = pygame.image.load("img/cadre3.png").convert_alpha()
cadre3 = pygame.transform.scale(cadre1, (223,130))

# Import des image des perso sélectionnés
goku = pygame.image.load("img/goku.png").convert_alpha()
goku = pygame.transform.scale(goku, (131,215))

vegeta = pygame.image.load("img/vegeta.png").convert_alpha()
vegeta = pygame.transform.scale(vegeta, (131,215))

# Import des logo des personnages
gokubleu = pygame.image.load("img/gokuBleu.png").convert_alpha()
gokured = pygame.image.load("img/gokuRed.png").convert_alpha()

vegetableu = pygame.image.load("img/vegetableu.png").convert_alpha()
vegetared = pygame.image.load("img/vegetaRed.png").convert_alpha()

kimbleu = pygame.image.load("img/kimbleu.png").convert_alpha()
kimred = pygame.image.load("img/kimred.png").convert_alpha()

luffybleu = pygame.image.load("img/luffybleu.png").convert_alpha()
luffyred = pygame.image.load("img/luffyred.png").convert_alpha()



itachired = pygame.image.load("img/itachirouge.png").convert_alpha()
itachibleu = pygame.image.load("img/itachibleu.png").convert_alpha()

# Import des images des maps:

map1 = pygame.image.load("img/highway.png").convert_alpha()
map1bis = pygame.image.load("img/highway2.png").convert_alpha()

map2 = pygame.image.load("img/laboratory.png").convert_alpha()
map2bis = pygame.image.load("img/laboratory2.png").convert_alpha()

map3 = pygame.image.load("img/neo_tokyo.png").convert_alpha()
map3bis = pygame.image.load("img/neo_tokyo2.png").convert_alpha()

map4 = pygame.image.load("img/tenkaichi_budokai.png").convert_alpha()
map4bis = pygame.image.load("img/tenkaichi_budokai2.png").convert_alpha()

map1bis = pygame.transform.scale(map1bis, (800, 300))
map2bis = pygame.transform.scale(map2bis, (800, 300))
map3bis = pygame.transform.scale(map3bis, (800, 300))
map4bis = pygame.transform.scale(map4bis, (800, 300))

# Import du fond du choix des maps:

fond3 = pygame.image.load("img/fond_map.jpg").convert_alpha()
fond3 = pygame.transform.scale(fond3, (1280, 720))

titre = pygame.image.load("img/titre.png").convert_alpha()
titre = pygame.transform.scale(titre, (700, 80))

# Import image OK

ok = pygame.image.load("img/ok.png").convert_alpha()