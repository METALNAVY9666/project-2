# Créé par Alexis, le 29/11/2022 en Python 3.7

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
                    return True
                    
        else:
            self.top_color = (255, 0, 0)

class carre1:
    """ Cette classe est un cadre qui se déplace en fonction du choix du personnage """
    def __init__(self, pos):
        """ Cette fonction permet de permet d'initialiser la classe """
        self.presse = False
        self.pos = pos
        self.i = 0

    
    def move_rect1(self, dir):
        """ Cette fonction permet de detecter le clic de certaine touche et exécuter certaines actions """
        
        aff_surface.blit(cadre2, self.pos)
        list_pos1 = [(67, 143), (205, 143)]
        # print(self.pos)
        
        if dir == 1:

            self.i -= 1
            if self.i == -1:
                self.i = 0
            self.pos = list_pos1[self.i]
            print(self.i)
        
        if dir == 2:
            
            self.i += 1
            if self.i == len(list_pos1):
                self.i = len(list_pos1) - 1
            self.pos = list_pos1[self.i]
            print(self.i)

        return self.i
        
                    
                

class carre2:
    """ Cette classe est un cadre qui se déplace en fonction du choix du personnage """
    def __init__(self, pos):
        """ Cette fonction permet de permet d'initialiser la classe """
        self.presse = False
        self.pos2 = pos
        self.j = 0


    def move_rect2(self):
        """ Cette fonction permet de detecter le clic de certaine touche et exécuter certaines actions """
        
        list_pos2 = [(698, 143), (838, 143)]
        dir = 2
        print(dir)
        
        
        if dir == 1:
            
            self.j -= 1
            if self.j == -1:
                self.j = 0
                
                            
        if dir == 2:
            
            self.j += 1
            if self.j == len(list_pos2):
                self.j = len(list_pos2) - 1
        
        return list_pos2[self.j]
            

        

class perso1:
    """ Cette classe permet d'aficher le personnage choisi. """
    posi1 = (50, 400)
    posi2 = (700, 400)


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

    xa = (67, 143)
    xb = (698, 143)

    # On applique la surface de la console ainsi que sa couleur
    aff_surface.fill(color)

    # On ajoute l'image et on la place au coordonnée (0 ; 0)

    dir = 1
    rect1 = carre1
    rect2 = carre2
    
    test = True
    while test:
        
        aff_surface.blit(fond2, (0, 0))
        aff_surface.blit(cadre2, xa)
        aff_surface.blit(cadre2, xb) 

        retour = Bouton.dessin()
        
        if retour:
            return "retour"
        # boucle permettant de détecter les touchent pressées : 
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    print("droit")
                    xb = (838, 143)
                    print(xa, xb)
                if event.key == pygame.K_LEFT:
                    print("gauche")
                    xb = (698, 143)
                if event.key == pygame.K_d:
                    print("d")
                    xa = (205, 143)
                if event.key == pygame.K_q:
                    print("q")
                    xa = (67, 143)
                if event.key == pygame.K_SPACE:
                    print("espace")

            pygame.display.update()



