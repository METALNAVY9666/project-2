"""ce module contient les différents niveaux"""
from data.modules.texture_loader import GFX
from data.modules.gui import PauseMenu
from data.modules.keyboard import KeyChecker
from data.modules.audio import Music
from data.modules import events
from data.modules.game import Jeu


class Background:
    """créée un fond qui s'adapte à la position des 2 joueurs"""
    def __init__(self, pkg, prop):
        self.pkg = pkg
        self.prop = prop
        self.pos = [0, 0]
        self.dims = pkg["dimensions"]
        self.scl = self.prop["scale"]
        self.bg = self.scale(GFX[self.prop["bg"]]["bg"], self.dims)

    def scale(self, obj, dims):
        """renvoie une image avec la taille changée"""
        return self.pkg["pygame"].transform.scale(obj, dims)

    def update(self):
        """met à jour le fond"""
        bg_rect = self.pkg["surface"].blit(self.bg, self.pos)
        return bg_rect


class BaseLevel:
    """générateur de niveaux"""
    def __init__(self, pygame_pack, prop, game_settings):
        """mettre pack_pygame, les propriétés du niveau et les paramètres
        du jeu en parametres afin de pouvoir modifier la scène sans recharger
        """
        self.update_list = []
        self.init_prop(pygame_pack, prop, game_settings)
        self.init_ui()
        self.init_audio()
        self.init_game()
        self.init_events()

    def init_prop(self, pygame_pack, prop, game_settings):
        """initlialise les variables et propriétés de la classe BaseLevel"""
        self.prop = prop
        self.pkg = pygame_pack
        self.settings = game_settings

    def init_ui(self):
        """initialise l'interface graphique du niveau"""
        self.cls = {}
        self.pkg["mouse"].set_visible(False)
        self.cls["bg"] = Background(self.pkg, self.prop)
        self.cls["pause"] = PauseMenu(self.pkg)
        self.cls["key"] = KeyChecker(self.pkg, self.cls["pause"])
        self.cls["busy"] = True

    def init_audio(self):
        """initialise l'audio du niveau"""
        bg_music = Music(self.pkg, self.prop, self.settings)
        bg_music.play()
        self.cls["pause"].bg_music = bg_music

    def init_game(self):
        """initialise le jeu"""
        self.cls["game"] = Jeu("goku")

    def init_events(self):
        """initialise les évènements"""
        self.cls["actions"] = self.pkg["pygame"].event.get()
        self.cls["countdown"] = events.Countdown(self.pkg, self.prop)
        self.cls["end"] = events.End(self.pkg, self.prop, self.settings)
        self.cls["events"] = {}
        if "ae86" in self.prop["events"]:
            self.cls["events"]["ae86"] = events.AE86(self.pkg, self.prop, GFX)

    def update_events(self, pause=bool, busy=bool):
        """met à jour les évènements du niveau"""
        keys = list(self.cls["events"].keys())
        rects = []
        for key in keys:
            rect = self.cls["events"][key].update(pause, busy)
            if rect is not None:
                rects.append(rect)
        return rects
    
    def update_countdown(self):
        """met à jour le décompte"""
        ctn = self.cls["countdown"].update(self.cls["pause"].bool)
        if ctn[0] == "ctn":
            number = GFX[ctn[1]]
            width = self.settings["display"]["horizontal"]
            height = self.settings["display"]["vertical"]
            pos = [(width//2)-(width//12), (height//2)-(height//12)] 
            self.update_list.append(self.pkg["surface"].blit(number, pos))
        else:
            if ctn[0] == "end":
                self.cls["busy"] = False
    
    def update_obstacles(self):
        """met à jour la position des obstacles"""
        if self.prop["bg"] == "neo_tokyo":
            surface = self.pkg["surface"]
            width = self.settings["display"]["horizontal"]
            height = self.settings["display"]["vertical"]
            pos = [(width//2)-(width//3), height//1.5] 
            return surface.blit(GFX["platform"], pos)

    def update(self, delta):
        """met à jour le niveau, renvoie si le niveau est terminé ou
        non, et le score"""

        # met à jour les touches
        next_op = None
        keys = [self.pkg["pygame"].K_ESCAPE]
        self.cls["key"].check_keys(keys)

        # met à jour le fond
        self.update_list.append(self.cls["bg"].update())

        #met à jour le jeu
        surface = self.pkg["surface"]
        game = self.cls["game"].update(surface, delta, self.cls["actions"])
        self.update_list.append(game[0])
        self.update_list.append(self.cls["game"].update_objects(surface))

        # met à jour les obstacles
        # self.update_list.append(self.update_obstacles())

        # met à jour les évènements
        self.update_list += self.update_events(self.cls["pause"].bool,
        self.cls["busy"])
        
        # met à jour le décompte
        self.update_countdown()

        # màj l'état des personnages
        end = self.cls["end"]
        self.update_list.append(end.update(game[1]))
        
        # met à jour le menu pause
        next_op, pause_rects = self.cls["pause"].update()
        if pause_rects is not None:
            for rect in pause_rects:
                self.update_list.append(rect)


        self.pkg["display"].update(self.update_list)
        self.update_list = []
        return next_op
