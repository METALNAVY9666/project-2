"""this module contains a music test"""
class NeoTokyo:

    def __init__(self, pygame_pack):
        """mettre pack_pygme en parametres afin de pouvoir modifier la scène sans recharger"""
        self.game_objects = pygame_pack
        self.PAUSE = False

    def update(self):
        """met à jour le niveau, renvoie si le niveau est terminé ou non, et le score"""
        ...