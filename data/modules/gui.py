"""contient les fonctions permettant d'affucher les menus"""
from data.modules.texture_loader import GFX
from data.modules.settings import read_settings


class PauseMenu:
    """menu pause"""

    def __init__(self, pkg):
        self.bool = False
        self.pkg = pkg
        self.bg_music = None
        self.settings = SettingsMenu(pkg)
        dims = pkg["dimensions"]
        self.pos = (dims[0] // 64, dims[1] // 64)

    def switch(self):
        """active ou désactive le menu pause"""
        if self.bool:
            self.pkg["mouse"].set_visible(True)
            self.bg_music.pause(True)
            self.pkg["mixer"].pause()
        else:
            self.pkg["mouse"].set_visible(False)
            self.bg_music.pause(False)
            self.pkg["mixer"].unpause()

    def update(self):
        """met à jour le menu pause"""
        update_l = []
        if self.bool and not self.settings.in_menu:
            mouse = self.pkg["mouse"].get_pressed()[0]
            blit_surface = self.pkg["surface"].blit

            blur_rect = blit_surface(GFX["blur"], (0, 0))
            update_l.append(blur_rect)

            exit_rect = blit_surface(GFX["btn"]["exit"], self.pos)
            update_l.append(exit_rect)

            settings_rect = self.settings.update()
            update_l.append(settings_rect)

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

class SettingsMenu:
    """paramètres"""
    def __init__(self, pkg):
        self.pkg = pkg
        self.in_menu = False
        self.sub_menu = None
        dims = pkg["dimensions"]
        self.pos = (dims[0] // 64, 2 * dims[1] // 64 + dims[1] // 10)

    def check_click(self, rect):
        """vérifie si le le bouton est préssé"""
        mouse_pos = self.pkg["mouse"].get_pos()
        pressed = self.pkg["mouse"].get_pressed()[0]
        if pressed and rect.collidepoint(mouse_pos):
            self.in_menu = True

    def update(self):
        """met à jour le menu paramètres"""
        rects = []
        blit_surface = self.pkg["surface"].blit
        if self.in_menu:
            delta = 0
            space = 2 * dims[1] // 64 + dims[1] // 10
            dims = self.pkg["dimensions"]
            for button in ["audio", "screen", "keyboard", "cancel"]:
                texture = GFX["btn"][button]
                pos = self.pos * 1
                pos[1] += delta
                rect = blit_surface(texture, pos)
                delta += space
        rect = blit_surface(GFX["btn"]["settings"], self.pos)
        self.check_click(rect)
        rects.append(rect)
        return rect