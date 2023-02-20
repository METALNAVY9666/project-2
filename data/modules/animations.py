"""Ce module gère les animations spéciales, comme les attaques spéciales"""
import pygame as pg
from data.modules.texture_loader import GFX


class Animate():
    """
    Cette classe permet de génerer une image afin de créer une animation
    """

    def __init__(self, spe):
        self.spe = spe
        self.vals = {"image": GFX["stats_box"],
                     "face": GFX[self.spe.game.name]}
        self.vals["rect"] = self.vals["image"].get_rect()
        self.vals["rect"].x = 0
        self.vals["rect"].y = 0
        self.rect_update = []

    def fade(self, width, height, screen):
        '''Cette fonction a pour but de faire une transition.
        On crée une seconde surface par dessus l'écran,
        que l'on assombri de plus en plus.'''
        pg.time.delay(300)
        # Création de la surface servant à faire le fondu au noir
        fade = pg.Surface((width, height))
        fade.fill((0, 0, 0))
        for i in range(0, 100):
            fade.set_alpha(i)
            self.rect_update = self.append_update(screen, fade)
            # Attente de 3 ms avant de lancer le fondu
            pg.time.delay(30)

    def append_update(self, screen, fade):
        """Ajout des choses à mettre à jour dans une liste"""
        width = screen.get_width() - (self.vals["image"].get_width() * 2)
        height = screen.get_height() // 2
        self.rect_update.append(screen.blit(fade, (0, 0)))
        self.rect_update.append(screen.blit(
            self.vals["image"], (width, height)))
        self.rect_update.append(screen.blit(
            self.vals["face"], (width+50, height+40)))
        pg.display.update(self.rect_update)
        return []
