"""contient les fonctions permettant d'afficher les menus"""
from data.modules.texture_loader import GFX
from data.modules.audio import SFX
from data.modules.settings import read_settings, write_settings
from tkinter import Tk, Button, Entry, Label
import keyboard

traductions = {
    "jump": "Sauter",
            "block": "Bloquer",
            "left": "Reculer",
            "right": "Avancer",
            "l_attack": "Attaque Legere",
            "h_attack": "Attaque Lourde"
}


def check(pkg, rect, old_click, onclick, args):
    """vérifie si le bouton est préssé"""
    mouse_pos = pkg["mouse"].get_pos()
    pressed = pkg["mouse"].get_pressed()[0]
    if rect.collidepoint(mouse_pos):
        if pressed:
            old_click = True
        else:
            if old_click:
                onclick(*args)
                old_click = False
    else:
        if old_click:
            old_click = False
    return old_click


class PauseMenu:
    """menu pause"""

    def __init__(self, pkg):
        self.bool = False
        self.pkg = pkg
        self.bg_music = None
        self.settings = SettingsMenu(pkg)
        dims = pkg["dimensions"]
        self.pos = (dims[0] // 64, dims[1] // 64)
        self.classes = []

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
            self.settings.in_menu = False
            self.settings.sub_menu = None
            self.init_settings()

    def reset_mixer(self, volume, dico=dict):
        """change le volume de chaque Sound d'un dictionnaire récursivement"""
        name = type(dico).__name__
        if name == "dict":
            keys = list(dico.keys())
            for key in keys:
                if type(dico[key]).__name__ == "dict":
                    self.reset_mixer(volume, dico[key])
                else:
                    dico[key].set_volume(volume)
        else:
            dico[key].set_volume(volume)

    def init_settings(self):
        """réinitialise les paramètres du jeu"""
        effects_volume = read_settings()["audio"]["effects"] / 100
        self.reset_mixer(effects_volume, SFX)
        for classe in self.classes:
            class_name = type(classe).__name__
            match class_name:
                case "Jeu":
                    classe.reset_player_settings()
                case "PauseMenu":
                    classe.bg_music.reset_volume()

    def update(self, events):
        """met à jour le menu pause"""
        update_l = []
        if self.bool:
            pressed = self.pkg["mouse"].get_pressed()[0]
            blit_surface = self.pkg["surface"].blit

            blur_rect = blit_surface(GFX["blur"], (0, 0))
            update_l.append(blur_rect)

            rects = []

            if not self.settings.in_menu:
                exit_rect = blit_surface(GFX["btn"]["exit"], self.pos)
                update_l.append(exit_rect)
                rects = [["exit", exit_rect]]

            settings_rect = self.settings.update(events)
            update_l.append(settings_rect)

            on_button = self.menu_clicks(rects)
            if pressed and on_button is not None:
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
        self.old_pressed = False
        self.old_pressed_buttons = {
            "audio": False,
            "screen": False,
            "keyboard": False,
            "cancel": False,
            "return": False,
            "music": False,
            "effects": False,
            "horizontal": False,
            "vertical": False,
            "FPS": False,
            "fullscreen": False,
            "keys": [
                {
                    "jump": False,
                    "block": False,
                    "left": False,
                    "right": False,
                    "l_attack": False,
                    "h_attack": False
                },
                {
                    "jump": False,
                    "block": False,
                    "left": False,
                    "right": False,
                    "l_attack": False,
                    "h_attack": False
                }]
        }
        dims = pkg["dimensions"]
        self.pos = (dims[0] // 64, 2 * dims[1] // 64 + dims[1] // 10)
        self.asks = {}
        settings = read_settings()
        self.asks["effects"] = IntInput(pkg, settings, [0, 100], ["audio", "effects"])
        self.asks["music"] = IntInput(pkg, settings, [0, 100], ["audio", "music"])
        self.asks["horizontal"] = IntInput(pkg, settings, [640, 7680], ["display", "horizontal"])
        self.asks["vertical"] = IntInput(pkg, settings, [480, 4320], ["display", "vertical"])
        self.asks["FPS"] = IntInput(pkg, settings, [1, 1000], ["display", "FPS"])

    def check_click(self, rect):
        """vérifie si le le bouton paramètres est préssé"""
        mouse_pos = self.pkg["mouse"].get_pos()
        pressed = self.pkg["mouse"].get_pressed()[0]
        if rect.collidepoint(mouse_pos):
            if pressed:
                self.old_pressed = True
            else:
                if self.old_pressed:
                    self.in_menu = True
                    SFX["ui"]["click"].play()
                    self.old_pressed = False
        else:
            if self.old_pressed:
                self.old_pressed = False

    def check_button(self, rect, name):
        """vérifie si le bouton de sous menu est préssé"""
        mouse_pos = self.pkg["mouse"].get_pos()
        pressed = self.pkg["mouse"].get_pressed()[0]
        if rect.collidepoint(mouse_pos):
            if pressed:
                self.old_pressed_buttons[name] = True
            else:
                if self.old_pressed_buttons[name]:
                    self.sub_menu = name
                    SFX["ui"]["click"].play()
                    self.button_action(name)
                    self.old_pressed_buttons[name] = False
        else:
            if self.old_pressed_buttons[name]:
                self.old_pressed_buttons[name] = False

    def button_action(self, name):
        """Permet de gérer les directions du menu audio."""
        match name:
            case "cancel":
                self.cancel()
            case "audio":
                self.sub_menu = "audio"

    def cancel(self):
        """retrourne au menu pause"""
        self.in_menu = False
        self.sub_menu = None

    def blit(self, image, pos):
        """blite (si si jte jure)"""
        return self.pkg["surface"].blit(image, pos)

    def goback(self):
        """retroune au menu principal"""
        SFX["ui"]["click"].play()
        self.sub_menu = None

    def update_settings(self, domain, subdomain, value):
        """reset les paramètres avec les nouvelles, valeurs"""
        if value is None:
            return
        dico = read_settings()
        dico[domain][subdomain] = value
        write_settings(dico)

    def update_audio(self, events):
        """met à jour le menu audio"""
        rects = []

        dims = self.pkg["dimensions"]
        space = dims[1] // 64 + dims[1] // 10
        pos = [dims[0] // 64, dims[1] // 64]

        for button in ["effects", "music"]:
            rect = self.blit(GFX["btn"][button], pos)
            self.asks[button].pos = [pos[0] + dims[0] // 8, pos[1]]
            pos[1] += space
            old = self.old_pressed_buttons[button]
            func = self.asks[button].switch_active
            self.old_pressed_buttons[button] = check(self.pkg, rect, old, func, [])
            rect, value = self.asks[button].update(events)
            rects.append(rect)
            self.update_settings("audio", button, value)

        rect = self.blit(GFX["btn"]["return"], pos)
        old = self.old_pressed_buttons["return"]
        self.old_pressed_buttons["return"] = check(self.pkg, rect, old, self.goback, [])

        return rects

    def update_screen(self, events):
        """met à jour le menu écran"""
        rects = []

        dims = self.pkg["dimensions"]
        space = dims[1] // 64 + dims[1] // 10
        pos = [dims[0] // 64, dims[1] // 64]

        for button in ["horizontal", "vertical", "FPS"]:
            rect = self.blit(GFX["btn"][button], pos)
            self.asks[button].pos = [pos[0] + dims[0] // 8, pos[1]]
            pos[1] += space
            func = self.asks[button].switch_active
            old = self.old_pressed_buttons[button]
            self.old_pressed_buttons[button] = check(self.pkg, rect, old, func, [])
            rect, value = self.asks[button].update(events)
            rects.append(rect)
            self.update_settings("display", button, value)

        rect = self.blit(GFX["btn"]["return"], pos)
        old = self.old_pressed_buttons["return"]
        self.old_pressed_buttons["return"] = check(self.pkg, rect, old, self.goback, [])

        return rects

    def resize(self, img, size):
        """renvoie une image redimensionnée"""
        return self.pkg["transform"].scale(img, size)

    def change_key(self, player, key):
        """change la touche appuyée"""
        SFX["ui"]["click"].play()
        dims = self.pkg["dimensions"] * 1
        texture = GFX["paladins"].render(
            "Appuyez sur une touche", True, (0, 0, 0))
        size = [dims[0] // 2, dims[1] // 5]
        texture = self.resize(texture, size)
        rect = texture.get_rect()
        pos = list(rect.center)
        pos[0] += dims[0] // 5
        pos[1] += dims[1] // 3
        rect = self.blit(texture, pos)
        self.pkg["display"].update(rect)

        new_key = keyboard.read_key()
        settings = read_settings()
        try:
            if int(new_key) in range(10):
                new_key = "kp_" + new_key
        except ValueError:
            pass
        try:
            settings["keys"][player][key] = settings["trad"][new_key]
        except KeyError:
            settings["keys"][player][key] = new_key
        write_settings(settings)

    def update_keyboard(self):
        """met à jour le sous-menu clavier"""
        rects = []

        dims = self.pkg["dimensions"]
        space = dims[1] // 64 + dims[1] // 10
        pos = [dims[0] // 64, dims[1] // 64]
        size = (dims[0] // 10, dims[1] // 32)

        settings = read_settings()

        player_ind = 0
        for player in settings["keys"]:
            texture = GFX["paladins"].render(
                f"Joueur {player_ind+1}", True, (37, 150, 190))
            texture = self.resize(texture, (dims[0] // 5, dims[1] // 10))
            temp_pos = pos * 1
            rects.append(self.blit(texture, temp_pos))
            pos[1] += space
            for key in list(player.keys()):
                subrects = []
                button_rect = self.blit(GFX["btn"]["key"], pos)
                old = self.old_pressed_buttons["keys"][player_ind][key]
                args = [player_ind, key]
                func = self.change_key
                old = check(self.pkg, button_rect, old, func, args)
                self.old_pressed_buttons["keys"][player_ind][key] = old
                subrects.append(button_rect)
                new_pos = pos * 1
                for ind in (0, 1):
                    new_pos[ind] += dims[ind] // 96
                temp = settings["keys"][player_ind][key]
                text = f"{traductions[key]} : {temp}"
                texture = GFX["paladins"].render(text, True, (0, 0, 0))
                texture = self.resize(texture, size)
                new_pos[1] += dims[1] // 34
                subrects.append(self.blit(texture, new_pos))
                pos[1] += space
                for rect in subrects:
                    rects.append(rect)
            pos = [dims[0] // 64, dims[1] // 64]
            pos[0] += dims[0] // 4
            player_ind += 1
        pos[0] += dims[0] // 4
        rect = self.blit(GFX["btn"]["return"], pos)
        old = self.old_pressed_buttons["return"]
        self.old_pressed_buttons["return"] = check(
            self.pkg, rect, old, self.goback, [])

        return rects

    def update_main(self):
        """met à jour le menu principal des paramètres"""
        rects = []
        blit_surface = self.pkg["surface"].blit
        dims = self.pkg["dimensions"]
        space = dims[1] // 64 + dims[1] // 10
        pos = [dims[0] // 64, dims[1] // 64]
        for button in ["audio", "screen", "keyboard", "cancel"]:
            texture = GFX["btn"][button]
            rect = blit_surface(texture, pos)
            self.check_button(rect, button)
            pos[1] += space
            rects.append(rect)
        return rects

    def update(self, events):
        """met à jour le menu paramètres"""
        blit_surface = self.pkg["surface"].blit
        if self.in_menu:
            match self.sub_menu:
                case None:
                    rects = self.update_main()
                case "audio":
                    rects = self.update_audio(events)
                case "screen":
                    rects = self.update_screen(events)
                case "keyboard":
                    rects = self.update_keyboard()
        else:
            rects = []
            rect = blit_surface(GFX["btn"]["settings"], self.pos)
            self.check_click(rect)
            rects.append(rect)
        return rects


class IntInput:
    """récupère l'entrée clavier"""

    def __init__(self, pkg, settings, extremums, path):
        self.pkg = pkg
        self.settings = settings
        self.active = False
        self.string = str(settings[path[0]][path[1]])
        self.extremums = extremums
        self.pos = [0, 0]

    def switch_active(self):
        """active ou désactive l'entrée"""
        if self.active:
            self.active = False
        else:
            self.active = True

    def return_int(self):
        """renvoie la valeur en int"""
        value = int(self.string)
        extremums = self.extremums
        if value < extremums[0]:
            return extremums[0]
        elif value > extremums[1]:
            return extremums[1]
        return value

    def show_value(self):
        """affiche la valeur à l'écran"""
        blit = self.pkg["surface"].blit
        display_settings = self.settings["display"]
        width, height = display_settings["horizontal"], display_settings["vertical"]
        string = "Valeur : " + self.string + " ('Entrée' pour confirmer)"
        image = GFX["small_paladins"].render(string, True, (255, 255, 255))
        return blit(image, self.pos)

    def add_letter(self, letter):
        """ajoute une lettre à la string"""
        zero_to_nine = [str(num) for num in range(10)]
        if letter in zero_to_nine:
            self.string += letter

    def check_keys(self, events):
        """vérifie les pressions de touches"""
        pg = self.pkg["pygame"]
        keydown = pg.KEYDOWN
        backspace = pg.K_BACKSPACE
        enter = pg.K_RETURN
        for event in events:
            if event.type == keydown:
                if event.key == backspace:
                    if len(self.string) > 0:
                        self.string = self.string[:-1]
                elif event.key == enter:
                    self.switch_active()
                    return self.return_int()
                else:
                    self.add_letter(event.unicode)

    def update(self, events):
        """met à jour"""
        if self.active:
            return self.show_value(), self.check_keys(events)
        return None, None
