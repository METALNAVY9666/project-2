""" Ce module permet à l'utilisateur de lire un tutoriel
    pour pouvoir avoir toutes les information pour jouer
    au jeu. """

import pygame
from data.modules.menu.textures import (tuto1, tuto2, tuto3, tuto4)


class BoutonQuit:
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
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

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
        return None


pygame.init()

# Couleur de la console
color = (0, 0, 0)

# Coordoné de la surface de la console
X = 1280
Y = 720

# On défini la surface de la console grâce aux coordonées
aff_surface = pygame.display.set_mode((X, Y))

# On nomme notre console
pygame.display.set_caption('Tutoriel')

police = pygame.font.Font(None, 30)

Bouton = BoutonQuit("QUITTER", 100, 50, (0, 670))


def main():
    """ Cette fonction créée une boucle d'affichage du tutoriel, et
        s'arrête lorsque l'utilisateur clique sur le bouton pour quitter
        le programme, et change les pages du tutoriel """

    tab_tuto = [tuto1, tuto2, tuto3, tuto4]

    tuto = tab_tuto[0]

    i = 0

    # On applique la surface de la console ainsi que sa couleur
    aff_surface.fill(color)

    # On ajoute l'image et on la place au coordonnée (0 ; 0)

    test = True
    while test:

        aff_surface.blit(tuto, (0, 0))

        retour = Bouton.dessin()

        if retour:
            return "retour"
        # boucle permettant de détecter les touchent pressées :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
            # Permet de changer les pages du tuto en appuyant sur des touches 
                if event.key == pygame.K_RIGHT:
                    print("d")
                    i += 1
                    if i == 4:
                        i = 0
                    tuto = tab_tuto[i]

                if event.key == pygame.K_LEFT:
                    print("q")
                    i -= 1
                    if i == -1:
                        i = 0
                    tuto = tab_tuto[i]

            pygame.display.update()
