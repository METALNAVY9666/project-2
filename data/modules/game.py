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
        self.elms = {'right': [False, True, True], 'fps': 60,
                     'side': ["left", "left", "left"], 'is_playing': True,
                     'pkg': pkg, 'prop': prop}
        # Génération de personnages
        self.player_0 = Fighter(self, pkg, prop, 0)
        self.player_1 = Gunner(pkg, prop, 1)
        self.player_2 = Fighter(self, pkg, prop, 2)
        self.players = [self.player_0, self.player_2]
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
            self.player_0.vals["attacked"] = False
            if choice[self.get_code("d")]:
                if choice[self.get_code("z")]:
                    self.player_0.jump()
                self.player_0.move()
                self.elms['right'][self.player_0.number] = True
            elif choice[self.get_code("q")]:
                if choice[self.get_code("z")]:
                    self.player_0.jump()
                self.player_0.move()
                self.elms['right'][self.player_0.number] = False
                if self.name in ['goku', 'vegeta']:
                    self.elms["side"][self.player_0.number] = 'left'
            # Gère les sauts
            elif choice[self.get_code("z")]:
                self.player_0.jump()
            # Gère le bloquage
            elif choice[self.get_code("s")]:
                self.player_0.block()
            if choice[self.get_code("z")] and choice[self.get_code("s")]:
                self.player_0.charge()
            self.ulti.spe_manager(screen, choice)
            # Actions qui nécessitent une boucle 'for'
            self.loop_input(actions)
            self.handle_input_player2(choice)

    def handle_input_player2(self, choice):
        """Saisie clavier pour le perso 2"""
        self.player_2.vals["pause"] = True
        # print(self.elms['right'][self.player_0.number])
        if choice[self.get_code("right")]:
            self.elms['right'][self.player_2.number] = True
            self.player_2.move()
            if choice[self.get_code("up")]:
                self.player_2.jump()
        elif choice[self.get_code("left")]:
            self.elms['right'][self.player_2.number] = False
            self.player_2.move()
            if choice[self.get_code("up")]:
                self.player_2.jump()
        elif choice[self.get_code("up")]:
            self.player_2.jump()
        elif choice[self.get_code("down")]:
            self.player_2.block()
        if choice[self.get_code("down")] and choice[self.get_code("up")]:
            self.player_2.charge()

    def handle_input_controller(self, actions, pause, busy, contro):
        """
        Cette fonction récupère les actions effectuées à la manette et
        effectue des opérations spécifiques correspondantes. La fonction
        get.button(n) avec n un nombre entier permet de savoir si la touche
        correspondante au nombre n est pressé
        """
        choice = pg.key.get_pressed()
        if not pause and not busy:
            # Modifie les animations en fonction de l'input
            # Gère le blocage
            if (contro[0].get_button(3) and
                    self.player_0.vals['current_height'] == 0):
                self.player_0.block()
            # Gère les mouvements à la manette
            elif contro[0].get_axis(0) // 3500 < -5 or (
                    contro[0].get_axis(0) // 3500 > 5):
                if contro[0].get_axis(0) > 0:
                    choice[self.get_code("d")]
                    self.player_0.move()
                    self.elms['right'][self.player_0.number] = True
                else:
                    choice[self.get_code("q")]
                    self.player_0.move()
                    self.elms['right'][self.player_0.number] = False
            # Gère les sauts
            if (contro[0].get_button(0) and
                    self.player_0.vals['current_height'] < 400):
                self.player_0.jump_controller(8)
            # Gère les attaques
            for event in actions:
                if self.player_0.vals['current_height'] > 40 and (
                        event.type == JOYBUTTONDOWN and event.button == 1):
                    self.player_0.dash_attack_up_controller()
                elif (contro[0].get_axis(1) / 3500 > 5 and
                      event.type == JOYBUTTONDOWN and event.button == 1):
                    print('sol')
                    self.player_0.attack_down_controller()
                elif event.type == JOYBUTTONDOWN and event.button == 1:
                    self.player_0.attack_controller(
                        contro[0].get_button(1), contro[0])
                elif event.type == JOYBUTTONDOWN and event.button == 2:
                    self.player_0.attack_controller(
                        contro[0].get_button(2), contro[0])

                elif event.type == JOYBUTTONDOWN and event.button == 7:
                    self.player_0.charge()
            if contro[0].get_button(10):
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
                self.player_2.is_dashing(choice, event)
            if event.type == pg.KEYUP and (
                self.elms["side"][self.player_0.number] == 'run'):
                self.player_0.vals['nbr_sprite'] = 5

    def collision(self):
        '''Cette fonction renvoi un bouléen,
        qui est sur True quand il y a une collision entre
        un sprite et un groupe de sprites. Le cas échéant, le
        bouléen est sur False.'''
        # Vérifie si il y a collision ou non
        for element in self.players:
            if element.number == 0:
                return pg.sprite.spritecollide(element, self.all_players_2,
                                               False, pg.sprite.collide_mask)
            elif element.number == 2:
                return pg.sprite.spritecollide(element, self.all_players,
                                               False, pg.sprite.collide_mask)

    def add_groups(self):
        '''Ajoute un objet au groupe de sprites.'''
        # Ajout de l'objet dans le groue de sprite de tout les objets
        self.all_objects.add(self.object)
        # Ajoute un joueur au groupe de sprite de tout les joueurs
        self.all_players.add(self.player_0)
        self.all_players_2.add(self.player_2)

    def strike_collision(self):
        '''Actionne l'attaque du personnage'''
        if self.collision():
            for objects in self.collision():
                objects.damages()
                # Change l'animation en cas d'attaque
                # self.object.image = GFX['hit']
                print('EHo')

    def update_stats(self):
        """
        Met à jour les caractéristiques spéciale comme les barres,
        les attaques spéciales, et les stats.
        """
        for element in self.players:
            if self.name[element.number] == "luffy":
                if element.vals["percent_ult"] <= 130:
                    element.vals["percent_ult"] += 0.1
            elif self.name[element.number] == "gear4":
                if element.vals["percent_ult"] > 0:
                    element.vals["percent_ult"] -= 0.1
                else:
                    self.name[element.number] = "luffy"

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
            # Dessin de la barre de vie du perso 1
            pg.draw.rect(surface, (25, 70, 17), [
                width - 400, height // 15,
                self.player_0.vals['max_health'], 15])
            pg.draw.rect(surface, (75, 198, 9), [
                width - 400, height // 15,
                self.players[0].vals['health'], 15])
            # Nombre d'esquive possible perso 1
            pg.draw.rect(surface, (0, 91, 136), [
                         width - 400, height // 10, 4 * 30, 15])
            pg.draw.rect(surface, (159, 212, 239), [
                width - 400, height // 10,
                self.players[0].vals['nbr_vanish'] * 30, 15])
            # Barre de vie du perso 2
            pg.draw.rect(surface, (25, 70, 17), [
                width // 8, height // 15,
                self.players[1].vals['max_health'], 15])
            pg.draw.rect(surface, (75, 198, 9), [
                width // 8, height // 15,
                self.players[1].vals['health'], 15])
            # Nombre esquive perso 2
            pg.draw.rect(surface, (0, 91, 136), [
                         width // 8, height // 10, 4 * 30, 15])
            pg.draw.rect(surface, (159, 212, 239), [
                width // 8, height // 10,
                self.players[1].vals['nbr_vanish'] * 30, 15])
            # Jauge de spé
            pg.draw.rect(surface, (64, 2, 97), [
                width - 400, height // 7, 130, 15])
            pg.draw.rect(surface, (168, 30, 241), [
                width - 400, height // 7,
                self.player_0.vals['percent_ult'], 15])
            pg.draw.rect(surface, (64, 2, 97), [
                width // 8, height // 7, 130, 15])
            pg.draw.rect(surface, (168, 30, 241), [
                width // 8, height // 7,
                self.player_2.vals['percent_ult'], 15])

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
            self.face = {"image": GFX[self.name[self.player_0.number]]}
            self.face["rect"] = self.face["image"].get_rect()
            self.face["rect"].x = screen.get_width() - 150
            self.face["rect"].y = screen.get_height() // 20
            self.rect_update.append(screen.blit(
                self.face["image"], (self.face["rect"])))
            self.rect_update.append(screen.blit(
                self.box["image"],
                (screen.get_width() // 60, 0)))
            # Visage
            self.face2 = {"image": GFX[self.name[self.player_2.number]]}
            self.face2["rect"] = self.face2["image"].get_rect()
            self.face2["rect"].x = screen.get_width() // 20
            self.face2["rect"].y = screen.get_height() // 20
            self.rect_update.append(screen.blit(
                self.face2["image"], (self.face2["rect"])))
        return self.rect_update

    def update_players(self, screen):
        """
        Mis à jour des persos
        """
        for element in self.players:
            element.gravity()
            #element.damages()
            element.dash()
            self.update_stats()
            self.ulti.spe_goku(screen)

    def update(self, screen, dlt, actions, pause, busy, contro, music):
        '''Cette fonction permet de mettre à jour les événements
        du jeu.'''
        # Affiche le personnage sur l'écran
        rects = []
        rects.append(self.player_0.blit_sprite(screen, dlt, pause))
        rects.append(self.player_2.blit_sprite(screen, dlt, pause))
        rects.append(self.player_1.update(dlt, pause, busy, self.player_0, music))
        for element in self.update_header(screen, busy):
            rects.append(element)
        # Gère les inputs
        self.handle_input(actions, pause, busy, screen)
        # Gère les inputs à la manette
        # Si il y a au moins une manette de connecté:
        events = False
        for event in actions:
            if 'joy' in event.dict:
                if event.dict['joy'] == 0:
                    events = True
        if events:
            if contro != None:
                print('la')
                self.handle_input_controller(actions, pause, busy, contro)
        # Renvoi le rectangle du joueur
        self.update_health(screen, busy)
        self.update_players(screen)
        return rects, [self.player_0, self.player_1]
