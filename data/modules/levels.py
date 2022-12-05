"""ce module contient les différents niveaux"""
from data.modules.texture_loader import GFX
from data.modules.players import TestPlayer
from data.modules.gui import PauseMenu
from data.modules.keyboard import KeyChecker


class Background:
    """créée un fond qui s'adapte à la position des 2 joueurs"""
    def __init__(self, pkg, prop):
        self.pkg = pkg
        self.prop = prop
        self.pos = (0, 0)
        self.dims = pkg["dimensions"]
        self.scl = self.prop["scale"]
        self.scl_ex = []
        for axe in (0, 1):
            self.scl_ex.append(self.scl[axe] - self.dims[axe])

    def clamp(self):
        """verouille la position du fond"""
        for axe in [0, 1]:
            if self.pos[axe] > axe:
                self.pos[axe] = 0
            if self.pos[axe] < -self.scl_ex[axe]:
                self.pos[axe] = -self.scl_ex[axe]

    def move(self, pos):
        """bouge le fond pour donner un effet de mouvement"""
        self.pos = pos

    def update(self):
        """met à jour la position du fond en fonction de
        la position des joueurs"""
        bg_img = GFX[self.prop["bg"]]["bg"]
        self.clamp()
        bg_rect = self.pkg["surface"].blit(bg_img, self.pos)
        return bg_rect


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
        background = Background(self.pkg, self.level_prop)
        self.cls["bg"] = background
        pause_menu = PauseMenu(self.pkg)
        self.cls["pause"] = pause_menu
        key_checker = KeyChecker(self.pkg, self.cls["pause"])
        self.cls["key"] = key_checker

    def init_audio(self):
        """initialise l'audio du niveau"""
        bg_music_path = self.level_prop["music"]
        volume = self.settings["audio"]["music"]/100
        self.pkg["mixer"].music.load(bg_music_path)
        self.pkg["mixer"].music.set_volume(volume)
        self.pkg["mixer"].music.play()

    def init_players(self):
        """initialise les joueurs"""
        self.players = []
        self.players.append([TestPlayer(0, self.pkg), None])
        self.players.append([TestPlayer(1, self.pkg), None])
        for element in (0, 1):
            player = self.players[element][0]
            temp = player.update(element, self.cls["pause"].bool)
            self.players[element][1] = temp

    def update(self, delta):
        """met à jour le niveau, renvoie si le niveau est terminé ou
        non, et le score"""
        next_op = None
        keys = [self.pkg["pygame"].K_ESCAPE]
        self.cls["key"].check_keys(keys)

        self.update_list.append(self.cls["bg"].update())

        player = self.players[1][0]
        pos, player_rect = player.update(delta, self.cls["pause"].bool)
        self.cls["bg"].pos = pos
        self.update_list.append(player_rect)

        next_op, pause_rects = self.cls["pause"].update()
        if pause_rects is not None:
            for rect in pause_rects:
                self.update_list.append(rect)

        self.pkg["display"].update(self.update_list)
        self.update_list = []
        return next_op
