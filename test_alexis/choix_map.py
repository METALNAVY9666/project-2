# Créé par Alexis, le 15/02/2023 en Python 3.7

import pygame
import sys
from textures import *
from persos_choisis import *
print("textures chargées")

class Bouton_quit:
    """ L'objet bouton permet de créer un bouton pour quitter le jeu. """
    def __init__(self, text, large, haut, pos):
        """ Initialisation de l'objet bouton """
        # attribut de base
        self.presse = False
        # création du rectangle suppérieur
        self.top_rect = pygame.Rect(pos, (large, haut))
        # Couleur de ce rectangle
        self.top_color = (255, 0, 0)
        # texte
        self.text_surf = police.render(text, True, (255, 255, 255))
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

    # Fonction qui va dessiner le rectangle suppérieur et le texte
    def dessin(self):
        """ Cette fonction permet de dessiner le bouton sur la fenetre
            pygame. """
        pygame.draw.rect(aff_surface, self.top_color, self.top_rect)
        aff_surface.blit(self.text_surf, self.text_rect)
        return self.check_click()

    # Fonction qui va vérifier le click de la souri sur le bouton
    def check_click(self):
        """ Cette fonction permet de detecter le clic sur les boutons de
            l'utilisateur. """
        pos_souri = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(pos_souri):
            self.top_color = (231, 189, 19)
            if pygame.mouse.get_pressed()[0]:
                self.presse = True
            else:
                if self.presse is True:
                    self.presse = False
                    return True
                    
        else:
            self.top_color = (255, 0, 0)
                    

pygame.init()

# Couleur de la console
color = (0, 0, 0)

# Coordoné de la surface de la console
X = 1280
Y = 720

# On défini la surface de la console grâce aux coordonées
aff_surface = pygame.display.set_mode((X, Y))

# On nomme notre console
pygame.display.set_caption('Choix du perso')

police = pygame.font.Font(None, 30)

Bouton = Bouton_quit("QUITTER", 100, 50, (0, 670))






def main():
    """ Cette fonction créée une boucle d'affichage du menu pygame, et
        s'arrête lorsque l'utilisateur clique sur le bouton pour quitter
        le programme. """
    print("Entrée dans le menu choix")
    
    y = 7687
    z = 6787

    xa = (37, 104)
    xb = (698, 143)
    
    list_pos1 = ([(37, 104), (275, 104), (513, 104), (751, 104)],
                 [(67, 312), (67, 312), (67, 312), (67, 312)])
    
    perso1 = (["goku", "vegeta", "kim", "luffy"],
                 ["itachi", "itachi", "itachi", "itachi"])
    
    
    i = 0
    j = 0  
    
    x = 0
    z = 0  
    
    # On applique la surface de la console ainsi que sa couleur
    aff_surface.fill(color)

    # On ajoute l'image et on la place au coordonnée (0 ; 0)

    test = True
    while test:
        
        aff_surface.blit(fond3, (0, 0))
        
        aff_surface.blit(cadre3, xa)
        
        aff_surface.blit(map1, (47, 114))
        
        aff_surface.blit(map2, (285, 114))
        
        aff_surface.blit(map3, (523, 114))
        
        aff_surface.blit(map4, (761, 114))
        
        aff_surface.blit(titre, (0, 0))
        


        retour = Bouton.dessin()
        
        if retour:
            return "retour"
        # boucle permettant de détecter les touchent pressées : 
        for event in pygame.event.get():
            
            if event.type == pygame.KEYDOWN:
                    
                if event.key == pygame.K_d:
                    print("d")
                    i += 1
                    if i == 4:
                        i = 4 - 1
                    xa = list_pos1[x][i]
                    
                if event.key == pygame.K_q:
                    print("q")
                    i -= 1
                    if i == -1:
                        i = 0
                    xa = list_pos1[x][i]
                    
                if event.key == pygame.K_SPACE:
                    print("espace")
                    pass
                    

                if event.key == pygame.K_s:
                    print("s")
                    x = x + 1
                    if x == len(list_pos1):
                        x = x - 1
                    xa = list_pos1[x][i]
                    
                    
                if event.key == pygame.K_z:
                    print("haut")
                    x = x - 1
                    if x == -1:
                        x = 0
                    xa = list_pos1[x][i]
                    

            pygame.display.update()



