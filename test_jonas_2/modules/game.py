'''Ce module est le jeu, il gère les inputs, les collisions ainsi que
les différents événements dans le jeu.'''
import pygame as pg
from pygame.locals import *
from modules.player import Player
from modules.object import PunchingBall
from modules.texture_loader import images


class Jeu:
    '''Cette classe a pour but de lancer le jeu, l'arrêter, de gérer les collisions,
    les dessins, les dégats etc...'''
    pg.joystick.init() #initialise le module joystick
    joysticks = [pg.joystick.Joystick(i) for i in range(pg.joystick.get_count())]
    #Permet de savoir le nombre de manettes utilisés
    for joystick in joysticks:
        print(joystick.get_name()) #Permet de connaitre la manette utilisée.

    def __init__(self, name):
        # On récupère le nom du perso choisi.
        self.name = name
        self.is_playing = False
        self.right = False
        self.fps = 60
        # Génération d'un personnage
        self.player = Player(self)
        # Génération d'un objet
        self.object = PunchingBall(self)
        # Crée des groupes de sprites vide
        self.all_players = pg.sprite.Group()
        self.all_objects = pg.sprite.Group()
        # Ajout dans des groupes de sprites
        self.add_groups()

    def handle_input_2(self, ):
        for event in pg.event.get():
            print(event)
            self.player.pause = True
            self.object.image = images['punchingball']
            if event.type == JOYBUTTONDOWN :
                

                if event.button == 0:
                    self.player.jump()
            if event.type == JOYAXISMOTION:
                if event.axis == 0:
                    self.player.motion[0]

    def handle_input(self):
        '''Cette fonction a pour but de récupérer les touches préssées.
        En fonction de celles-ci, on effectue des opération spécifiques.'''
        # Récupère les touches préssées actuellement
        choice = pg.key.get_pressed()
        self.player.pause = True
        # Réaffecte l'image de l'objet
        self.object.image = images['punchingball']
        # Modifie les animations en fonction de l'input
        if choice[pg.K_RIGHT]:
            self.player.move_right()
            self.right = True
        elif choice[pg.K_LEFT]:
            self.player.move_left()
            self.right = False
        elif choice[pg.K_q]:
            self.player.attack()
            # Gère les collisions du personnage
            self.strike_collision()
        elif choice[pg.K_SPACE]:
            # Gère les sauts
            self.player.jump()
        # Système de gravité
        self.player.gravity()
            

    def collision(self, sprite, group):
        '''Cette fonction renvoi un bouléen,
        qui est sur True quand il y a une collision entre
        un sprite et un groupe de sprites. Le cas échéant, le
        bouléen est sur False.'''
        # Vérifie si il y a collision ou non
        return pg.sprite.spritecollide(sprite, group,
                                       False, pg.sprite.collide_mask)

    def update(self, screen, dlt):
        '''Cette fonction petrmet de mettre à jour les événements
        du jeu.'''
        # Affiche le personnage sur l'écran
        self.rect = self.player.blit_sprite(screen, dlt)
        # Gère les inputs
        self.handle_input()
        self.handle_input_2()
        # Renvoi le rectangle du joueur
        return self.rect

    def add_groups(self):
        '''Ajoute un objet au groupe de sprites.'''
        # Ajout de l'objet dans le groue de sprite de tout les objets
        self.all_objects.add(self.object)
        # Ajoute un joueur au groupe de sprite de tout les joueurs
        self.all_players.add(self.player)

    def update_objects(self, screen):
        '''Met à jour l'image del'objet'''
        # Fait bouger le punching ball
        self.object.forward()
        # Met le punching ball à jour
        return screen.blit(self.object.image, (self.object.rect))

    def strike_collision(self):
        '''Actionne l'attaque du personnage'''
        if self.collision(self.player, self.all_objects):
            for objects in self.collision(self.player, self.all_objects):
                objects.damage()
                self.object.image = images['hit']
