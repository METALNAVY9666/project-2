'''Ce module est le jeu, il gère les inputs, les collisions ainsi que
les différents événements dans le jeu.'''
import pygame as pg
from modules.player import Player, manage_controller
from modules.object import PunchingBall
from modules.texture_loader import images


class Jeu:
    '''Cette classe a pour but de lancer le jeu, l'arrêter, de gérer les collisions,
    les dessins, les dégats etc...'''

    def __init__(self, name):
        # On récupère le nom du perso choisi.
        self.name = name
        self.dict_game = {'right': False, 'fps': 60,
                          'side': 'left', 'is_playing': True}
        self.rect = None
        # Génération d'un personnage
        self.player = Player(self)
        # Génération d'un objet
        self.object = PunchingBall(self)
        # Crée des groupes de sprites vide
        self.all_players = pg.sprite.Group()
        self.all_objects = pg.sprite.Group()
        # Ajout dans des groupes de sprites
        self.add_groups()

    def handle_input(self, actions):
        '''Cette fonction a pour but de récupérer les touches préssées.
        En fonction de celles-ci, on effectue des opération spécifiques.
        La fonction get_pressed() récupère les touches préssées actuellement,
        et gère des actions en continu comme le fait d'avancer.'''
        # Récupère les touches préssées actuellement
        choice = pg.key.get_pressed()
        self.player.stats_dict['pause'] = True
        # Réaffecte l'image de l'objet
        self.object.image = images['punchingball']
        # Modifie les animations en fonction de l'input
        if choice[pg.K_RIGHT]:
            self.player.move()
            self.dict_game['right'] = True
        elif choice[pg.K_LEFT]:
            self.player.move()
            self.dict_game['right'] = False
            self.dict_game['side'] = 'left'
        elif choice[pg.K_SPACE]:
            # Gère les sauts
            self.player.jump()
        elif choice[pg.K_s]:
            # Gère le bloquage
            self.player.block()
        elif choice[pg.K_ESCAPE]:
            self.dict_game['is_playing'] = False
        # Système de gravité
        self.player.gravity()
        # Actions qui nécessitent une boucle 'for'
        self.loop_input(actions)

    def handle_input_controller(self, actions):
        """
        """
        controller = manage_controller()
        # Réaffecte l'image de l'objet
        self.object.image = images['punchingball']
        # Modifie les animations en fonction de l'input
        for event in actions:
            if event.type == pg.JOYAXISMOTION and event.axis == 0:
                self.player.move_controller(event)
            # Gère les sauts
            if event.type == pg.JOYBUTTONDOWN and controller.get_button(0):
                self.player.jump_controller()
            # Gère le bloquage
            if event.type == pg.JOYBUTTONDOWN and controller.get_button(3):
                self.player.block()
        # Système de gravité
        self.player.gravity()
        # Actions qui nécessitent une boucle 'for'
        self.loop_input(actions)

    def loop_input(self, actions):
        '''Fonction qui gère les saisie de l'utilisateur avec une boucle for.
        Celle-ci gère les actions unique, par exemple, une attaque qui ne doit pas être lancée
        en continu. Ces actions se déclenchent uniquement quand le joueur appuie sur une touche,
        et non quand il la maintient.'''
        choice = pg.key.get_pressed()
        for event in actions:
            # On vérifie si le joueur appuie sur une touche
            if event.type == pg.KEYDOWN:
                # Le perso tombe
                self.player.stats_dict['fall'] = True
                # Attaque du joueur
                self.player.attack(event, choice)
                # Esquive du joueur
                self.player.vanish(event)
            if event.type == pg.JOYBUTTONDOWN:
                self.player.attack_controller(choice)

    def collision(self, sprite, group):
        '''Cette fonction renvoi un bouléen,
        qui est sur True quand il y a une collision entre
        un sprite et un groupe de sprites. Le cas échéant, le
        bouléen est sur False.'''
        # Vérifie si il y a collision ou non
        return pg.sprite.spritecollide(sprite, group,
                                       False, pg.sprite.collide_mask)

    def update(self, screen, dlt, actions):
        '''Cette fonction permet de mettre à jour les événements
        du jeu.'''
        # Affiche le personnage sur l'écran
        self.rect = self.player.blit_sprite(screen, dlt)
        # Gère les inputs
        self.handle_input(actions)
        # Renvoi le rectangle du joueur
        self.update_health(screen)
        self.handle_input_controller(actions)
        # Dommages
        self.player.damages()
        # Affiche les pv
        print(self.player.update_pv())
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
        # Gravité de l'objet
        self.object.gravity_object()
        # Met le punching ball à jour
        return screen.blit(self.object.image, (self.object.rect))

    def strike_collision(self):
        '''Actionne l'attaque du personnage'''
        if self.collision(self.player, self.all_objects):
            for objects in self.collision(self.player, self.all_objects):
                objects.damage()
                # Change l'animation en cas d'attaque
                self.object.image = images['hit']

    def update_health(self, surface):
        '''Cette fonction dessine la barre de vie, d'énergie, et de défense du perso.
        Chaque barre possède une longueur propre au montant de sa variable respective.
        On dessine d'abord une barre grise, afin de faire le fond, puis on dessine celle
        avec de la couleur. Les deux, sur la surface donnée en paramètre.'''
        # Dessin de la barre de vie
        pg.draw.rect(surface, (140, 138, 137), [
                     950, 50, self.player.stats_dict['max_health'], 15])
        pg.draw.rect(surface, (1, 88, 33), [
                     950, 50, self.player.stats_dict['health'], 15])
        # Barre de vie de l'objet
        pg.draw.rect(surface, (140, 138, 137), [
                     10, 50, self.object.stats['max_health'], 15])
        pg.draw.rect(surface, (1, 88, 33), [
                     10, 50, self.object.stats['health'], 15])
        # Nombre d'esquive possible
        pg.draw.rect(surface, (140, 138, 137), [950, 100, 4*30, 15])
        pg.draw.rect(surface, (255, 200, 133), [
                     950, 100, self.player.stats_dict['nbr_vanish']*30, 15])
