# Menu projet 2

""" Ce module est le menu de démarage du jeu. """

import pygame
import sys
from choix_perso import main as choix
from textures import * 

class Bouton:
    """ L'objet bouton permet de créer des boutons pour que le joueur
        puisse choisir ses choix du programme. """
    def __init__(self, text, large, haut, pos):
        """ Initialisation de l'objet bouton """
        # attribut de base
        self.presse = False   
        # création du rectangle suppérieur
        self.top_rect = pygame.Rect(pos, (large, haut))
        # Couleur de ce rectangle
        self.top_color = (117, 45, 254)
        # texte
        self.text_surf = police.render(text, True, (255, 255, 255))
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

    # Fonction qui va dessiner le rectangle suppérieur et le texte
    def dessin(self):
        """ Cette fonction permet de dessiner le bouton sur la fenetre
            pygame. """
        pygame.draw.rect(aff_surface, self.top_color, self.top_rect)
        aff_surface.blit(self.text_surf, self.text_rect)
        self.check_click()

    # Fonction qui va vérifier le click de la souri sur le bouton
    def check_click(self):
        """ Cette fonction permet de detecter le clic sur les boutons de
            l'utilisateur. """
        pos_souri = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(pos_souri):
            self.top_color = (14, 8, 195)
            if pygame.mouse.get_pressed()[0]:
                self.presse = True
            else:
                if self.presse is True:
                    # Bouton jouer
                    if pos_souri[1] < 335:
                        print("clik verifier pour jouer")
                        choix()
                    # Bouton règle du jeu
                    elif 340 < pos_souri[1] < 430:
                        pass
                    # Bouton Test perso
                    elif pos_souri[1] > 430:
                        pass

                self.presse = False
        else:
            self.top_color = (117, 45, 254)



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
        self.check_click()

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
                    pygame.display.quit()
                    sys.exit()
        else:
            self.top_color = (255, 0, 0)


class Bouton_credit:
    """ L'objet bouton permet de créer des boutons pour que le joueur
        puisse choisir ses choix du programme. """
    def __init__(self, text, large, haut, pos):
        """ Initialisation de l'objet bouton """
        # attribut de base
        self.presse = False
        # création du rectangle suppérieur
        self.top_rect = pygame.Rect(pos, (large, haut))
        # Couleur de ce rectangle
        self.top_color = (31, 151, 193)
        # texte
        self.text_surf = police.render(text, True, (255, 255, 255))
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

    # Fonction qui va dessiner le rectangle suppérieur et le texte
    def dessin(self):
        """ Cette fonction permet de dessiner le bouton sur la fenetre
            pygame. """
        pygame.draw.rect(aff_surface, self.top_color, self.top_rect)
        aff_surface.blit(self.text_surf, self.text_rect)
        self.check_click()

    # Fonction qui va vérifier le click de la souri sur le bouton
    def check_click(self):
        """ Cette fonction permet de detecter le clic sur les boutons de
            l'utilisateur. """
        pos_souri = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(pos_souri):
            self.top_color = (122, 193, 31)
            if pygame.mouse.get_pressed()[0]:
                self.presse = True
            else:
                if self.presse is True:
                    pass
        else:
            self.top_color = (31, 151, 193)


pygame.init()

# Couleur de la console
color = (0, 0, 0)

# Coordoné de la surface de la console
X = 1280
Y = 720

# On défini la surface de la console grâce aux coordonées
aff_surface = pygame.display.set_mode((X, Y))

# On nomme notre console
pygame.display.set_caption('Menu')

# Police graphique
police = pygame.font.Font(None, 30)

Bouton1 = Bouton("ENTRAINEMENT", 350, 70, (860, 430))

Bouton2 = Bouton("TUTORIEL", 350, 70, (860, 340))

Bouton3 = Bouton("JOUER", 350, 70, (860, 250))

Bouton4 = Bouton_quit("QUITTER", 100, 50, (1120, 50))

Bouton5 = Bouton_credit("CREDITS", 150, 50, (965, 600))


def main():
    """ Cette fonction créée une boucle d'affichage du menu pygame, et
        s'arrête lorsque l'utilisateur clique sur le bouton pour quitter
        le programme. """
    test = True
    while test:

        # On applique la surface de la console ainsi que sa couleur
        aff_surface.fill(color)

        # On ajoute l'image et on la place au coordonnée (0 ; 0)
        aff_surface.blit(fond1, (0, 0))

        # Dessin des Boutons
        Bouton1.dessin()

        Bouton2.dessin()

        Bouton3.dessin()

        Bouton4.dessin()

        Bouton5.dessin()

        if test is True:
            # boucle pour quitter ou pas la console du menu
            for event in pygame.event.get():
                pygame.display.update()
                if event.type == pygame.display.quit:

                    pygame.display.quit()

                    sys.exit()
                    
            
