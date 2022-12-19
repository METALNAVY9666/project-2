'''Ce module permet de gérer le joueur, ses déplacements etc'''
import pygame as pg
from modules.texture_loader import persos
from modules.texture_loader import sprites_images


class Player(pg.sprite.Sprite):
    '''Cette classe permet de gérer les actions du joueur, ainsi que son apparence.'''

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = persos[self.game.name]
        self.rect = self.image.get_rect()
        self.coord = self.coordinates_list()
        self.propertie = self.coord[0]
        self.init_plus()
        self.strike = 10
        # Nombre de sauts max
        self.jumps = 1

    def init_plus(self):
        '''Cette fonction permet d'initialiser des élements
        suplémentaires.'''
        self.rect.x, self.rect.y = 900, 500
        self.sprite_x = 50
        # Temps entre chaque sprite de l'animation idle en ms
        self.idle_speed = 300
        # Somme des temps entres chaque frame
        self.delta_sum = 0
        # Bouléen pour savoir si le joueur fait rien ou pas
        self.pause = True
        # Images complémentaires
        self.images_dict = sprites_images(self.game.name)

    def move_right(self):
        '''Cette fonction gère les déplacements à droite.'''
        if self.rect.x <= 950:
            self.rect.x += 10
            # On change l'image du joueur
            self.change_animation('right')
            # Le joueur fait une action
            self.pause = False

    def move_left(self):
        '''Cette fonction gère les déplacements à gauche.'''
        if self.rect.x > 5:
            if not self.game.collision(self, self.game.all_objects):
                self.rect.x -= 10
                # On change l'image du joueur
                self.change_animation('left')
                # Change les coordonnées du perso
                self.pause = False

    def attack(self):
        '''Cette fonction permet de gérer l'attaque d'un perso.'''
        # Le joueur fait une action
        self.pause = False
        self.change_animation('attack')
        if not self.game.collision(self, self.game.all_objects):
            self.rect.x -= 1

    def jump(self):
        '''Fonction saut'''
        # Vérfie si le perso est inférieur à la hauteur de saut max
        if self.rect.y >= 300:
            # Vérifie si le perso n'a pas déjà sauté deux fois
            if self.jumps < 2:
                # Saute
                self.rect.y -= 25
            # Si le joueur a atteint la hauteur maximale, il redescend
            if self.rect.y <= 300:
                self.jumps = 3

    def gravity(self):
        '''Focntion qui simule une gravité'''
        # Le joueur tombe tant qu'il n'est pas au sol
        if self.rect.y <= 500 and not self.game.collision(self, self.game.all_objects):
            # fait tomber le perso et change l'image
            self.pause = False
            self.rect.y += 4
            self.change_animation('jump')
        # Sinon, on réinitialise son nombre de sauts à zéro
        elif self.rect.y >= 500:
            self.jumps = 0

    def change_animation(self, name):
        '''Fonction qui change l'image du personnage'''
        self.images_dict = sprites_images(self.game.name)
        self.image = self.images_dict[name]

    def blit_sprite(self, screen, dlt):
        '''Cette fonction sert à afficher le sprite du joueur en continu
        des coordonées demandes.'''
        if self.pause:
            screen.blit(self.image, (self.rect.x, self.rect.y),
                        (self.sprite_x * self.propertie[0],
                        self.propertie[1], self.propertie[2],
                        self.propertie[3]))
            self.delta_sum += dlt
            # si la somme des temps entre les frames est plus grande que 300ms
            if self.delta_sum >= self.idle_speed:
                # changer le sprite
                self.sprite_x += 1
                # remettre la somme des temps à 0
                self.delta_sum = 0
            if self.sprite_x > 2:
                self.sprite_x = 0
        else:
            # On affiche les actions que le joueur fait
            screen.blit(self.image, (self.rect))

    def coordinates_list(self):
        '''Coordonées du spritesheet'''
        self.tab = [[1, 2, 3, 4], [1, 3, 4, 5]]
        self.image = persos[self.game.name]
        if self.game.name == 'goku':
            self.tab = [[111, 0, 110, 130],
                        [111, 2, 1, 135],
                        [150, 2247, 139, 140]]
            if self.game.right:
                # Inverse le sens du spritesheet
                self.image = persos['goku_right']

        # Change le personnage en fonction du nom
        elif self.game.name == 'vegeta':
            self.tab = [[100, 0, 100, 120],
                        [1, 1970, 120, 105],
                        [150, 4400, 135, 140]]
            if self.game.right:
                self.image = persos['vegeta_right']
        # Renvoi le tableau des coordonnées
        return self.tab
