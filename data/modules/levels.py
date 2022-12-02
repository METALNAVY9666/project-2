"""ce module contient les différents niveaux"""
import os
from data.modules.texture_loader import GFX

class TestPlayer:
    """créée un joueur test"""
    def __init__(self, iden, pkg):
        self.iden = iden
        self.pkg = pkg
        self.pos = [0, 0]
        self.dt = 1
        self.velocity = 1
        pg = pkg["pygame"]
        self.player_texture = GFX["players"]["nyan"]
        self.controls = [
            [pg.K_LEFT, pg.K_UP, pg.K_RIGHT, pg.K_DOWN],
            [pg.K_q, pg.K_z, pg.K_d, pg.K_s]
        ]
    
    def move(self):
        """bouge le joueur"""
        keys = self.pkg["pygame"].key.get_pressed()
        controls = self.controls[self.iden]
        speed = self.dt * self.velocity * 0.01
        if keys[controls[0]]:
            self.pos[0] -= 5 * speed
        if keys[controls[1]]:
            self.pos[1] -= 5 * speed
        if keys[controls[2]]:
            self.pos[0] += 5 * speed
        if keys[controls[3]]:
            self.pos[1] += 5 * speed
        rect = self.pkg["surface"].blit(self.player_texture, self.pos)
        return rect

    def update(self, dt, pause):
        """met à jour le joueur"""
        self.dt = dt
        if pause:
            self.velocity = 0
        else:
            self.velocity = 20
        return self.move()

class Background:
    """créée un fond qui s'adapte à la position des 2 joueurs"""
    def __init__(self, pkg, prop):
        self.pkg = pkg
        self.prop = prop
        self.bg = GFX[self.prop["bg"]]["bg"]

    def update(self, player_rects):
        """met à jour la position du fond en fonction de
        la position des joueurs"""
        screen = self.prop["scale"]
        pos = [player_rects[0].center, player_rects[1].center]
        if pos[0][0] + screen[0]//4 < pos[1][0]:
            print("1 à gauche")
            os.system("clear")
        bg_rect = self.pkg["surface"].blit(self.bg, (0, 0))
        return bg_rect
    
class BaseLevel:
    """générateur de niveaux"""
    def __init__(self, pygame_pack, level_prop, game_settings):
        """mettre pack_pygame, les propriétés du niveau et les paramètres
        du jeu en parametres afin de pouvoir modifier la scène sans recharger
        """
        self.pause = False
        self.update_list = []
        self.keys = {}
        self.dt = 0
        self.init_prop(pygame_pack, level_prop, game_settings)
        self.init_ui()
        self.init_audio()
        self.init_players()

    def init_players(self):
        """initialise les joueurs"""
        self.player0 = TestPlayer(0, self.pkg)
        self.player1 = TestPlayer(1, self.pkg)
        payload0 = self.player0.update(1, self.pause)
        payload1 = self.player1.update(1, self.pause)
        self.player_rects = [payload0, payload1]

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
        self.background = Background(self.pkg, self.level_prop)

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

        self.update_list.append(self.background.update(self.player_rects))

        self.player_rects = [None, None]
        self.player_rects[0] = self.player0.update(self.dt, self.pause)
        self.player_rects[1] = self.player1.update(self.dt, self.pause)
        self.update_list.append(self.player_rects[0])
        self.update_list.append(self.player_rects[1])

        next_op = self.pause_menu_update()
        
        self.update_list.reverse()
        self.pkg["display"].update(self.update_list)
        self.update_list = []
        # print("FPS : ", int(self.pkg["clock"].get_fps()))
        return next_op
