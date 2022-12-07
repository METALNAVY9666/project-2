"""contient les fonctions permettant d'affucher les menus"""
from data.modules.texture_loader import GFX


class PauseMenu:
    """menu pause"""
    def __init__(self, pkg):
        self.bool = False
        self.pkg = pkg
        self.bg_music = None

    def switch(self):
        """active ou désactive le menu pause"""
        if self.bool:
            self.pkg["mouse"].set_visible(True)
            self.bg_music.pause(True)
        else:
            self.pkg["mouse"].set_visible(False)
            self.bg_music.pause(False)

    def update(self):
        """met à jour le menu pause"""
        update_l = []
        if self.bool:
            mouse = self.pkg["mouse"].get_pressed()[0]
            blit_surface = self.pkg["surface"].blit

            blur_rect = blit_surface(GFX["blur"], (0, 0))
            update_l.append(blur_rect)

            exit_rect = blit_surface(GFX["exit"], (20, 20))
            update_l.append(exit_rect)

            rects = [["exit", exit_rect]]

            on_button = self.menu_clicks(rects)
            if mouse and on_button is not None:
                return on_button, update_l
        return "continue", None

    def menu_clicks(self, rects):
        """vérifie les boutons cliqués par la souris"""
        mouse_pos = self.pkg["mouse"].get_pos()
        for rect in rects:
            if rect[1].collidepoint(mouse_pos):
                return rect[0]
        return None
