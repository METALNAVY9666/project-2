"""Module qui gère les attaques spéciales"""
import pygame as pg
from data.modules.animations import Animate
from data.modules.audio import SFX


class Special(pg.sprite.Sprite):
    """Classe qui gère les attaque spéciales."""

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.animate = Animate(self)
        print('la spé de', self.game.name, 'est chargée.')
        # self.pl1_speed = self.game.player_1.pkg["dimensions"][0] / 1920 * 3
        self.init_dict()

    def init_dict(self):
        self.can_spe = {}
        self.can_spe["goku"] = True
        self.can_spe["itachi"] = True
        self.can_spe["luffy"] = True
        self.can_spe["vegeta"] = True

    def spe_manager(self, screen, element):
        "Gestion des attaque spéciales"
        name = element.game.name[element.number]
        print(name)
        match name:
            case "itachi":
                self.spe_itachi(screen, element)
            case "luffy":
                self.spe_luffy(screen, element)
            case "vegeta":
                self.spe_vegeta(element)

    def spe_luffy(self, screen, element):
        """
        Attaque spéciale de luffy
        """
        if element.vals["percent_ult"] >= 130:
            SFX["luffy"]["spe"].play()
            self.animate.fade(screen.get_width(),
                              screen.get_height(), screen, element)
            self.game.name[element.number] = 'gear4'
            element.vals['nbr_sprite'] = 0
            self.game.elms['side'][element.number] = 'ult'
            element.upgrade_stats()

    def spe_itachi(self, screen, element):
        """
        Attaque spéciale d'itachi
        """
        if self.can_spe["itachi"]:
            self.game.elms['side'][element.number] = "ult"
            if 0 < element.vals["health"] < element.vals["max_health"] // 3:
                if element.vals["percent_ult"] >= 130:
                    SFX["itachi"]["spe"].play()
                    element.vals["percent_ult"] = 0
                    self.animate.fade(screen.get_width(),
                                      screen.get_height(), screen, element)
                    victime = self.who_is_victime(element)
                    self.can_spe["itachi"] = False
                    if victime.game.name[victime.number] == "kim":
                        victime.player["hp"] //= 2
                    else:
                        victime.degrade_stats()

    def who_is_victime(self, element):
        """
        Mais qui sera la victime d'Itachi ?
        """
        victime = element
        if self.game.name[0] == "itachi":
            victime = self.game.players[1]
        elif self.game.name[1] == "itachi":
            victime = self.game.players[0]
        return victime

    def spe_vegeta(self, element):
        """
        Attaque spéciale de vegeta
        """
        SFX["vegeta"]["spe"].play()
        self.can_spe["vegeta"] = False
        if element.vals["percent_ult"] > 0:
            element.vals["attacked"] = True

    def spe_goku(self, screen):
        """
        Animations + Transfo de goku
        """
        for element in self.game.players:
            if element.game.name[element.number] == "goku":
                element.vals["percent_ult"] = 130
                if element.vals["health"] <= 0:
                    self.can_spe["goku"] = False
                    SFX["goku"]["damage"].stop()
                    SFX["goku"]["spe"].play()
                    SFX["goku"]["transfo"].play()
                    self.game.name[element.number] = "revive"
                    self.animate.fade(screen.get_width(),
                                      screen.get_height(), screen, element)
                    self.game.elms["side"][element.number] = "transfo"
                    element.upgrade_stats()
                    element.vals["percent_ult"] = 0
