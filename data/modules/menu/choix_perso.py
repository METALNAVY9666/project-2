# Créé par Alexis, le 29/11/2022 en Python 3.7

import pygame
from data.modules.menu.textures import *
from data.modules.menu.persos_choisis import *


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

    posok = (3000, 3000)

    list_pos1 = ([(67, 143), (205, 143), (343, 143), (481, 143)],
                 [(67, 312), (67, 312), (67, 312), (67, 312)])

    perso1 = (["goku", "vegeta", "kim", "luffy"],
              ["itachi", "itachi", "itachi", "itachi"])

    list_pos2 = ([(698, 143), (838, 143), (979, 143), (1120, 143)],
                 [(698, 312), (698, 312), (698, 312), (698, 312)])

    perso2 = (["goku", "vegeta", "kim", "luffy"],
              ["itachi", "itachi", "itachi", "itachi"])

    tab1_grand_perso = ([goku_grand_r, vegeta_grand_r, kim_grand_r,
                        luffy_grand_r],
                        [itachi_grand_r, itachi_grand_r, itachi_grand_r,
                         itachi_grand_r])

    tab2_grand_perso = ([goku_grand_b, vegeta_grand_b, kim_grand_b,
                        luffy_grand_b],
                        [itachi_grand_b, itachi_grand_b, itachi_grand_b,
                         itachi_grand_b])

    grand_perso1 = tab1_grand_perso[0][0]
    grand_perso2 = tab2_grand_perso[0][0]

    i = 0
    j = 0

    x = 0
    z = 0

    # On applique la surface de la console ainsi que sa couleur
    aff_surface.fill(color)

    # On ajoute l'image et on la place au coordonnée (0 ; 0)

    test = True
    while test:

        aff_surface.blit(fond2, (0, 0))

        aff_surface.blit(cadre2, xa)
        aff_surface.blit(cadre2, xb)

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

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RIGHT:
                    print("droit")
                    j += 1
                    if j == 4:
                        j = 4 - 1
                    xb = list_pos2[z][j]
                    grand_perso2 = tab2_grand_perso[z][j]

                if event.key == pygame.K_LEFT:
                    print("gauche")
                    j -= 1
                    if j == -1:
                        j = 0
                    xb = list_pos2[z][j]
                    grand_perso2 = tab2_grand_perso[z][j]

                if event.key == pygame.K_d:
                    print("d")
                    i += 1
                    if i == 4:
                        i = 4 - 1
                    xa = list_pos1[x][i]
                    grand_perso1 = tab1_grand_perso[x][i]

                if event.key == pygame.K_q:
                    print("q")
                    i -= 1
                    if i == -1:
                        i = 0
                    xa = list_pos1[x][i]
                    grand_perso1 = tab1_grand_perso[x][i]

                if event.key == pygame.K_SPACE:
                    print("espace")
                    if perso1[x][i] != perso2[z][j]:
                        print(perso1[x][i], perso2[z][j])
                        posok = (200, 200)
                        return (perso1[x][i], perso2[z][j], "suivant")

                if event.key == pygame.K_DOWN:
                    print("bas")
                    z = z + 1
                    if z == len(list_pos2):
                        z = z - 1
                    xb = list_pos2[z][j]
                    grand_perso2 = tab2_grand_perso[z][j]

                if event.key == pygame.K_s:
                    print("s")
                    x = x + 1
                    if x == len(list_pos1):
                        x = x - 1
                    xa = list_pos1[x][i]
                    grand_perso1 = tab1_grand_perso[x][i]

                if event.key == pygame.K_UP:
                    print("haut")
                    z = z - 1
                    if z == -1:
                        z = 0
                    xb = list_pos2[z][j]
                    grand_perso2 = tab2_grand_perso[z][j]

                if event.key == pygame.K_z:
                    print("z")
                    x = x - 1
                    if x == -1:
                        x = 0
                    xa = list_pos1[x][i]
                    grand_perso1 = tab1_grand_perso[x][i]

            pygame.display.update()
