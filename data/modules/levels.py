"""ce module contient les différents niveaux"""


class BaseLevel:
    """niveau dans une ville futuriste"""
    def __init__(self, pygame_pack, level_prop):
        """mettre pack_pygme en parametres afin de
        pouvoir modifier la scène sans recharger"""
        self.level_prop = level_prop
        self.pkg = pygame_pack

        self.init_ui()
        self.init_audio()

        self.keys = self.pkg["pygame"].key.get_pressed()
        self.pause = False

    def init_ui(self):
        """initialise l'interface grapgique du niveau"""
        loading = self.pkg["pygame"].image.load("data/gfx/ui/loading.png")
        loading = self.pkg["pygame"].transform.scale(loading, self.level_prop["scale"])
        self.quit_button = self.pkg["pygame"].image.load("data/gfx/ui/exit_button.png")
        self.pkg["display"].update(self.pkg["surface"].blit(loading, (0, 0)))
        self.background = self.pkg["pygame"].image.load(self.level_prop["background"])
        self.background = self.pkg["pygame"].transform.scale(self.background, self.level_prop["scale"])

    def init_audio(self):
        """initialise l'audio du niveau"""
        self.bg_music = self.pkg["mixer"].Sound(self.level_prop["music"])
        self.bg_music.play()

    def check_keys(self):
        """vérifie quelles touches sont appuyées"""
        old_keys = self.keys
        self.keys = self.pkg["pygame"].key.get_pressed()

        if self.keys[self.pkg["pygame"].K_ESCAPE] and not old_keys[self.pkg["pygame"].K_ESCAPE]:
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
        update_rect = self.pkg["surface"].blit(self.background, (0, 0))
        self.pkg["display"].update(update_rect)
        return "continue"
