'''Ce module est le jeu, il gère les inputs, les collisions ainsi que
les différents événements dans le jeu.'''
import pygame as pg
from modules.player import Player
from modules.object import PunchingBall


class Jeu:
    '''Cette classe a pour but de lancer le jeu, l'arrêter, de gérer les collisions,
    les dessins, les dégats etc...'''

    def __init__(self, name):
        # On récupère le nom du perso choisi.
        self.name = name
        self.is_playing = False
        self.fps = 60
        self.right = False
        self.player = Player(self)
        # Crée des groupes de sprites vide
        self.all_players = pg.sprite.Group()
        self.all_objects = pg.sprite.Group()
        # Ajoute un joueur au groupe de sprite de tout les joueurs
        self.all_players.add(self.player)
        self.spawn_objects()

    def handle_input(self):
        '''Cette fonction a pour but de récupérer les touches préssées.
        En fonction de celles-ci, on effectue des opération spécifiques.'''
        choice = pg.key.get_pressed()
        # On réaffecte le tableau d'origine afinde reprendre les coordonnées de base
        self.player.coord = self.player.coordinates_list()
        self.player.propertie = self.player.coord[0]
        self.player.pause = True
        # Modifie les animations en fonction dde l'input
        if choice[pg.K_RIGHT]:
            self.player.move_right()
            self.right = True
        elif choice[pg.K_LEFT]:
            self.player.move_left()
            self.right = False
        elif choice[pg.K_q]:
            self.player.attack()
            self.strike_collision()

    def collision(self, sprite, group):
        '''Cette fonction renvoi un bouléen,
        qui est sur True quand il y a une collision entre
        un sprite et un groupe de sprites. Le cas échéant, le
        bouléen est sur False.'''
        # Vérifie si il y a collision ou non
        return pg.sprite.spritecollide(sprite, group,
                                       False, pg.sprite.collide_mask)

    def update(self, screen, dt):
        '''Cette fonction petrmet de mettre à jour le jeu.'''
        # screen.blit(self.player.image, self.player.rect)
        self.rect = self.player.blit_sprite(screen, dt)
        # Gère les inputs
        self.handle_input()
        # Renvoi le rectangle du joueur
        return self.rect

    def spawn_objects(self):
        '''Ajoute un objet punchingball au groupe de sprites d'objets.'''
        self.object = PunchingBall(self)
        self.all_objects.add(self.object)

    def update_objects(self, screen):
        '''Met à jour l'image del'objet'''
        self.punch = screen.blit(self.object.image,
                                 (self.object.x, self.object.y))
        return self.punch
    
    def strike_collision(self):
        '''Actionne l'attaque du personnage'''
        if self.collision(self.player, self.all_objects):
            print('geh')
            for objects in self.collision(self.player, self.all_objects):
                objects.damage()
                print(self.player.strike)
