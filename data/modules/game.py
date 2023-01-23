'''Ce module est le jeu, il gère les inputs, les collisions ainsi que
les différents événements dans le jeu.'''
import pygame as pg
from data.modules.fighter import Fighter
from data.modules.gunner import Gunner
from data.modules.thing import PunchingBall
from data.modules.texture_loader import GFX


class Jeu:
    '''Cette classe a pour but de lancer le jeu, l'arrêter, de gérer les collisions,
    les dessins, les dégats etc...'''

    def __init__(self, name, pkg, prop):
        # On récupère le nom du perso choisi.
        self.name = name
        self.dict_game = {'right': False, 'fps': 60,
                          'side': 'left', 'is_playing': True}
        # Génération de personnages
        self.player_0 = Fighter(self)
        self.player_1 = Gunner(pkg, prop)
        # Génération d'un objet
        self.object = PunchingBall(self)
        # Crée des groupes de sprites vide
        self.all_players = pg.sprite.Group()
        self.all_objects = pg.sprite.Group()
        # Ajout dans des groupes de sprites
        self.add_groups()

    def get_code(self, key):
        "renvoie la valeur de la touche"
        return pg.key.key_code(key)

    def handle_input(self, actions, pause, busy):
        '''Cette fonction a pour but de récupérer les touches préssées.
        En fonction de celles-ci, on effectue des opération spécifiques.
        La fonction get_pressed() récupère les touches préssées actuellement,
        et gère des actions en continu comme le fait d'avancer.'''
        
        if not pause and not busy:
            # Récupère les touches préssées actuellement
            choice = pg.key.get_pressed()
            self.player_0.stats_dict['pause'] = True
            # Réaffecte l'image de l'objet
            self.object.image = GFX['punchingball']
            # Modifie les animations en fonction de l'input
            if choice[self.get_code("d")]:
                self.player_0.move()
                self.dict_game['right'] = True
            elif choice[self.get_code("q")]:
                self.player_0.move()
                self.dict_game['right'] = False
                self.dict_game['side'] = 'left'
            elif choice[self.get_code("z")]:
                # Gère les sauts
                self.player_0.jump()
            elif choice[self.get_code("s")]:
                # Gère le bloquage
                self.player_0.block()
            # Système de gravité
            self.player_0.gravity()
            # Actions qui nécessitent une boucle 'for'
            self.loop_input(actions)

    def handle_input_controller(self, actions):
        """
        """
        choice = pg.key.get_pressed()
        # Réaffecte l'image de l'objet
        self.object.image = GFX['punchingball']
        # Modifie les animations en fonction de l'input
        for event in actions:
            self.player_0.move_controller(event)
            # Gère les sauts
            self.player_0.jump()
            """# Gère le bloquage
            self.player_0.block()"""
        # Système de gravité
        self.player_0.gravity()
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
                self.player_0.stats_dict['fall'] = True
                # Attaque du joueur
                self.player_0.attack(event, choice)
                # Esquive du joueur
                self.player_0.vanish(event)

    def collision(self, sprite, group):
        '''Cette fonction renvoi un bouléen,
        qui est sur True quand il y a une collision entre
        un sprite et un groupe de sprites. Le cas échéant, le
        bouléen est sur False.'''
        # Vérifie si il y a collision ou non
        return pg.sprite.spritecollide(sprite, group,
                                       False, pg.sprite.collide_mask)

    def update(self, screen, dlt, actions, pause, busy):
        '''Cette fonction permet de mettre à jour les événements
        du jeu.'''
        # Affiche le personnage sur l'écran
        rects = []
        rects.append(self.player_0.blit_sprite(screen, dlt, pause))
        rects.append(self.player_1.update())
        # Gère les inputs
        self.handle_input(actions, pause, busy)
        # Renvoi le rectangle du joueur
        self.update_health(screen, busy)
        #self.handle_input_controller(actions)
        # Dommages
        self.player_0.damages()
        return rects, self.player_0.update_pv()

    def add_groups(self):
        '''Ajoute un objet au groupe de sprites.'''
        # Ajout de l'objet dans le groue de sprite de tout les objets
        self.all_objects.add(self.object)
        # Ajoute un joueur au groupe de sprite de tout les joueurs
        self.all_players.add(self.player_0)

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
        if self.collision(self.player_0, self.all_objects):
            for objects in self.collision(self.player_0, self.all_objects):
                objects.damage()
                # Change l'animation en cas d'attaque
                self.object.image = GFX['hit']

    def update_health(self, surface, busy):
        '''Cette fonction dessine la barre de vie, d'énergie, et de défense du perso.
        Chaque barre possède une longueur propre au montant de sa variable respective.
        On dessine d'abord une barre grise, afin de faire le fond, puis on dessine celle
        avec de la couleur. Les deux, sur la surface donnée en paramètre.'''
        if not busy:
            # Dessin de la barre de vie
            pg.draw.rect(surface, (140, 138, 137), [
                        950, 50, self.player_0.stats_dict['max_health'], 15])
            pg.draw.rect(surface, (1, 88, 33), [
                        950, 50, self.player_0.stats_dict['health'], 15])
            # Barre de vie de l'objet
            pg.draw.rect(surface, (140, 138, 137), [
                        10, 50, self.object.stats['max_health'], 15])
            pg.draw.rect(surface, (1, 88, 33), [
                        10, 50, self.object.stats['health'], 15])
            # Nombre d'esquive possible
            pg.draw.rect(surface, (140, 138, 137), [950, 100, 4*30, 15])
            pg.draw.rect(surface, (255, 200, 133), [
                        950, 100, self.player_0.stats_dict['nbr_vanish']*30, 15])
