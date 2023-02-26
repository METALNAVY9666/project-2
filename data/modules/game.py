'''Ce module est le jeu, il gère les inputs, les collisions ainsi que
les différents événements dans le jeu.'''
import pygame as pg
from data.modules.fighter import Fighter
from data.modules.gunner import Gunner
# from data.modules.thing import PunchingBall
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
        self.init_dict(pkg, prop)
        self.init_players(pkg, prop)
        self.init_group()

    def init_dict(self, pkg, prop):
        """
        Initialisation des dictionnaires"""
        self.elms = {}
        self.elms["right"] = [False, True]
        self.elms["fps"] = 60
        self.elms["side"] = ["left", "left"]
        self.elms["pkg"] = pkg
        self.elms["prop"] = prop

    def init_players(self, pkg, prop):
        """Initialisation des personnages"""
        if self.name[0] == "kim":
            self.player_0 = Gunner(self, pkg, prop, 0)
            self.player_1 = Fighter(self, pkg, prop, 1)
        elif self.name[1] == "kim":
            self.player_0 = Fighter(self, pkg, prop, 0)
            self.player_1 = Gunner(self, pkg, prop, 1)
        elif "kim" not in self.name:
            self.player_0 = Fighter(self, pkg, prop, 0)
            self.player_1 = Fighter(self, pkg, prop, 1)
        self.players = [self.player_0, self.player_1]
        self.ulti = Special(self)
        # self.object = PunchingBall(self)

    def init_group(self):
        """Initialisation des personnages dans leur groupes"""
        # self.all_objects = pg.sprite.Group()
        self.all_players_0 = pg.sprite.Group()
        self.all_players_1 = pg.sprite.Group()
        self.add_groups()

    def get_code(self, key):
        "renvoie la valeur de la touche"
        return pg.key.key_code(key)

    def handle_input(self, actions, pause, busy, screen):
        '''Cette fonction a pour but de récupérer les touches préssées.
        En fonction de celles-ci, on effectue des opération spécifiques.
        La fonction get_pressed() récupère les touches préssées actuellement,
        et gère des actions en continu comme le fait d'avancer.'''
        choice = pg.key.get_pressed()
        if not pause and not busy and self.name[0] != "kim":
            # Récupère les touches préssées actuellement
            self.player_0.vals['pause'] = True
            # Réaffecte l'image de l'objet
            # self.object.image = GFX['punchingball']
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
            elif choice[self.get_code("z")] and not choice[self.get_code("y")]:
                self.player_0.jump()
            # Gère le bloquage
            elif choice[self.get_code("s")]:
                self.player_0.block()
            if choice[self.get_code("z")] and choice[self.get_code("s")]:
                self.player_0.charge()
            self.ulti.spe_manager(screen, choice)
            # Actions qui nécessitent une boucle 'for'
            self.loop_input(actions)
        self.handle_input_player2(choice, pause, busy)

    def handle_input_player2(self, choice, pause, busy):
        """Saisie clavier pour le perso 2"""
        if not pause and not busy and self.name[1] != "kim":
            self.player_1.vals["pause"] = True
            # print(self.elms['right'][self.player_0.number])
            if choice[self.get_code("right")]:
                self.elms['right'][self.player_1.number] = True
                self.player_1.move()
                if choice[self.get_code("up")]:
                    self.player_1.jump()
            elif choice[self.get_code("left")]:
                self.elms['right'][self.player_1.number] = False
                self.player_1.move()
                if choice[self.get_code("up")]:
                    self.player_1.jump()
            elif choice[self.get_code("up")]:
                self.player_1.jump()
            elif choice[self.get_code("down")]:
                self.player_1.block()
            if choice[self.get_code("down")] and choice[self.get_code("up")]:
                self.player_1.charge()

    def handle_input_controller(self, actions, pause, busy, contro, num):
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
            if (contro[num].get_button(3) and
                    self.player_0.vals['current_height'] == 0):
                self.player_0.block()
            # Gère les mouvements à la manette
            elif contro[num].get_axis(0) // 3500 < -5 or (
                    contro[num].get_axis(0) // 3500 > 5):
                if contro[num].get_axis(0) > 0:
                    choice[self.get_code("d")]
                    self.player_0.move()
                    self.elms['right'][self.player_0.number] = True
                else:
                    choice[self.get_code("q")]
                    self.player_0.move()
                    self.elms['right'][self.player_0.number] = False
            # Gère les sauts
            if (contro[num].get_button(0) and
                    self.player_0.vals['current_height'] < 400):
                self.player_0.jump_controller(8)
            # Gère les attaques
            for event in actions:
                if self.player_0.vals['current_height'] > 40 and (
                        event.type == JOYBUTTONDOWN and event.button == 1):
                    self.player_0.dash_attack_up_controller()
                elif (contro[num].get_axis(1) / 3500 > 5 and
                      event.type == JOYBUTTONDOWN and event.button == 1):
                    print('sol')
                    self.player_0.attack_down_controller()
                elif event.type == JOYBUTTONDOWN and event.button == 1:
                    self.player_0.attack_controller(
                        contro[num].get_button(1), contro[num])
                elif event.type == JOYBUTTONDOWN and event.button == 2:
                    self.player_0.attack_controller(
                        contro[num].get_button(2), contro[num])

                elif event.type == JOYBUTTONDOWN and event.button == 7:
                    self.player_0.charge()
            if contro[num].get_button(10):
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
                for element in self.players:
                    if self.name[element.number] != "kim":
                        element.vals["fall"] = True
                        element.attack(event, choice)
                        element.move_manager(event)
                        element.vanish(event)
                        element.is_dashing(choice, event)
                        element.dash_attack_up(choice, event)
                    if event.type == pg.KEYUP and (
                            self.elms["side"][element.number] == 'run'):
                        self.player_0.vals['nbr_sprite'] = 5

    def collision(self):
        '''Cette fonction renvoi un bouléen,
        qui est sur True quand il y a une collision entre
        un sprite et un groupe de sprites. Le cas échéant, le
        bouléen est sur False.'''
        # Vérifie si il y a collision ou non
        for element in self.players:
            if "kim" not in self.name:
                if element.number == 0:
                    return pg.sprite.spritecollide(element,
                                                   self.all_players_1,
                                                   False,
                                                   pg.sprite.collide_mask)
                elif element.number == 1:
                    return pg.sprite.spritecollide(element,
                                                   self.all_players_0,
                                                   False,
                                                   pg.sprite.collide_mask)
            else:
                if self.name[element.number] == "kim":
                    if element.number == 0:
                        return element.pkg["Rect"].colliderect(
                            element.get_rect(), self.player_1)
                    elif element.number == 1:
                        return element.pkg["Rect"].colliderect(
                            element.get_rect(), self.player_0)

    def add_groups(self):
        '''Ajoute un objet au groupe de sprites.'''
        # Ajout de l'objet dans le groue de sprite de tout les objets
        # self.all_objects.add(self.object)
        # Ajoute un joueur au groupe de sprite de tout les joueurs
        self.all_players_0.add(self.player_0)
        self.all_players_1.add(self.player_1)

    def strike_collision(self, ennemy):
        '''Actionne l'attaque du personnage'''
        if self.collision():
            if "kim" not in self.name:
                for element in self.collision():
                    if self.players[ennemy.number] == self.player_0:
                        self.player_0.vals["health"] -= 10
                        self.elms["side"][0] = "hit"
                    elif self.players[element.number] == self.player_1:
                        self.player_1.vals["health"] -= 10
                        self.elms["side"][1] = "hit"
            else:
                if self.name[ennemy.number] == "kim":
                    ennemy.player["hp"] -= 10

                # Change l'animation en cas d'attaque
                # self.object.image = GFX['hit']

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
        """self.object.forward()
        self.object.gravity_object()
        # Met le punching ball à jour
        return screen.blit(self.object.image, (self.object.rect))"""

    def update_health(self, surface, busy):
        '''Cette fonction dessine la barre de vie, d'énergie, et de défense du
        perso.Chaque barre possède une longueur propre au montant de sa
        variable respective. On dessine d'abord une barre grise, afin de faire
        le fond, puis on dessine celleavec de la couleur. Les deux, sur la
        surface donnée en paramètre.'''
        width = self.elms["pkg"]["surface"].get_width()
        height = self.elms["pkg"]["surface"].get_height()
        if not busy:
            self.update_hp_player_0(surface, width, height)
            self.update_hp_player_1(surface, width, height)

    def update_hp_player_0(self, surface, width, height):
        if self.name[0] != "kim":
            pg.draw.rect(surface, (25, 70, 17), [
                width // 8, height // 15,
                self.player_0.vals['max_health'], 15])
            pg.draw.rect(surface, (75, 198, 9), [
                width // 8, height // 15,
                self.players[0].vals['health'], 15])
            # Nombre d'esquive possible perso 1
            pg.draw.rect(surface, (0, 91, 136), [
                         width // 8, height // 10, 4 * 30, 15])
            pg.draw.rect(surface, (159, 212, 239), [
                width // 8, height // 10,
                self.players[0].vals['nbr_vanish'] * 30, 15])
            pg.draw.rect(surface, (64, 2, 97), [
                width // 8, height // 7, 130, 15])
            pg.draw.rect(surface, (168, 30, 241), [
                width // 8, height // 7,
                self.player_0.vals['percent_ult'], 15])
        else:
            pg.draw.rect(surface, (25, 70, 17), [
                width // 8, height // 15,
                100, 15])
            pg.draw.rect(surface, (75, 198, 9), [
                width // 8, height // 15,
                self.players[0].player['hp'], 15])

    def update_hp_player_1(self, surface, width, height):
        if self.name[1] != 'kim':
            # Barre de vie du perso 2
            pg.draw.rect(surface, (25, 70, 17), [
                width - 400, height // 15,
                self.players[1].vals['max_health'], 15])
            pg.draw.rect(surface, (75, 198, 9), [
                width - 400, height // 15,
                self.players[1].vals['health'], 15])
            # Nombre esquive perso 2
            pg.draw.rect(surface, (0, 91, 136), [
                         width - 400, height // 10, 4 * 30, 15])
            pg.draw.rect(surface, (159, 212, 239), [
                width - 400, height // 10,
                self.players[1].vals['nbr_vanish'] * 30, 15])
            # Jauge de spé
            pg.draw.rect(surface, (64, 2, 97), [
                width - 400, height // 7, 130, 15])
            pg.draw.rect(surface, (168, 30, 241), [
                width - 400, height // 7,
                self.player_1.vals['percent_ult'], 15])
        else:
            pg.draw.rect(surface, (25, 70, 17), [
                width - 400, height // 15,
                100, 15])
            pg.draw.rect(surface, (75, 198, 9), [
                width - 400, height // 15,
                self.players[1].player['hp'], 15])

    def update_header(self, screen, busy):
        """
        Fonction qui met à jour les élements du haut de l'écran
        """
        rect_update = []
        if not busy:
            self.update_box(screen, rect_update)
            self.update_face(screen, rect_update)
        return rect_update

    def update_box(self, screen, rect_update):
        """
        Mis à jour des box
        """
        # Boite de stats
        self.box = {"image": GFX['stats_box']}
        self.box['rect'] = self.box["image"].get_rect()
        self.box["rect"].x = screen.get_width() - 450
        rect_update.append(screen.blit(
            self.box["image"], (self.box["rect"])))
        rect_update.append(screen.blit(
            self.box["image"],
            (screen.get_width() // 60, 0)))

    def update_face(self, screen, rect_update):
        """
        Mis à jour des visages
        """
        # Visage
        if self.name[0] == "kim":
            self.face = {
                "image": GFX[self.name[self.player_0.number]+"_face"]}
        else:
            self.face = {"image": GFX[self.name[self.player_0.number]]}
        self.face["rect"] = self.face["image"].get_rect()
        self.face["rect"].x = screen.get_width() // 20
        self.face["rect"].y = screen.get_height() // 20
        rect_update.append(screen.blit(
            self.face["image"], (self.face["rect"])))
        # Visage
        if self.name[1] == "kim":
            self.face2 = {
                "image": GFX[self.name[self.player_1.number]+"_face"]}
        else:
            self.face2 = {"image": GFX[self.name[self.player_1.number]]}
        self.face2["rect"] = self.face2["image"].get_rect()
        self.face2["rect"].x = screen.get_width() - 150
        self.face2["rect"].y = screen.get_height() // 20
        rect_update.append(screen.blit(
            self.face2["image"], (self.face2["rect"])))

    def update_players(self, screen, busy):
        """
        Mis à jour des persos
        """
        for element in self.players:
            if self.name[element.number] != "kim":
                element.gravity()
                # element.damages()
                element.dash()
                self.ulti.spe_goku(screen)
                self.update_stats()
        self.update_health(screen, busy)

    def rect_append_gunner(self, rects, dlt, pause, busy, music):
        """
        Rect des gunners
        """
        if self.name[0] == "kim":
            rects.append(self.player_0.update(
                dlt, pause, busy, self.player_1, music))
        elif self.name[1] == "kim":
            rects.append(self.player_1.update(
                dlt, pause, busy, self.player_0, music))

    def rect_append_fighter(self, rects, screen, dlt, pause):
        """
        rect des fighters
        """
        if self.name[0] != "kim":
            rects.append(self.player_0.blit_sprite(screen, dlt, pause))
        if self.name[1] != "kim":
            rects.append(self.player_1.blit_sprite(screen, dlt, pause))

    def update(self, screen, dlt, actions, pause, busy, contro, music):
        '''Cette fonction permet de mettre à jour les événements
        du jeu.'''
        # Affiche le personnage sur l'écran
        rects = []
        self.rect_append_gunner(rects, dlt, pause, busy, music)
        self.rect_append_fighter(rects, screen, dlt, pause)
        for element in self.update_header(screen, busy):
            rects.append(element)
        # Gère les inputs
        self.handle_input(actions, pause, busy, screen)
        # Gère les inputs à la manette
        # Si il y a au moins une manette de connecté:
        if contro != None and len(contro) == 2:
            print('la')
            self.handle_input_controller(actions, pause, busy, contro, 1)
        # Renvoi le rectangle du joueur
        self.update_players(screen, busy)
        return rects, self.players
