""" Ce module permet à l'utilisateur de choisir la carte dans laquelle il veut
effectuer ca partie."""
import pygame
from data.modules.menu.textures import (titre, map4, map3, map2, map1, cadre3,
                                        fond3, map1bis, map2bis, map3bis,
                                        map4bis)


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
pygame.display.set_caption('Choix du perso')

police = pygame.font.Font(None, 30)

Bouton = BoutonQuit("QUITTER", 100, 50, (0, 670))


def main():
    """ Cette fonction créée une boucle d'affichage du menu pygame, et
        s'arrête lorsque l'utilisateur clique sur le bouton pour quitter
        le programme. """
    print("Entrée dans le menu choix")

    coo = (36, 126)

    list_pos1 = [(37, 126), (275, 126), (513, 126), (751, 126)]

    tabmap = [map1bis, map2bis, map3bis, map4bis]

    mapchoisi = ["highway", "laboratory", "neo_tokyo", "tenkaichi_budokai"]

    carte = tabmap[0]

    i = 0

    # On applique la surface de la console ainsi que sa couleur
    aff_surface.fill(color)

    # On ajoute l'image et on la place au coordonnée (0 ; 0)

    test = True
    while test:

        aff_surface.blit(fond3, (0, 0))

        aff_surface.blit(cadre3, coo)

        aff_surface.blit(map1, (47, 134))

        aff_surface.blit(map2, (287, 134))

        aff_surface.blit(map3, (526, 134))

        aff_surface.blit(map4, (764, 134))

        aff_surface.blit(titre, (280, 0))

        aff_surface.blit(carte, (240, 370))

        retour = Bouton.dessin()

        if retour:
            return "retour"
        # boucle permettant de détecter les touchent pressées :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_d:
                    print("d")
                    i += 1
                    if i == 4:
                        i = 4 - 1
                    coo = list_pos1[i]
                    carte = tabmap[i]

                if event.key == pygame.K_q:
                    print("q")
                    i -= 1
                    if i == -1:
                        i = 0
                    coo = list_pos1[i]
                    carte = tabmap[i]

                if event.key == pygame.K_SPACE:
                    print("espace")
                    print(mapchoisi[i])
                    return (mapchoisi[i], "fini")

            pygame.display.update()
