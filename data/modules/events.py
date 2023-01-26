"""contient la classe permettant de créer des évènements aléatoires"""
from random import randint


class AE86:
    """fait drifter une ae86 sur la map highway, inflige des dégâts"""

    def __init__(self, pkg, prop, GFX):
        self.pkg = pkg
        self.prop = prop
        self.ae86 = {}
        self.ae86["car"] = GFX["ae86"]
        self.lock = False
        self.timer = 0
        dims = self.pkg["dimensions"]
        self.pos = [dims[0]//2, dims[1]//2]

    def check_event(self, n):
        """vérifie si l'évènement se réalise avec 1/n proba par seconde"""
        return randint(0, self.pkg["FPS"] * n) == 0

    def check_timer(self, n):
        """vérifie le timer duh"""
        return self.timer == self.pkg["FPS"] * n

    def update(self, pause=False, busy=False):
        """met à jour l'évènement"""
        if not busy:
            if self.lock:
                if not pause:
                    self.timer += 1
                if self.check_timer(6):
                    self.lock = False
                    print("Wow that was really cool.")
                surface = self.pkg["surface"]
                return surface.blit(self.ae86["car"], self.pos)
            else:
                if self.check_event(20):
                    print("Akina's drift !")
                    self.lock = True
                    self.timer = 0


class Countdown:
    """fait le décompte avant le début du combat"""

    def __init__(self, pkg, prop) -> None:
        self.timer = 0
        self.pkg = pkg
        self.prop = prop
        self.values = []

    def sound(self, file):
        return f"data/sfx/level/{file}.mp3"

    def update(self, pause=False):
        if pause is False:
            self.timer += 1
        clock = self.timer
        fps = self.pkg["FPS"]
        drop = self.prop["drop"]
        counts = [
            [fps * (drop - 3), "three"],
            [fps * (drop - 2), "two"],
            [fps * (drop - 1), "one"],
            [fps * drop, "go"],
            [fps * (drop + 1), "end of countdown"]
        ]
        for ind in range(len(counts)-1):
            if counts[ind][0] == clock:
                self.pkg["mixer"].Sound(self.sound(counts[ind][1])).play()
            if counts[ind][0] < clock < counts[ind+1][0]:
                return "ctn", counts[ind][1]
        if clock > counts[-1][0]:
            return "end", None
        return "idle", None


class End:
    """gère l'état de la partie en fonction des pvs des joueurs"""

    def __init__(self, pkg, prop, settings):
        self.pkg = pkg
        self.prop = prop
        self.settings = settings
        self.players = None
        self.font = pkg["pygame"].font.Font(
            'test_olivier/gfx/fonts/04B_19__.TTF', 60)
        self.lock = True

    def death(self, player):
        """lance la fonction quand un joueur meurt"""
        txt = self.font.render(player + " wins", True, (0, 0, 0))
        width = self.settings["display"]["horizontal"]
        height = self.settings["display"]["vertical"]
        pos = (width//2, height//2)
        pos = txt.get_rect(center=pos)
        if self.lock:
            PATH = f"data/sfx/events/wins/win_{player}.mp3"
            self.pkg["mixer"].Sound(PATH).play()
            self.lock = False
        return self.pkg["surface"].blit(txt, pos)

    def update(self, players):
        """met à jour l'état de la partie"""
        self.players = players
        for i in [0, 1]:
            if players[i][1] <= 0:
                return self.death(players[1-i][0])
