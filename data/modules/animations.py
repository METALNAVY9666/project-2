"""Ce module gère les animations spéciales, comme les attaques spéciales"""
import pygame as pg
from data.modules.texture_loader import GFX


class Animate():
    """
    Cette classe permet de génerer une image afin de créer une animation
    """

    def __init__(self, spe):
        self.spe = spe
        for element in self.spe.game.players:
            self.vals = {"image": GFX["skill_box"],
                         "face": GFX[self.spe.game.name[element.number]]}
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
        self.rect_update.append(self.txt_blit(screen, width, height))
        pg.display.update(self.rect_update)
        return []

    def txt_blit(self, screen, width, height):
        """Fonction qui permet d'afficher le texte"""
        quotes = {"vegeta": "blabla",
                  "goku": "Ce n'est pas encore terminé...",
                  "luffy": "Le prochain roi des pirates...Ce sera moi !",
                  "itachi": "Toute technique est inutile devant mes yeux.",
                  "revive": "Ce n'est toujours pas fini...",
                  "kim": "Mouais mouais"}
        self.vals["font"] = pg.font.Font(
            'test_olivier/gfx/fonts/04B_19__.TTF', 30)
        for element in self.spe.game.players:
            if element.game.name[element.number] != "kim":
                if element.vals["health"] <= 0:
                    dead = element
                    txt = self.vals["font"].render(
                        quotes[self.spe.game.name[dead.number]],
                        0, (244, 49, 14))
                    txt_width = screen.get_width() - (txt.get_width()) * 2
                    return screen.blit(txt, (txt_width, height))
                if element.game.name[element.number] == "itachi" and (
                        self.spe.can_spe["itachi"] and
                        element.vals["health"] < element.vals["max_health"] // 3):
                    txt = self.vals["font"].render(
                        quotes[element.game.name[element.number]],
                        0, (244, 49, 14))
                    txt_width = screen.get_width() - (txt.get_width()) * 1.5
                    self.animation_itachi(screen)
                    height = screen.get_height() - (screen.get_height() // 5)
                    return screen.blit(txt, (txt_width, height))
                if element.game.name[element.number] == "luffy":
                    txt = self.vals["font"].render(
                        quotes[element.game.name[element.number]],
                        0, (244, 49, 14))
                    txt_width = screen.get_width() - (txt.get_width() * 1.5)
                    return screen.blit(txt, (txt_width, height))

    def animation_itachi(self, screen):
        """
        Animation pour la spé d'itachi"""
        image = GFX["itachi_spe"]
        image_rect = image.get_rect()
        self.rect_update.append(screen.blit(image, image_rect))
