
""" Module qui est chargé d'importer les images qui serviront pour le module
    Menu et Choix_Perso """

import pygame

pygame.display.init()
surface = pygame.display.set_mode((1280, 720))

IMG_PATH = "data/modules/menu/img/"

# Importation de l'image qui feras office de Menu du jeu
fond1 = pygame.image.load(IMG_PATH + "/fond3.jpg").convert()

# Import de l'image de fond du module Choix_Perso
fond2 = pygame.image.load(IMG_PATH + "/fond_choix.jpg").convert()

fond_map = pygame.image.load(IMG_PATH + "/fond2.jpg").convert()
fond_map = pygame.transform.scale(fond_map, (1280, 720))

# Import des cadres pour le choix des personnages à jouer
cadre1 = pygame.image.load(IMG_PATH + "/cadre3.png").convert_alpha()
cadre2 = pygame.image.load(IMG_PATH + "/cadre3.png").convert_alpha()
cadre3 = pygame.transform.scale(cadre1, (223, 130))

# Import des image des perso sélectionnés
goku = pygame.image.load(IMG_PATH + "/goku.png").convert_alpha()
goku = pygame.transform.scale(goku, (131, 215))

vegeta = pygame.image.load(IMG_PATH + "/vegeta.png").convert_alpha()
vegeta = pygame.transform.scale(vegeta, (131, 215))

# Import des logo des personnages
gokubleu = pygame.image.load(IMG_PATH + "/gokuBleu.png").convert_alpha()
gokured = pygame.image.load(IMG_PATH + "/gokuRed.png").convert_alpha()

vegetableu = pygame.image.load(IMG_PATH + "/vegetableu.png").convert_alpha()
vegetared = pygame.image.load(IMG_PATH + "/vegetaRed.png").convert_alpha()

kimbleu = pygame.image.load(IMG_PATH + "/kimbleu.png").convert_alpha()
kimred = pygame.image.load(IMG_PATH + "/kimred.png").convert_alpha()

luffybleu = pygame.image.load(IMG_PATH + "/luffybleu.png").convert_alpha()
luffyred = pygame.image.load(IMG_PATH + "/luffyred.png").convert_alpha()


itachired = pygame.image.load(IMG_PATH + "/itachirouge.png").convert_alpha()
itachibleu = pygame.image.load(IMG_PATH + "/itachibleu.png").convert_alpha()

# Import des images des maps:

map1 = pygame.image.load(IMG_PATH + "/highway.png").convert_alpha()
map1bis = pygame.image.load(IMG_PATH + "/highway2.png").convert_alpha()

map2 = pygame.image.load(IMG_PATH + "/laboratory.png").convert_alpha()
map2bis = pygame.image.load(IMG_PATH + "/laboratory2.png").convert_alpha()

map3 = pygame.image.load(IMG_PATH + "/neo_tokyo.png").convert_alpha()
map3bis = pygame.image.load(IMG_PATH + "/neo_tokyo2.png").convert_alpha()

map4 = pygame.image.load(IMG_PATH + "/tenkaichi_budokai.png").convert_alpha()
map4bis = pygame.image.load(
    IMG_PATH + "/tenkaichi_budokai2.png").convert_alpha()

map1bis = pygame.transform.scale(map1bis, (800, 300))
map2bis = pygame.transform.scale(map2bis, (800, 300))
map3bis = pygame.transform.scale(map3bis, (800, 300))
map4bis = pygame.transform.scale(map4bis, (800, 300))

# Import du fond du choix des maps:

fond3 = pygame.image.load(IMG_PATH + "/fond_map.jpg").convert_alpha()
fond3 = pygame.transform.scale(fond3, (1280, 720))

titre = pygame.image.load(IMG_PATH + "/titre.png").convert_alpha()
titre = pygame.transform.scale(titre, (700, 80))

# Import image OK

ok = pygame.image.load(IMG_PATH + "/ok.png").convert_alpha()

# Import des grandes images des personnages

goku_grand_r = pygame.image.load(IMG_PATH + "/goku_grand.png").convert_alpha()
goku_grand_b = pygame.image.load(
    IMG_PATH + "/goku_grand_b.png").convert_alpha()

vegeta_grand_r = pygame.image.load(
    IMG_PATH + "/vegeta_grand.png").convert_alpha()
vegeta_grand_b = pygame.image.load(
    IMG_PATH + "/vegeta_grand_b.png").convert_alpha()

kim_grand_r = pygame.image.load(IMG_PATH + "/kim_grand.png").convert_alpha()
kim_grand_b = pygame.image.load(IMG_PATH + "/kim_grand_b.png").convert_alpha()

luffy_grand_r = pygame.image.load(
    IMG_PATH + "/luffy_grand.png").convert_alpha()
luffy_grand_b = pygame.image.load(
    IMG_PATH + "/luffy_grand_b.png").convert_alpha()

itachi_grand_r = pygame.image.load(
    IMG_PATH + "/itachi_grand.png").convert_alpha()
itachi_grand_b = pygame.image.load(
    IMG_PATH + "/itachi_grand_b.png").convert_alpha()

# Import des images du tutoriel

tuto1 = pygame.image.load(IMG_PATH + "/tuto1.png").convert_alpha()
tuto2 = pygame.image.load(IMG_PATH + "/tuto2.png").convert_alpha()
tuto3 = pygame.image.load(IMG_PATH + "/tuto3.png").convert_alpha()
tuto4 = pygame.image.load(IMG_PATH + "/tuto4.png").convert_alpha()