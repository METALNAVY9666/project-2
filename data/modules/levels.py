"""ce module contient les différents niveaux"""


class BaseLevel:
    """générateur de niveaux"""
    def __init__(self, pygame_pack, level_prop):
        """mettre pack_pygme en parametres afin de
        pouvoir modifier la scène sans recharger"""
        self.level_prop = level_prop
        self.pkg = pygame_pack

        self.init_ui()
        self.init_audio()

        self.keys = {}
        self.keys["new"] = self.pkg["pygame"].key.get_pressed()
        self.pause = False

    def init_ui(self):
        """initialise l'interface grapgique du niveau"""
        ui_path = "data/gfx/ui/"
        loading = self.pkg["pygame"].image.load(ui_path+"loading.png")
        loading_scale = self.level_prop["scale"]
        loading = self.pkg["pygame"].transform.scale(loading, loading_scale)
        self.quit_btn = self.pkg["pygame"].image.load(ui_path+"exit_btn.png")
        self.pkg["display"].update(self.pkg["surface"].blit(loading, (0, 0)))
        self.bckg = self.pkg["pygame"].image.load(self.level_prop["bg"])
        bg_scale = self.level_prop["scale"]
        self.bckg = self.pkg["pygame"].transform.scale(self.bckg, bg_scale)

    def init_audio(self):
        """initialise l'audio du niveau"""
        self.bg_music = self.pkg["mixer"].Sound(self.level_prop["music"])
        self.bg_music.play()

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
                print("jeu")
            else:
                self.pause = True
                print("pause")

    def update(self):
        """met à jour le niveau, renvoie si le niveau est terminé ou
        non, et le score"""
        self.check_keys()
        update_rect = self.pkg["surface"].blit(self.bckg, (0, 0))
        self.pkg["display"].update(update_rect)
        return "continue"
