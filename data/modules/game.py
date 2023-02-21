'''Ce module est le jeu, il gère les inputs, les collisions ainsi que
les différents événements dans le jeu.'''
import pygame as pg
from data.modules.fighter import Fighter
from data.modules.gunner import Gunner
from data.modules.thing import PunchingBall
from data.modules.texture_loader import GFX
from data.modules.spe import Special
from data.modules.controllers import manage_controller, manage_joysticks
from pygame._sdl2.controller import Controller
from pygame.locals import *
pg._sdl2.controller.init()
pg.init()


class Jeu:
    '''Cette classe a pour but de lancer le jeu, l'arrêter, de gérer les
    collisions, les dessins, les dégats etc...'''

    def __init__(self, name, pkg, prop):
        # On récupère le nom du perso choisi.
        self.name = name
        self.elms = {'right': False, 'fps': 60,
                     'side': 'left', 'is_playing': True,
                     'pkg': pkg, 'prop': prop}
        # Génération de personnages
        self.player_0 = Fighter(self, pkg, prop, 0)
        self.player_1 = Gunner(pkg, prop, 1)
        self.player_2 = Fighter(self, pkg, prop, 2)
        self.ulti = Special(self)
        # Génération d'un objet
        self.object = PunchingBall(self)
        # Crée des groupes de sprites vide
        self.all_players = pg.sprite.Group()
        self.all_objects = pg.sprite.Group()
        self.all_players_2 = pg.sprite.Group()
        # Ajout dans des groupes de sprites
        self.add_groups()

    def get_code(self, key):
        "renvoie la valeur de la touche"
        return pg.key.key_code(key)

    def handle_input(self, actions, pause, busy, screen):
        '''Cette fonction a pour but de récupérer les touches préssées.
        En fonction de celles-ci, on effectue des opération spécifiques.
        La fonction get_pressed() récupère les touches préssées actuellement,
        et gère des actions en continu comme le fait d'avancer.'''
        if not pause and not busy:
            # Récupère les touches préssées actuellement
            choice = pg.key.get_pressed()
            self.player_0.vals['pause'] = True
            # Réaffecte l'image de l'objet
            self.object.image = GFX['punchingball']
            # Modifie les animations en fonction de l'input
            if choice[self.get_code("d")]:
                self.player_0.jump(choice)
                self.player_0.move()
                self.elms['right'] = True
            elif choice[self.get_code("q")]:
                self.player_0.jump(choice)
                self.player_0.move()
                self.elms['right'] = False
                if self.name in ['goku', 'vegeta']:
                    self.elms['side'] = 'left'
            # Gère les sauts
            self.player_0.jump(choice)
            # Gère le bloquage
            self.player_0.block(choice)
            self.ulti.spe_manager(screen, choice)
            # Système de gravité
            self.player_0.charge(choice)
            # Actions qui nécessitent une boucle 'for'
            self.loop_input(actions)

    def handle_input_controller(self, actions):
        """
        Cette fonction récupère les actions effectuées à la manette et
        effectue des opérations spécifiques correspondantes. La fonction
        get.button(n) avec n un nombre entier permet de savoir si la touche
        correspondante au nombre n est pressé
        """
        contro = manage_controller()
        joy = manage_joysticks()
        # Réaffecte l'image de l'objet
        self.object.image = GFX['punchingball']
        # Modifie les animations en fonction de l'input
        if joy[0].get_id() == 0:
            # Gère le blocage
            if (contro.get_button(3) and
                    self.player_0.vals['current_height'] == 0):
                self.player_0.block()

            # Gère les mouvements à la manette
            elif (contro.get_axis(0) / 3500 > 5
                  or contro.get_axis(0) / 3500 < - 5):
                if contro.get_axis(0) < 0:
                    self.elms['right'] = False
                else:
                    self.elms['right'] = True
                self.player_0.move_controller(contro.get_axis(0))

            # Gère les sauts
            if (contro.get_button(0) and
                    self.player_0.vals['current_height'] < 400):
                self.player_0.jump_controller(8)

            # Gère les attaques
            for event in actions:
                if self.player_0.vals['current_height'] > 40 and (
                        event.type == JOYBUTTONDOWN and event.button == 1):
                    self.player_0.dash_attack_up_controller()

                elif (contro.get_axis(1) / 3500 > 5 and
                      event.type == JOYBUTTONDOWN and event.button == 1):
                    print('sol')
                    self.player_0.attack_down_controller()

                elif event.type == JOYBUTTONDOWN and event.button == 1:
                    self.player_0.attack_controller(contro.get_button(1))

                elif event.type == JOYBUTTONDOWN and event.button == 2:
                    self.player_0.attack_controller(contro.get_button(2))

            if contro.get_button(10):
                self.player_0.vanish_controller()

    def loop_input(self, actions):
        '''Fonction qui gère les saisie de l'utilisateur avec une boucle for.
        Celle-ci gère les actions unique, par exemple, une attaque qui ne doit
        pas être lancée en continu. Elles se déclenchent uniquement quand
        le joueur appuie sur une touche, et non quand il la maintient.'''
        choice = pg.key.get_pressed()
        for event in actions:
            # On vérifie si le joueur appuie sur une touche
            if event.type == pg.KEYDOWN:
                # Le perso tombe
                self.player_0.vals['fall'] = True
                # Attaque du joueur
                self.player_0.attack(event, choice)
                self.player_0.move_manager(event)
                # Esquive du joueur
                self.player_0.vanish(event)
                # dash attack
                self.player_0.dash_attack_up(choice, event)
                self.player_0.is_dashing(choice, event)
            if event.type == pg.KEYUP and self.elms['side'] == 'run':
                self.player_0.vals['nbr_sprite'] = 5

    def collision(self, sprite, group):
        '''Cette fonction renvoi un bouléen,
        qui est sur True quand il y a une collision entre
        un sprite et un groupe de sprites. Le cas échéant, le
        bouléen est sur False.'''
        # Vérifie si il y a collision ou non
        return pg.sprite.spritecollide(sprite, group,
                                       False, pg.sprite.collide_mask)

    def add_groups(self):
        '''Ajoute un objet au groupe de sprites.'''
        # Ajout de l'objet dans le groue de sprite de tout les objets
        self.all_objects.add(self.object)
        # Ajoute un joueur au groupe de sprite de tout les joueurs
        self.all_players.add(self.player_0)
        self.all_players_1.add(self.player_2)

    def strike_collision(self):
        '''Actionne l'attaque du personnage'''
        if self.collision(self.player_0, self.all_objects):
            for objects in self.collision(self.player_0, self.all_objects):
                objects.damage()
                # Change l'animation en cas d'attaque
                self.object.image = GFX['hit']

    def update_stats(self):
        """
        Met à jour les caractéristiques spéciale comme les barres,
        les attaques spéciales, et les stats.
        """
        if self.name == "luffy" and self.player_0.vals["percent_ult"] <= 130:
            self.player_0.vals["percent_ult"] += 0.1
        elif self.name == 'gear4' and self.player_0.vals["percent_ult"] > 0:
            self.player_0.vals["percent_ult"] -= 0.1
        elif self.name == 'gear4' and self.player_0.vals["percent_ult"] <= 0:
            self.name = 'luffy'

    def update_objects(self, screen):
        '''Met à jour l'image del'objet'''
        self.object.forward()
        self.object.gravity_object()
        # Met le punching ball à jour
        return screen.blit(self.object.image, (self.object.rect))

    def update_health(self, surface, busy):
        '''Cette fonction dessine la barre de vie, d'énergie, et de défense du
        perso.Chaque barre possède une longueur propre au montant de sa
        variable respective. On dessine d'abord une barre grise, afin de faire
        le fond, puis on dessine celleavec de la couleur. Les deux, sur la
        surface donnée en paramètre.'''
        width = self.elms["pkg"]["surface"].get_width()
        height = self.elms["pkg"]["surface"].get_height()
        if not busy:
            # Dessin de la barre de vie
            pg.draw.rect(surface, (25, 70, 17), [
                width - 400, height // 15,
                self.player_0.vals['max_health'], 15])
            pg.draw.rect(surface, (75, 198, 9), [
                width - 400, height // 15, self.player_0.vals['health'], 15])
            # Barre de vie de l'objet
            pg.draw.rect(surface, (140, 138, 137), [
                width // 8, height // 15, self.object.stats['max_health'], 15])
            pg.draw.rect(surface, (1, 88, 33), [
                width // 8, height // 15, self.object.stats['health'], 15])
            # Nombre d'esquive possible
            pg.draw.rect(surface, (0, 91, 136), [
                         width - 400, height // 10, 4 * 30, 15])
            pg.draw.rect(surface, (159, 212, 239), [
                width - 400, height // 10,
                self.player_0.vals['nbr_vanish'] * 30, 15])
            # Jauge de spé
            if self.name in ['luffy', 'gear4', 'goku', 'revive']:
                pg.draw.rect(surface, (64, 2, 97), [
                             width - 400, height // 7, 130, 15])
                pg.draw.rect(surface, (168, 30, 241), [
                             width - 400, height // 7,
                             self.player_0.vals['percent_ult'], 15])

    def update_header(self, screen, busy):
        """
        Fonction qui met à jour les élements du haut de l'écran
        """
        self.rect_update = []
        if not busy:
            # Boite de stats
            self.box = {"image": GFX['stats_box']}
            self.box['rect'] = self.box["image"].get_rect()
            self.box["rect"].x = screen.get_width() - 450
            self.rect_update.append(screen.blit(
                self.box["image"], (self.box["rect"])))
            # Visage
            self.face = {"image": GFX[self.name]}
            self.face["rect"] = self.face["image"].get_rect()
            self.face["rect"].x = screen.get_width() - 150
            self.face["rect"].y = screen.get_height() // 20
            self.rect_update.append(screen.blit(
                self.face["image"], (self.face["rect"])))
            self.rect_update.append(screen.blit(
                self.box["image"],
                (screen.get_width() // 60, 0)))
        return self.rect_update

    def update_player_0(self, screen):
        """Mis à jour du perso 0"""
        self.player_0.gravity()
        self.player_0.damages()
        self.update_stats()
        self.player_0.dash()
        self.player_0.combo()
        self.ulti.spe_goku(screen)

    def update_player_2(self, screen):
        """Mise à jour du perso 1"""
        self.player_2.gravity()
        self.player_2.damages()
        self.update_stats()
        self.player_2.dash()
        self.player_2.combo()
        self.ulti.spe_goku(screen)

    def update(self, screen, dlt, actions, pause, busy):
        '''Cette fonction permet de mettre à jour les événements
        du jeu.'''
        # Affiche le personnage sur l'écran
        rects = []
        rects.append(self.player_0.blit_sprite(screen, dlt, pause))
        rects.append(self.player_1.update(dlt, pause, busy))
        #rects.append(self.player_2.blit_sprite(screen, dlt, pause))
        for element in self.update_header(screen, busy):
            rects.append(element)
        # Gère les inputs
        self.handle_input(actions, pause, busy, screen)
        # Gère les inputs à la manette
        # Si il y a au moins une manette de connecté:
        if manage_controller() != None:
            self.handle_input_controller(actions)
        # Renvoi le rectangle du joueur
        self.update_health(screen, busy)
        # self.handle_input_controller(actions)
        self.update_player_0(screen)
        self.update_player_2(screen)
        return rects, self.player_0.update_pv()
