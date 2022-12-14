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
        return randint(0, self.pkg["FPS"] * n)  == 0

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

    def sound(self,file):
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