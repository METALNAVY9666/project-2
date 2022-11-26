"""this module contains a music test"""
class NeoTokyo:

    def __init__(self, pygame_pack):
        """mettre pack_pygme en parametres afin de pouvoir modifier la scène sans recharger"""
        self.game_objects = pygame_pack
        pygame = self.game_objects["pygame"]
        self.background = pygame.image.load("data/gfx/levels/neo_tokyo.png")
        self.PAUSE = False

    def update(self):
        """met à jour le niveau, renvoie si le niveau est terminé ou non, et le score"""
        surface = self.game_objects["surface"]
        display = self.game_objects["display"]
        update_rect = surface.blit(self.background, (0, 0))
        display.update(update_rect)
        return "continue"