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

    def spe_manager(self, screen):
        "Gestion des attaque spéciales"
        self.spe_itachi()
        self.spe_luffy()

    def spe_luffy(self):
        """
        Attaque spéciale de luffy
        """
        if self.game.name == 'luffy':
            if self.game.player_0.vals["percent_ult"] >= 130:
                self.game.name = 'gear4'
                self.game.player_0.vals['nbr_sprite'] = 0
                self.game.elms['side'] = 'ult'
                self.game.player_0.vals['strike'] = 30
        elif self.game.player_0.vals["percent_ult"] <= 0:
            if self.game.name == 'gear4':
                self.game.name = 'luffy'

    def spe_itachi(self):
        """
        Attaque spéciale d'itachi
        """
        if self.game.name == 'itachi':
            self.game.elms['side'] = 'ult'
            self.game.player_1.physics["speed"] = self.pl1_speed
            self.game.player_1.player["hp"] -= 0.01
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
        if self.game.player_0.vals["percent_ult"] >= 130:
            if self.game.name == "goku":
                if self.game.player_0.vals["health"] <= 0:
                    self.game.name = "revive"
                    self.animate.fade(screen.get_width(),
                                      screen.get_height(), screen)
                    #self.game.player_0.rect.y = 200
                    pg.time.wait(1000)
                    self.game.elms["side"] = "transfo"
                    self.game.player_0.vals["health"] = 100
                    self.game.player_0.vals["percent_ult"] = 0
