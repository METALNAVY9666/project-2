"""contient les fonctions permettant d'affucher les menus"""
from data.modules.texture_loader import GFX, grayscale
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

    def update(self):
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

            settings_rect = self.settings.update()
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
            "audio" : False,
            "screen": False,
            "keyboard": False,
            "cancel" : False,
            "music" : False,
            "effects": False,
            "horizontal" : False,
            "vertical": False,
            "FPS" : False,
            "fullscreen" : False,
            "keys":[
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
        self.value = None

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

    def update_audio(self):
        """met à jour le menu audio"""
        rects = []

        dims = self.pkg["dimensions"]
        space = dims[1] // 64 + dims[1] // 10
        pos = [dims[0] // 64, dims[1] // 64]

        for button in ["effects", "music"]:
            rect = self.blit(GFX["btn"][button], pos)
            pos[1] += space
            args = ["audio", button, 0, 100]
            old = self.old_pressed_buttons[button]
            self.old_pressed_buttons[button] = check(self.pkg, rect, old, self.askint, args)
        return rects

    def update_screen(self):
        """met à jour le menu écran"""
        rects = []

        dims = self.pkg["dimensions"]
        space = dims[1] // 64 + dims[1] // 10
        pos = [dims[0] // 64, dims[1] // 64]

        for button in ["horizontal", "vertical", "FPS", "fullscreen"]:
            rect = self.blit(GFX["btn"][button], pos)
            pos[1] += space
            func = self.askint
            match button:
                case "horizontal":
                    args = ["display", button, 480, 7680]
                case "vertical":
                    args = ["display", button, 360, 4320]
                case "FPS":
                    args = ["display", button, 0, 300000]
                case "fullscreen":
                    args = ["display", button]
                    func = self.askbool
            old = self.old_pressed_buttons[button]
            self.old_pressed_buttons[button] = check(self.pkg, rect, old, func, args)
        return rects

    def resize(self, img, size):
        """renvoie une image redimensionnée"""
        return self.pkg["transform"].scale(img, size)

    def change_key(self, player, key):
        """change la touche appuyée"""
        SFX["ui"]["click"].play()
        dims = self.pkg["dimensions"] * 1
        texture = GFX["paladins"].render("Appuyez sur une touche", True, (0, 0, 0))
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
            texture = GFX["paladins"].render(f"Joueur {player_ind+1}", True, (0, 0, 0))
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
        return rects

    def askint(self, category, setting, mini, maxi):
        """modifie le paramètre demandé"""
        def yes():
            """modifie les paramètres"""
            settings = read_settings()
            value = entry.get()
            try:
                value = int(value)
                if mini <= value <= maxi:
                    settings[category][setting] = value
                    write_settings(settings)
                    root.destroy()
                else:
                    label.config(text=f"La valeur n'est pas comprise entre {mini} et {maxi}")
            except ValueError:
                label.config(text="La valeur entrée n'est pas bonne")

        def cancel():
            """ne modifie pas les paramètres"""
            root.destroy()

        SFX["ui"]["click"].play()

        root = Tk()
        root.config(bg="white")
        root.title(setting)

        actual = Label(root, text=f"{setting} : {read_settings()[category][setting]}")
        actual.pack()

        label = Label(root, text=f"Entrer une valeur entre {mini} et {maxi} (inclus)")
        label.pack()

        entry = Entry(root)
        entry.pack()

        yes_btn = Button(root, text="Modifier" ,command=yes)
        yes_btn.pack()

        cancel_btn = Button(root, text="Annuler", command=cancel)
        cancel_btn.pack()

        root.mainloop()

    def askbool(self, category, setting):
        def get_text(boolean):
            """bool vers str"""
            if boolean:
                return "Activé(e)"
            return "Désactivé(e)"

        def get_bool():
            """str vers bool"""
            if switch.cget("text") == "Activé(e)":
                return True
            return False

        def switch_value():
            """switche la valeur du bouton"""
            text = get_text(not get_bool())
            switch.config(text=text)

        def save():
            settings = read_settings()
            settings[category][setting] = get_bool()
            write_settings(settings)
            root.destroy()

        SFX["ui"]["click"].play()

        root = Tk()
        root.config(bg="white")
        root.title(setting)

        temp = get_text(read_settings()[category][setting])
        switch = Button(root, text=temp, command=switch_value)
        switch.pack()

        yes_btn = Button(root, text="Sauvegarder" ,command=save)
        yes_btn.pack()

        root.mainloop()

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

    def update(self):
        """met à jour le menu paramètres"""
        blit_surface = self.pkg["surface"].blit
        if self.in_menu:
            match self.sub_menu:
                case None:
                    rects = self.update_main()
                case "audio":
                    rects = self.update_audio()
                case "screen":
                    rects = self.update_screen()
                case "keyboard":
                    rects = self.update_keyboard()
        else:
            rects = []
            rect = blit_surface(GFX["btn"]["settings"], self.pos)
            self.check_click(rect)
            rects.append(rect)
        return rects
