"""ce module contient les différents niveaux"""
from data.modules.texture_loader import GFX


class BaseLevel:
    """générateur de niveaux"""
    def __init__(self, pygame_pack, level_prop, game_settings):
        """mettre pack_pygame, les propriétés du niveau et les paramètres
        du jeu en parametres afin de pouvoir modifier la scène sans recharger
        """
        self.pause = False
        self.update_list = []
        self.keys = {}
        self.init_prop(pygame_pack, level_prop, game_settings)
        self.init_ui()
        self.init_audio()

    def init_prop(self, pygame_pack, level_prop, game_settings):
        """initlialise les variables et propriétés de la classe BaseLevel"""
        self.level_prop = level_prop
        self.pkg = pygame_pack
        self.settings = game_settings
        self.keys["new"] = self.pkg["pygame"].key.get_pressed()

    def init_ui(self):
        """initialise l'interface graphique du niveau"""
        self.pkg["mouse"].set_visible(False)
        surface_blit = self.pkg["surface"].blit
        self.pkg["display"].update(surface_blit(GFX["loading"], (0, 0)))

    def init_audio(self):
        """initialise l'audio du niveau"""
        bg_music_path = self.level_prop["music"]
        volume = self.settings["audio"]["music"]/100
        self.pkg["mixer"].music.load(bg_music_path)
        self.pkg["mixer"].music.set_volume(volume)
        self.pkg["mixer"].music.play()

    def check_key(self, key_name):
        """vérifie si la touche est touchée et relâchée"""
        pressed = {}
        pressed["old"] = self.keys["old"][key_name]
        pressed["new"] = self.keys["new"][key_name]
        if not pressed["old"] and pressed["new"]:
            return True
        return False

    def check_keys(self):
        """vérifie quelles touches sont appuyées"""
        self.keys["old"] = self.keys["new"]
        self.keys["new"] = self.pkg["pygame"].key.get_pressed()

        if self.check_key(self.pkg["pygame"].K_ESCAPE):
            if self.pause:
                self.pause = False
            else:
                self.pause = True
            self.pause_menu()

    def pause_menu(self):
        """active ou désactive le menu pause"""
        if self.pause:
            self.pkg["mixer"].music.pause()
            self.pkg["mouse"].set_visible(True)
        else:
            self.pkg["mixer"].music.unpause()
            self.pkg["mouse"].set_visible(False)

    def pause_menu_update(self):
        """met à jour le menu pause"""
        if self.pause:
            mouse = self.pkg["mouse"].get_pressed()[0]
            blit_surface = self.pkg["surface"].blit
            blur_rect = blit_surface(GFX["blur"], (0, 0))
            self.update_list.append(blur_rect)
            exit_rect = blit_surface(GFX["exit"], (20, 20))
            self.update_list.append(exit_rect)
            rects = [["exit", exit_rect]]
            on_button = self.pause_menu_clicks(rects)
            if mouse and on_button is not None:
                return on_button
        return "continue"

    def pause_menu_clicks(self, rects):
        """vérifie les boutons cliqués par la souris"""
        mouse_pos = self.pkg["mouse"].get_pos()
        for rect in rects:
            if rect[1].collidepoint(mouse_pos):
                return rect[0]
        return None

    def update(self):
        """met à jour le niveau, renvoie si le niveau est terminé ou
        non, et le score"""
        next_op = None
        self.check_keys()
        background = GFX[self.level_prop["bg"]]["bg"]
        bg_rect = self.pkg["surface"].blit(background, (0, 0))
        self.update_list.append(bg_rect)
        self.update_list.reverse()
        next_op = self.pause_menu_update()
        self.pkg["display"].update(self.update_list)
        # print("FPS : ", int(self.pkg["clock"].get_fps()))
        self.update_list = []
        return next_op
