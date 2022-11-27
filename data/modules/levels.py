"""ce module contient les différents niveaux"""


class BaseLevel:
    """niveau dans une ville futuriste"""
    def __init__(self, pygame_pack, level_prop):
        """mettre pack_pygme en parametres afin de
        pouvoir modifier la scène sans recharger"""
        self.level_prop = level_prop
        self.pgpck = pygame_pack

        self.init_ui()
        self.init_audio()

        self.keys = self.pygame.key.get_pressed()
        self.pause = False

    def init_ui(self):
        """initialise l'interface grapgique du niveau"""
        loading = self.pygame.image.load("data/gfx/ui/loading.png")
        loading = self.pygame.transform.scale(loading, self.level_prop["scale"])
        self.quit_button = self.pygame.image.load("data/gfx/ui/exit_button.png")
        self.display.update(self.surface.blit(loading, (0, 0)))
        self.background = self.pygame.image.load(self.level_prop["background"])
        self.background = self.pygame.transform.scale(self.background, self.level_prop["scale"])

    def init_audio(self):
        """initialise l'audio du niveau"""
        self.bg_music = self.pgpck["mixer"].Sound(self.level_prop["music"])
        self.bg_music.play()

    def check_keys(self):
        """vérifie quelles touches sont appuyées"""
        old_keys = self.keys
        self.keys = self.pygame.key.get_pressed()

        if self.keys[self.pygame.K_ESCAPE] and not old_keys[self.pygame.K_ESCAPE]:
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
        update_rect = self.surface.blit(self.background, (0, 0))
        self.display.update(update_rect)
        return "continue"
