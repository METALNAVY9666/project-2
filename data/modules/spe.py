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
        self.pl1_speed = self.game.player_1.pkg["dimensions"][0] / 1920 * 3

    def spe_manager(self, screen, choice):
        "Gestion des attaque spéciales"
        if choice[self.game.get_code("r")]:
            self.spe_itachi()
            self.spe_luffy()

    def spe_luffy(self):
        """
        Attaque spéciale de luffy
        """
        for element in self.game.players:
            if element.game.name[element.number] == "luffy":
                if element.vals["percent_ult"] >= 130:
                    self.game.name[element.number] = 'gear4'
                    element.vals['nbr_sprite'] = 0
                    self.game.elms['side'][element.number] = 'ult'
                    self.game.player_0.vals['strike'] = 30

    def spe_itachi(self):
        """
        Attaque spéciale d'itachi
        """
        victime = None
        for element in self.game.players:
            if self.game.name[element.number] == 'itachi':
                self.game.elms['side'][element.number] = 'ult'
            else:
                victime = element
            victime.vals["strike"] = self.pl1_speed
            victime.vals["health"] -= 50
            print(self.game.player_1.player["hp"])

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
                    element.vals["percent_ult"] = 130
