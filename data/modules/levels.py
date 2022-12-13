"""ce module contient les différents niveaux"""
from data.modules.texture_loader import GFX
from data.modules.players import TestPlayer
from data.modules.gui import PauseMenu
from data.modules.keyboard import KeyChecker
from data.modules.audio import Music

class BackgroundOne:
    """créée un fond qui s'adapte à la position d'un unique joueur"""
    def __init__(self, pkg, prop):
        self.pkg = pkg
        self.prop = prop
        self.pos = [0, 0]
        self.dims = pkg["dimensions"]
        self.scl = self.prop["scale"]
        self.scl_ex = []
        for axe in (0, 1):
            self.scl_ex.append(self.scl[axe] - self.dims[axe])

    def clamp(self):
        """verouille la position du fond"""
        clamps = [[False, False], [False, False]]
        for axe in [0, 1]:
            if self.pos[axe] >= 0:
                self.pos[axe] = 0
                clamps[axe][0] = True
            if self.pos[axe] <= -self.scl_ex[axe]:
                self.pos[axe] = -self.scl_ex[axe]
                clamps[axe][1] = True
        return clamps

    def move(self, pos):
        """bouge le fond pour donner un effet de mouvement"""
        self.pos = pos

    def update(self, player):
        """met à jour la position du fond en fonction de
        la position des joueurs"""
        bg_img = GFX[self.prop["bg"]]["bg"]
        player.clamps = self.clamp()
        bg_rect = self.pkg["surface"].blit(bg_img, self.pos)
        return bg_rect


class BackgroundTwo:
    """met à jour la position du fond en fonction du joueur"""
    def __init__(self, pkg, prop):
        self.pkg = pkg
        self.bg_pos = [0, 0]
        self.base_scale = prop["scale"]
        self.scale = self.base_scale*1
        self.p_pos = [[0, 0], [0, 0]]
        self.bg = GFX[prop["bg"]]

    def change_scale(self, img, scl):
        """renvoie l'image avec taille modifiée"""
        return self.pkg["pygame"].tansform.scale(img, scl)

    def update(self):
        """met à jour la position de l'écran en fonction des joueurs"""
        self.bg_pos[0] = abs(self.p_pos[0][0]-self.p_pos[1][0])
        self.bg_pos[1] = abs(self.p_pos[0][1]-self.p_pos[1][1])
        return self.bg, self.bg_pos


class BaseLevel:
    """générateur de niveaux"""
    def __init__(self, pygame_pack, level_prop, game_settings):
        """mettre pack_pygame, les propriétés du niveau et les paramètres
        du jeu en parametres afin de pouvoir modifier la scène sans recharger
        """
        self.update_list = []
        self.init_prop(pygame_pack, level_prop, game_settings)
        self.init_ui()
        self.init_audio()
        self.init_players()

    def init_prop(self, pygame_pack, level_prop, game_settings):
        """initlialise les variables et propriétés de la classe BaseLevel"""
        self.level_prop = level_prop
        self.pkg = pygame_pack
        self.settings = game_settings

    def init_ui(self):
        """initialise l'interface graphique du niveau"""
        self.cls = {}
        self.pkg["mouse"].set_visible(False)
        # background = BackgroundOne(self.pkg, self.level_prop)
        background = BackgroundTwo(self.pkg, self.level_prop)
        self.cls["bg"] = background
        pause_menu = PauseMenu(self.pkg)
        self.cls["pause"] = pause_menu
        key_checker = KeyChecker(self.pkg, self.cls["pause"])
        self.cls["key"] = key_checker

    def init_audio(self):
        """initialise l'audio du niveau"""
        bg_music = Music(self.pkg, self.level_prop, self.settings)
        bg_music.play()
        self.cls["pause"].bg_music = bg_music

    def init_players(self):
        """initialise les joueurs"""
        self.players = []
        self.players.append(TestPlayer(0, self.pkg))
        self.players.append(TestPlayer(1, self.pkg))
        self.players[1].player_pos = self.level_prop["scale"]
        """ version 1 joueur
        for element in (0, 1):
            player = self.players[element][0]
            pos = self.cls["bg"].pos
            temp = player.update(element, self.cls["pause"].bool, pos)
            self.players[element][1] = temp"""

    def display(self, data):
        """affiche des trucs"""
        temp = self.pkg["surface"].blit(data[0], data[1])
        return temp

    def update(self, delta):
        """met à jour le niveau, renvoie si le niveau est terminé ou
        non, et le score"""
        next_op = None
        keys = [self.pkg["pygame"].K_ESCAPE]
        self.cls["key"].check_keys(keys)
        """ version 1 joueur player = self.players[1][0]"""

        # met à jour le fond
        pause = self.cls["pause"].bool
        for elt in (0, 1):
            self.cls["bg"].p_pos[elt] = self.players[elt].move(delta,pause)
        rect = self.display(self.cls["bg"].update())
        self.update_list.append(rect)
        """self.update_list.append(self.cls["bg"].update(player))"""

        # met à jour le joueur
        """pos = self.cls["bg"].pos
        pos, player_rect = player.update(delta, pause, pos)
        self.cls["bg"].pos = pos
        self.update_list.append(player_rect)"""


        # met à jour le menu pause
        next_op, pause_rects = self.cls["pause"].update()
        if pause_rects is not None:
            for rect in pause_rects:
                self.update_list.append(rect)

        # self.pkg["display"].update(self.pkg["surface"].blit(GFX[self.level_prop["bg"]], (0,0)))
        self.pkg["display"].update(self.update_list)
        print(self.update_list)
        self.update_list = []
        return next_op
