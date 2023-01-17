'''Ce module gère le menu.'''
import pygame as pg
from modules.game import Jeu
from modules.texture_loader import images


class Menu:
    '''Cette classe permet de gérer lemenu, de là,
    on pourra choisir son personnage.'''

    def __init__(self):
        self.menu_dict = {'line': 0, 'column': 0,
                          'font': pg.font.Font('test_olivier/gfx/fonts/04B_19__.TTF', 20),
                          'image': images['square']
                          }
        self.rect = self.menu_dict['image'].get_rect()
        self.rect.x = 120
        self.rect.y = 70
        # Affecte un nom par défaut
        self.name = 'hello'
        self.liste_rect = []
        self.choosen = False

    def perso(self):
        '''Tableau qui renvoie les personnages, à modifier si inutile.'''
        tab = [['goku', 'vegeta', 'Prend pas', 'Prend pas'],
               ['Prend pas', 'Prend pas', 'Prend pas', 'Prend pas'],
               ['Prend pas', 'Prend pas', 'Prend pas', 'Prend pas']
               ]
        return tab

    def choice_perso(self, actions):
        '''Cette fonction permet de choisir le perso en fonction des lignes et des
        colonnes.'''
        for event in actions:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    tab = self.perso()
                    # Affecte le nom du joueur sélectionné
                    self.name = tab[self.menu_dict['column']
                                    ][self.menu_dict['line']]
                    self.choosen = True
        return self.name

    def choice_lines(self, event):
        '''Cette fonction permet de renvoyer le numéro de la ligne
        sur laquelle le joueur est.'''
        if event.key == pg.K_RIGHT and self.menu_dict['line'] < 3:
            self.menu_dict['line'] += 1
            self.rect.x += 110
        elif event.key == pg.K_LEFT and self.menu_dict['line'] >= 0:
            if self.menu_dict['line'] < 0:
                self.menu_dict['line'] = 0
            else:
                self.rect.x -= 110
                self.menu_dict['line'] -= 1
        return self.menu_dict['line']

    def choice_column(self, event):
        '''Cette fonction permet de renvoyer le numéro de la colonne
        sur laquelle le joueur est.'''
        if event.key == pg.K_DOWN and self.menu_dict['column'] < 2:
            self.rect.y += 100
            self.menu_dict['column'] += 1
            print(self.menu_dict['column'])
        elif event.key == pg.K_UP and self.menu_dict['column'] > 0:
            self.rect.y -= 100
            self.menu_dict['column'] -= 1
            print(self.menu_dict['column'])
        return self.menu_dict['column']

    def txt_blit(self, screen):
        '''Affiche les noms des persos que l'on peut choisir.'''
        tab = self.perso()
        txt = self.menu_dict['font'].render(
            tab[self.menu_dict['column']][self.menu_dict['line']], 0, (0, 0, 0))
        # Renvoi le rectangle du texte
        return screen.blit(txt, (self.rect))

    def menu_update(self, screen, actions):
        '''Cette fonction met à jour le menu.'''
        # Affiche les visages des personnages
        self.images_blit(screen)
        # Affiche le carré pour le menu et l'ajoute dans la liste de chose à updates
        self.liste_rect.append(screen.blit(
            self.menu_dict['image'], (self.rect)))
        self.liste_rect.append(self.txt_blit(screen))
        for event in actions:
            if event.type == pg.KEYDOWN:
                # Récupère le numéro de ligne et colonne
                self.menu_dict['line'] = self.choice_lines(event)
                self.menu_dict['column'] = self.choice_column(event)
                self.choice_perso(actions)
        return self.name

    def images_blit(self, screen):
        "Cette fonction permet d'afficher les visages des personnages."
        self.image_vegeta = images['vegeta_face']
        self.image_goku = images['goku_face']
        self.liste_rect.append(screen.blit(self.image_goku, (155, 105)))
        self.liste_rect.append(screen.blit(self.image_vegeta, (260, 105)))
