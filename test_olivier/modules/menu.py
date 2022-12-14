'''Ce module gère le menu.'''
import pygame as pg
from modules.game import Jeu
from modules.texture_loader import images


class Menu:
    '''Cette classe permet de gérer lemenu, de là,
    on pourra choisir son personnage.'''

    def __init__(self):
        self.image = images["square"]
        self.rect = self.image.get_rect()
        self.rect.x = 120
        self.rect.y = 70
        self.font = pg.font.Font('test_olivier/gfx/fonts/04B_19__.TTF', 20)
        # Affecte un nom par défaut
        self.name = 'hello'
        self.lines, self.column = 0, 0
        self.game = None
        self.liste_rect = []

    def perso(self):
        '''Tableau qui renvoie les personnages, à modifier si inutile.'''
        tab = [['goku', 'vegeta', 'Prend pas', 'Prend pas'],
               ['Prend pas', 'Prend pas', 'Prend pas', 'Prend pas'],
               ['Prend pas', 'Prend pas', 'Prend pas', 'Prend pas']
               ]
        return tab

    def choice_perso(self, EVENTS):
        '''Cette fonction permet de choisir le perso en fonction des lignes et des
        colonnes.'''
        for event in EVENTS:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    tab = self.perso()
                    print('Vous êtes sortis du menu.')
                    # Affecte le nom du joueur sélectionné
                    self.name = tab[self.column][self.lines]
        return self.name

    def choice_lines(self, event):
        '''Cette fonction permet de renvoyer le numéro de la ligne
        sur laquelle le joueur est.'''
        if event.key == pg.K_RIGHT and self.lines < 3:
            self.lines += 1
            self.rect.x += 110
        elif event.key == pg.K_LEFT and self.lines >= 0:
            if self.lines < 0:
                self.lines = 0
            else:
                self.rect.x -= 110
                self.lines -= 1
        return self.lines

    def choice_column(self, event):
        '''Cette fonction permet de renvoyer le numéro de la colonne
        sur laquelle le joueur est.'''
        if event.key == pg.K_DOWN and self.column < 2:
            self.rect.y += 100
            self.column += 1
            print(self.column)
        elif event.key == pg.K_UP and self.column > 0:
            self.rect.y -= 100
            self.column -= 1
            print(self.column)
        return self.column

    def txt_blit(self, screen):
        '''Affiche les noms des persos que l'on peut choisir.'''
        tab = self.perso()
        txt = self.font.render(tab[self.column][self.lines], 0, (0, 0, 0))
        # Renvoi le rectangle du texte
        return screen.blit(txt, (self.rect))

    def menu_update(self, screen, EVENTS):
        '''Cette fonction met à jour le menu.'''
        # Affiche le carré pour le menu et l'ajoute dans la liste de chose à updates
        self.liste_rect.append(screen.blit(self.image, (self.rect)))
        self.liste_rect.append(self.txt_blit(screen))
        for event in EVENTS:
            if event.type == pg.KEYDOWN:
                # Récupère le numéro de ligne et colonne
                self.lines = self.choice_lines(event)
                self.column = self.choice_column(event)
                self.choice_perso(EVENTS)
        # Si le joueur a choisi un perso, initialise Jeu et renvoie le nom
        if self.name != 'hello':
            self.game = Jeu(self.name)
        return self.name

    def launch_game(self):
        '''Cette fonction permet de lancer le jeu, à utiliser plus tard.'''
        self.game.is_playing = True
        print('tu vas rentrer dans le jeu,', self.game.name)
