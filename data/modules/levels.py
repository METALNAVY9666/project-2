"""ce module contient les différents niveaux"""
from data.modules.texture_loader import TEXTURES as GFX


class BaseLevel:
    """générateur de niveaux"""
    def __init__(self, pygame_pack, level_prop, game_settings):
        """mettre pack_pygame, les propriétés du niveau et les paramètres
        du jeu en parametres afin de pouvoir modifier la scène sans recharger
        """
        self.init_prop(pygame_pack, level_prop, game_settings)
        self.init_ui()
        self.init_audio()

        self.keys = {}
        self.keys["new"] = self.pkg["pygame"].key.get_pressed()

    def init_prop(self, pygame_pack, level_prop, game_settings):
        """initlialise les variables et les propriétés de la classe BaseLevel"""
        self.level_prop = level_prop
        self.pkg = pygame_pack
        self.settings = game_settings
        self.pause = False
        self.update_list = []

    def init_ui(self):
        """initialise l'interface graphique du niveau"""
        self.pkg["display"].update(self.pkg["surface"].blit(GFX["loading"], (0, 0)))

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
        else:
            self.pkg["mixer"].music.unpause()

    def pause_menu_update(self):
        """met à jour le menu pause"""
        if self.pause:
            blur_rect = self.pkg["surface"].blit(GFX["blur"], (0, 0))
            self.update_list.append(blur_rect)

    def update(self):
        """met à jour le niveau, renvoie si le niveau est terminé ou
        non, et le score"""
        self.check_keys()
        bg_rect = self.pkg["surface"].blit(GFX[self.level_prop["bg"]]["bg"], (0, 0))
        self.update_list.append(bg_rect)
        self.update_list.reverse()
        self.pause_menu_update()
        self.pkg["display"].update(self.update_list)
        print("FPS : ", int(self.pkg["clock"].get_fps()))
        self.update_list = []
        return "continue"
