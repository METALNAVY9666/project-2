'''Ce module est le jeu, il gère les inputs, les collisions ainsi que
les différents événements dans le jeu.'''
import pygame as pg
from data.modules.fighter import Fighter
from data.modules.gunner import Gunner
from data.modules.texture_loader import GFX
from data.modules.audio import SFX
from data.modules.spe import Special
from data.modules.settings import read_settings
from data.modules.keyboard import azerty_to_qwerty
from pygame.locals import JOYBUTTONDOWN
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
        self.elms["fps"] = pkg["FPS"]
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
        self.init_keys()
        self.ulti = Special(self)
        self.start_audio()
        # self.object = PunchingBall(self)

    def start_audio(self):
        """
        Audio des personnages à l'entrée en scène
        """
        if self.name[0] != "kim":
            SFX[self.name[0]]["start"].play()
            pg.time.wait(1000)
        if self.name[1] != "kim":
            pg.time.wait(1000)
            SFX[self.name[1]]["start"].play()

    def init_group(self):
        """
        Initialisation des personnages dans leur groupes
        """
        # self.all_objects = pg.sprite.Group()
        self.all_players_0 = pg.sprite.Group()
        self.all_players_1 = pg.sprite.Group()
        self.add_groups()

    def init_keys(self):
        """initialise les touches des personngaes"""
        self.elms["keymap"] = []
        self.players = [self.player_0, self.player_1]
        for player in self.players:
            if type(player).__name__ == "Fighter":
                self.elms["keymap"].append(
                    read_settings()["keys"][player.number])
        self.ulti = Special(self)
        # self.object = PunchingBall(self)

    def get_code(self, key):
        "renvoie la valeur de la touche"
        return pg.key.key_code(key)

    def convert_key(self, key, element):
        """renvoie la classe pygame de la clé"""
        if "kim" in self.name:
            keymap = self.elms["keymap"][0]
            return pg.key.key_code(azerty_to_qwerty(keymap[key]))
        if self.name[element.number] != "kim":
            keymap = self.elms["keymap"][element.number]
            return pg.key.key_code(azerty_to_qwerty(keymap[key]))

    def handle_input(self, actions, pause, busy, screen):
        '''Cette fonction a pour but de récupérer les touches préssées.
        En fonction de celles-ci, on effectue des opération spécifiques.
        La fonction get_pressed() récupère les touches préssées actuellement,
        et gère des actions en continu comme le fait d'avancer.'''
        choice = pg.key.get_pressed()
        for element in self.players:
            if not pause and not busy and self.name[element.number] != "kim":
                # Récupère les touches préssées actuellement
                element.vals['pause'] = True
                # Modifie les animations en fonction de l'input
                element.vals["attacked"] = False
                if choice[self.convert_key("right", element)]:
                    if choice[self.convert_key("jump", element)]:
                        element.jump()
                    element.move()
                    self.elms['right'][element.number] = True
                elif choice[self.convert_key("left", element)]:
                    if choice[self.convert_key("jump", element)]:
                        element.jump()
                    element.move()
                    self.elms['right'][element.number] = False
                    if self.name in ['goku', 'vegeta']:
                        self.elms["side"][element.number] = 'left'
                self.handle_input_part2(choice, element, actions, screen)

    def handle_input_part2(self, choice, element, actions, screen):
        """
        Gère les actions du joueur
        """
        # Gère les sauts
        if choice[self.convert_key("jump", element)] and (
                not choice[self.convert_key("l_attack", element)]):
            element.jump()
        elif choice[self.convert_key("l_attack", element)] and (
                choice[self.convert_key("jump", element)]):
            element.attack_up()
        elif choice[self.convert_key("l_attack", element)] and (
                choice[self.convert_key("block", element)]):
            element.attack_down()
        # Gère le bloquage
        elif choice[self.convert_key("block", element)]:
            element.block()
        if choice[self.convert_key("jump", element)] and (
                choice[self.convert_key("block", element)]):
            element.charge()
        if choice[self.convert_key("block", element)] and (
                choice[self.convert_key("h_attack", element)]):
            self.ulti.spe_manager(screen, element)
        # Actions qui nécessitent une boucle 'for'
        self.loop_input(actions)

    def handle_input_contro_part1(self, contro, choice, num):
        """
        Gère une partie des actions à la manette. (Blocage, mouvement,
        sauts, dash)
        """
        # Gère le blocage
        if (contro[num].get_button(3) and
                self.player_0.vals['current_height'] == 0):
            self.player_0.block()

        # Gère les mouvements à la manette
        elif contro[num].get_axis(0) // 3500 < -5 or (
                contro[num].get_axis(0) // 3500 > 5):
            # Droite
            if contro[num].get_axis(0) > 0:
                choice[self.convert_key("right", self.players[0])]
                self.player_0.move()
                self.elms['right'][self.player_0.number] = True
            # Gauche
            else:
                choice[self.convert_key("left", self.players[0])]
                self.player_0.move()
                self.elms['right'][self.player_0.number] = False

        # Gère les sauts
        if (contro[num].get_button(0) and
                self.player_0.vals['current_height'] < 400):
            self.player_0.jump_controller(8)

        # Gère les dash
        # Dash droit
        if contro[num].get_axis(2) // 3500 > 5:
            self.player_0.vals["dashing"][self.player_0.number] = True
            self.player_0.game.elms["right"][self.player_0.number] = True
            self.player_0.dash()
        # Dash gauche
        if contro[num].get_axis(2) // 3500 < -5:
            self.player_0.vals["dashing"][self.player_0.number] = True
            self.player_0.game.elms["right"][self.player_0.number] = False
            self.player_0.dash()

    def handle_input_contro_attacks(self, actions, contro, num):
        """
        Gère une partie des actions à la manette. (Attaques)
        """
        # Gère les attaques
        for event in actions:
            if self.player_0.vals['current_height'] > 40 and (
                    event.type == JOYBUTTONDOWN and event.button == 1):
                self.player_0.dash_attack_up_controller()
            # Attaque au sol
            elif (contro[num].get_axis(1) / 3500 > 5 and
                  event.type == JOYBUTTONDOWN and event.button == 2):
                choice = "Sol"
                self.player_0.attack_controller(choice, contro[num])
            # Attaque en haut
            elif (contro[num].get_axis(1) / 3500 < -5 and
                  event.type == JOYBUTTONDOWN and event.button == 1):
                choice = "Air"
                self.player_0.attack_controller(choice, contro[num])
            # Attaques normales
            elif event.type == JOYBUTTONDOWN and event.button == 1:
                self.player_0.attack_controller(
                    contro[num].get_button(1), contro[num])
            elif event.type == JOYBUTTONDOWN and event.button == 2:
                self.player_0.attack_controller(
                    contro[num].get_button(2), contro[num])

    def handle_input_controller(self, actions, pause, busy, contro):
        """
        Cette fonction récupère les actions effectuées à la manette et
        effectue des opérations spécifiques correspondantes pour le joueur 1.
        La fonction get.button(n) avec n un nombre entier permet de savoir
        si la touche correspondante au nombre n est pressé
        """
        choice = pg.key.get_pressed()
        num = 1
        if not pause and not busy and self.name[0] != "kim":
            if len(contro) < 2:
                num = 0
            self.handle_input_contro_part1(contro, choice, num)
            self.handle_input_contro_attacks(actions, contro, num)
            # Recharge l'énergie
            if contro[num].get_button(7):
                self.player_0.charge()
            # Gère l'esquive
            if contro[num].get_button(10):
                self.player_0.vanish_controller()

        if len(contro) == 2:
            self.handle_input_controller_player2(pause, actions, busy, contro)

    def handle_input_contro_player1_part1(self, contro, choice, num):
        """
        Gère une partie des actions à la manette pour le joueur 2.
        (Blocage, mouvement, sauts, dash)
        """
        # Gère le blocage
        if (contro[num].get_button(3) and
                self.player_1.vals['current_height'] == 0):
            self.player_1.block()

        # Gère les mouvements à la manette
        elif contro[num].get_axis(0) // 3500 < -5 or (
                contro[num].get_axis(0) // 3500 > 5):
            if contro[num].get_axis(0) > 0:
                choice[self.convert_key("right", self.players[1])]
                self.player_1.move()
                self.elms['right'][self.player_1.number] = True
            else:
                choice[self.convert_key("left", self.players[1])]
                self.player_1.move()
                self.elms['right'][self.player_1.number] = False

        # Gère les sauts
        if (contro[num].get_button(0) and
                self.player_1.vals['current_height'] < 400):
            self.player_1.jump_controller(8)

        # Gère les dash
        # Dash droit
        if contro[num].get_axis(2) // 3500 > 5:
            self.player_1.vals["dashing"][self.player_1.number] = True
            self.player_1.game.elms["right"][self.player_1.number] = True
            self.player_1.dash()
        # Dash gauche
        if contro[num].get_axis(2) // 3500 < -5:
            self.player_1.vals["dashing"][self.player_1.number] = True
            self.player_1.game.elms["right"][self.player_1.number] = False
            self.player_1.dash()

    def handle_input_contro_player1_attacks(self, actions, contro, num):
        """
        Gère une partie des actions à la manette pour le joueur 2. (Attaques)
        """
        # Gère les attaques
        for event in actions:
            # Dash en l'air
            if self.player_1.vals['current_height'] > 40 and (
                    event.type == JOYBUTTONDOWN and event.button == 1):
                self.player_1.dash_attack_up_controller()
            # Attaque au sol
            elif (contro[num].get_axis(1) / 3500 > 5 and
                  contro[num].get_button(2)):
                choice = "Sol"
                self.player_1.attack_controller(choice, contro[num])
            # Attaque en haut
            elif (contro[num].get_axis(1) / 3500 < -5 and
                  event.type == JOYBUTTONDOWN and event.button == 1):
                choice = "Air"
                self.player_1.attack_controller(choice, contro[num])
            # Attaques normales
            elif event.type == JOYBUTTONDOWN and event.button == 1:
                self.player_1.attack_controller(
                    contro[num].get_button(1), contro[num])
            elif event.type == JOYBUTTONDOWN and event.button == 2:
                self.player_1.attack_controller(
                    contro[num].get_button(2), contro[num])

    def handle_input_controller_player2(self, pause, actions, busy, contro):
        """
        Cette fonction récupère les actions effectuées à la manette et
        effectue des opérations spécifiques correspondantes pour le joueur 2.
        La fonction get.button(n) avec n un nombre entier permet de savoir
        si la touche correspondante au nombre n est pressé
        """
        num = 0
        choice = pg.key.get_pressed()
        if not pause and not busy and self.name[1] != "kim":
            self.handle_input_contro_player1_part1(contro, choice, num)
            self.handle_input_contro_player1_attacks(actions, contro, num)

            # Charge l'énergie
            if contro[num].get_button(7):
                self.player_1.charge()

            # Esquive du joueur
            if contro[num].get_button(10):
                self.player_1.vanish_controller()

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
                        element.attack(event)
                        element.move_manager(event)
                        element.vanish(choice)
                        element.is_dashing(choice, event)
                        element.dash_attack_up(choice, event)
                    if event.type == pg.KEYUP and (
                            self.elms["side"][element.number] == 'run'):
                        element.vals['nbr_sprite'] = 5

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
                if element.number == 1:
                    return pg.sprite.spritecollide(element,
                                                   self.all_players_0,
                                                   False,
                                                   pg.sprite.collide_mask)
            else:
                if self.name[element.number] == "kim":
                    if element.number == 0:
                        return element.pkg["Rect"].colliderect(
                            element.get_rect(), self.player_1)
                    if element.number == 1:
                        return element.pkg["Rect"].colliderect(
                            element.get_rect(), self.player_0)
        return None

    def add_groups(self):
        '''Ajoute un objet au groupe de sprites.'''
        # Ajout de l'objet dans le groue de sprite de tout les objets
        # self.all_objects.add(self.object)
        # Ajoute un joueur au groupe de sprite de tout les joueurs
        self.all_players_0.add(self.player_0)
        self.all_players_1.add(self.player_1)

    def strike_collision(self, ennemy):
        '''Actionne l'attaque du personnage'''
        if "kim" not in self.name:
            for element in self.collision():
                if self.players[ennemy.number] == self.player_0:
                    self.player_0.damages(ennemy)
                elif self.players[element.number] == self.player_1:
                    self.player_1.damages(ennemy)
        self.strike_kim(ennemy)

    def strike_kim(self, ennemy):
        """
        Degats contre kim
        """
        limit = self.elms["pkg"]["surface"].get_height()
        if self.name[ennemy.number] == "kim":
            if self.name[0] == "kim":
                striker = self.players[1]
            if self.name[1] == "kim":
                striker = self.players[0]
            ennemy.damage_self(10)
            if 0 < ennemy.physics["pos"][0] < limit:
                if self.elms["right"][striker.number]:
                    ennemy.physics["pos"][0] += 10
                else:
                    ennemy.physics["pos"][0] -= 10

    def update_stats(self):
        """
        Met à jour les caractéristiques spéciale comme les barres,
        les attaques spéciales, et les stats.
        """
        for element in self.players:
            if self.name[element.number] == "luffy" and (
                    element.vals["percent_ult"] <= 130):
                element.vals["percent_ult"] += 0.1
            elif self.name[element.number] == "gear4" and (
                    element.vals["percent_ult"] > 0):
                element.vals["percent_ult"] -= 0.1
                if element.vals["percent_ult"] <= 0:
                    self.name[element.number] = "luffy"
                    element.reset_stats()
            self.update_spe_itachi(element)
            self.update_spe_vegeta(element)

    def update_spe_itachi(self, element):
        
        if self.name[element.number] == "itachi":
            if self.ulti.can_spe["itachi"] and (
                    element.vals["percent_ult"] <= 130):
                element.vals["percent_ult"] += 0.1
            else:
                if self.players[0] == "itachi":
                    self.players[1].reset_stats()
                elif self.players[1] == "itachi":
                    self.players[0].reset_stats()

    def update_spe_vegeta(self, element):
        if self.name[element.number] == "vegeta" and not self.ulti.can_spe["vegeta"]:
            if element.vals["percent_ult"] >= 0:
                element.vals["attacked"] = True
                element.vals["percent_ult"] -= 0.1

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
        """
        Fonction qui met à jour les points de vie du joueur 1
        """
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
            pg.draw.rect(surface, (64, 2, 97), [
                width // 8, height // 7,
                100, 15])
            pg.draw.rect(surface, (168, 30, 241), [
                width // 8, height // 7,
                self.player_0.player['ult']["power"], 15])

    def update_hp_player_1(self, surface, width, height):
        """
        Fonction qui met à jour les points de vie du joueur 2
        """
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
            pg.draw.rect(surface, (64, 2, 97), [
                width - 400, height // 7,
                100, 15])
            pg.draw.rect(surface, (168, 30, 241), [
                width - 400, height // 7,
                self.player_1.player['ult']["power"], 15])

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
                "image": GFX[self.name[self.player_0.number] + "_face"]}
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
                "image": GFX[self.name[self.player_1.number] + "_face"]}
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

    def reset_player_settings(self):
        """réinitialise les paramètres des joueurs"""
        players = [self.player_0, self.player_1]
        for player in players:
            player.init_keymap()
        self.init_keys()

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
        if contro is not None and len(contro) == 2:
            self.handle_input_controller(actions, pause, busy, contro)
        elif contro is not None and len(contro) == 1:
            self.handle_input_controller(actions, pause, busy, contro)
        # Renvoi le rectangle du joueur
        self.update_players(screen, busy)
        return rects, self.players
