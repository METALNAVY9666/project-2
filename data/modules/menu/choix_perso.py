""" Ce module permet aux utilisateurs de choisir les personnages avec
lesquelles ils veulent effectuer ca partie."""
from sys import exit
import pygame
from data.modules.menu.textures import (ok, itachibleu, itachired, luffybleu,
                                        luffyred, kimbleu, kimred, vegetableu,
                                        vegetared, gokubleu, gokured,
                                        goku_grand_r, vegeta_grand_r,
                                        kim_grand_r, luffy_grand_r,
                                        itachi_grand_r, goku_grand_b,
                                        vegeta_grand_b, kim_grand_b,
                                        luffy_grand_b, itachi_grand_b,
                                        fond2, cadre2)


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
    # Coordonnées des images des personnages
    coo_a = (67, 143)
    coo_b = (698, 143)

    posok = (3000, 3000)
    # Liste des coordonnées que peut prendre coo_a et coo_b
    list_pos = [([(67, 143), (205, 143), (343, 143), (481, 143)],
                 [(67, 312), (67, 312), (67, 312), (67, 312)]),
                 ([(698, 143), (838, 143), (979, 143), (1120, 143)],
                 [(698, 312), (698, 312), (698, 312), (698, 312)])]

    list_perso = [(["goku", "vegeta", "kim", "luffy"],
              ["itachi", "itachi", "itachi", "itachi"]),
              (["goku", "vegeta", "kim", "luffy"],
              ["itachi", "itachi", "itachi", "itachi"])]

    # Tableau des grandes images des personnages
    tab_grand_perso = [([goku_grand_r, vegeta_grand_r, kim_grand_r,
                        luffy_grand_r],
                        [itachi_grand_r, itachi_grand_r, itachi_grand_r,
                         itachi_grand_r]),

                         ([goku_grand_b, vegeta_grand_b, kim_grand_b,
                        luffy_grand_b],
                        [itachi_grand_b, itachi_grand_b, itachi_grand_b,
                         itachi_grand_b])]

    grand_perso1 = tab_grand_perso[0][0][0]
    grand_perso2 = tab_grand_perso[1][0][0]

    ind_i = 0
    ind_j = 0

    ind_x = 0
    ind_z = 0

    # On applique la surface de la console ainsi que sa couleur
    aff_surface.fill(color)

    # On ajoute l'image et on la place au coordonnée (0 ; 0)

    test = True
    while test:
        # Affichage des images
        aff_surface.blit(fond2, (0, 0))

        aff_surface.blit(cadre2, coo_a)
        aff_surface.blit(cadre2, coo_b)

        aff_surface.blit(gokured, (77, 154))
        aff_surface.blit(gokubleu, (708, 154))

        aff_surface.blit(vegetared, (215, 154))
        aff_surface.blit(vegetableu, (848, 154))

        aff_surface.blit(kimred, (353, 154))
        aff_surface.blit(kimbleu, (989, 154))

        aff_surface.blit(luffyred, (491, 154))
        aff_surface.blit(luffybleu, (1130, 154))

        aff_surface.blit(itachired, (77, 323))
        aff_surface.blit(itachibleu, (708, 323))

        aff_surface.blit(ok, posok)

        aff_surface.blit(grand_perso1, (255, 333))
        aff_surface.blit(grand_perso2, (888, 333))

        retour = Bouton.dessin()

        if retour:
            return "retour"
        # boucle permettant de détecter les touchent pressées :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:
                # Actions effectué si une touche est pressée
                if event.key == pygame.K_RIGHT:

                    ind_j += 1
                    if ind_j == 4:
                        ind_j = 4 - 1
                    coo_b = list_pos[1][ind_z][ind_j]
                    grand_perso2 = tab_grand_perso[1][ind_z][ind_j]

                if event.key == pygame.K_LEFT:
                    ind_j -= 1
                    if ind_j == -1:
                        ind_j = 0
                    coo_b = list_pos[1][ind_z][ind_j]
                    grand_perso2 = tab_grand_perso[1][ind_z][ind_j]

                if event.key == pygame.K_d:
                    ind_i += 1
                    if ind_i == 4:
                        ind_i = 4 - 1
                    coo_a = list_pos[0][ind_x][ind_i]
                    grand_perso1 = tab_grand_perso[0][ind_x][ind_i]

                if event.key == pygame.K_q:
                    ind_i -= 1
                    if ind_i == -1:
                        ind_i = 0
                    coo_a = list_pos[0][ind_x][ind_i]
                    grand_perso1 = tab_grand_perso[0][ind_x][ind_i]

                if event.key == pygame.K_SPACE:
                    if list_perso[0][ind_x][ind_i] != list_perso[1][ind_z][ind_j]:
                        posok = (200, 200)
                        return (list_perso[0][ind_x][ind_i], list_perso[1][ind_z][ind_j], "suivant")

                if event.key == pygame.K_DOWN:
                    ind_z = ind_z + 1
                    if ind_z == len(list_pos[1]):
                        ind_z = ind_z - 1
                    coo_b = list_pos[1][ind_z][ind_j]
                    grand_perso2 = tab_grand_perso[1][ind_z][ind_j]

                if event.key == pygame.K_s:
                    ind_x = ind_x + 1
                    if ind_x == len(list_pos[0]):
                        ind_x = ind_x - 1
                    coo_a = list_pos[0][ind_x][ind_i]
                    grand_perso1 = tab_grand_perso[0][ind_x][ind_i]

                if event.key == pygame.K_UP:
                    ind_z = ind_z - 1
                    if ind_z == -1:
                        ind_z = 0
                    coo_b = list_pos[1][ind_z][ind_j]
                    grand_perso2 = tab_grand_perso[1][ind_z][ind_j]

                if event.key == pygame.K_z:
                    ind_x = ind_x - 1
                    if ind_x == -1:
                        ind_x = 0
                    coo_a = list_pos[0][ind_x][ind_i]
                    grand_perso1 = tab_grand_perso[0][ind_x][ind_i]

            pygame.display.update()
