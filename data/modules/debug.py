"""contient toutes les fonctions permettant de déboguer le jeu"""
from math import floor


class FPS:
    """crée un objet permettant de stocker les fps et des les analyser"""
    def __init__(self, pkg):
        self.record = 0
        self.record_n = 0
        self.pkg = pkg

    def get_fps(self):
        """renvoie le nombre de fps à l'instant t"""
        return self.pkg["clock"].get_fps()

    def record_fps(self):
        """enregistre le fps actuel"""
        self.record += self.get_fps()
        self.record_n += 1

    def end(self):
        """renvoie la moyenne de l'enregistrement des fps"""
        return floor(self.record / self.record_n)


def print_fps(pkg):
    """affiche les fps dans la console"""
    print("FPS : ", int(pkg["clock"].get_fps()))
