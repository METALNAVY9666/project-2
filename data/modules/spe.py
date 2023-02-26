"""Module qui gère les attaques spéciales"""
import pygame as pg
from data.modules.animations import Animate


class Special(pg.sprite.Sprite):
    """Classe qui gère les attaque spéciales."""

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.animate = Animate(self)
        print('la spé de', self.game.name, 'est chargée.')
        # self.pl1_speed = self.game.player_1.pkg["dimensions"][0] / 1920 * 3

    def spe_manager(self, screen, choice):
        "Gestion des attaque spéciales"
        if choice[self.game.get_code("r")]:
            self.spe_itachi(screen)
            self.spe_luffy(screen)

    def spe_luffy(self, screen):
        """
        Attaque spéciale de luffy
        """
        for element in self.game.players:
            if element.game.name[element.number] == "luffy":
                if element.vals["percent_ult"] >= 130:
                    self.animate.fade(screen.get_width(), screen.get_height(), screen)
                    self.game.name[element.number] = 'gear4'
                    element.vals['nbr_sprite'] = 0
                    self.game.elms['side'][element.number] = 'ult'
                    self.game.player_0.vals['strike'] = 30

    def spe_itachi(self, screen):
        """
        Attaque spéciale d'itachi
        """
        for element in self.game.players:
            if self.game.name[element.number] == 'itachi':
                self.game.elms['side'][element.number] = "ult"
                if 0 < element.vals["health"] < element.vals["max_health"] // 3:
                    if element.vals["percent_ult"] >= 130:
                        element.vals["percent_ult"] = 0
                        self.animate.fade(screen.get_width(),
                                          screen.get_height(), screen)
                        victime = self.who_is_victime(element)
                        if victime.game.name[victime.number] == "kim":
                            victime.player["hp"] = victime.pkg["dimensions"][0] / 1920 * 3
                        else:
                            victime.vals["nbr_vanish"] = 0

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

    def spe_vegeta(self):
        """
        Attaque spéciale de vegeta
        """
        if self.game.name == 'vegeta':
            """On passe un boulééen sur True."""
            """On charge une variable random."""
            """A chaque attaque, si le bouléen est sur True"""
            """ Si les attaque touches et que le random est sur 2."""
            """lE joueur Adverse ne peut pas bouger."""

    def spe_goku(self, screen):
        """
        Animations + Transfo de goku
        """
        for element in self.game.players:
            if element.game.name[element.number] == "goku":
                element.vals["percent_ult"] = 130
                if element.vals["health"] <= 0:
                    self.game.name[element.number] = "revive"
                    self.animate.fade(screen.get_width(),
                                      screen.get_height(), screen)
                    self.game.elms["side"][element.number] = "transfo"
                    element.vals["health"] = 100
                    element.vals["percent_ult"] = 0
