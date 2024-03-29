"""contient la classe permettant de créer des évènements aléatoires"""
from random import randint
from data.modules.audio import SFX
from data.modules.texture_loader import GFX


class AE86:
    """fait drifter une ae86 sur la map highway, inflige des dégâts"""

    def __init__(self, pkg, prop, graphics):
        self.pkg = pkg
        self.prop = prop
        self.ae86 = {}
        self.ae86["car"] = graphics["ae86"]
        self.lock = False
        self.timer = 0
        dims = self.pkg["dimensions"]
        self.pos = [dims[0] // 2, dims[1] // 2]

    def check_event(self, natural):
        """vérifie si l'évènement se réalise avec 1/n proba par seconde"""
        return randint(0, self.pkg["FPS"] * natural) == 0

    def check_timer(self, natural):
        """vérifie le timer duh"""
        return self.timer == self.pkg["FPS"] * natural

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

            if self.check_event(20):
                print("Akina's drift !")
                self.lock = True
                self.timer = 0
        return None


class Countdown:
    """fait le décompte avant le début du combat"""

    def __init__(self, pkg, prop) -> None:
        self.timer = 0
        self.pkg = pkg
        self.prop = prop
        self.values = []

    def sound(self, file):
        """Charge le son"""
        return f"data/sfx/level/{file}.mp3"

    def update(self, pause=False):
        """Met à jour le son"""
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
        for ind in range(len(counts) - 1):
            if counts[ind][0] == clock:
                sound = counts[ind][1]
                SFX["level"][sound].play()
            if counts[ind][0] < clock < counts[ind + 1][0]:
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
        self.lock = True
        self.delta_sum = 0
        self.fade = FadeOut(pkg)

    def death(self, player, music, delta):
        """lance la fonction quand un joueur meurt"""
        if self.delta_sum <= self.prop["outro"] * 1000:
            player_name = type(player).__name__
            if player_name == "Fighter":
                name = player.vals["name"]
            elif player_name == "Gunner":
                name = player.player["name"]

            txt = GFX["paladins"].render(name + " wins", True, (0, 0, 0))
            width = self.settings["display"]["horizontal"]
            height = self.settings["display"]["vertical"]
            pos = (width // 2, height // 2)
            pos = txt.get_rect(center=pos)
            self.delta_sum += delta
            if self.lock:
                music.end()
                # SFX["events"][f"win_{name}"].play()
                self.lock = False
            return self.pkg["surface"].blit(txt, pos), None

        reponse = self.fade.update()
        return None, reponse

    def update(self, players, music, delta):
        """met à jour l'état de la partie"""
        self.players = players
        for ind in range(len(self.players)):
            player_name = type(self.players[ind]).__name__
            if player_name == "Fighter":
                health_point = self.players[ind].update_pv()[0][1]
            elif player_name == "Gunner":
                health_point = self.players[ind].player["hp"]
            if health_point <= 0:
                return self.death(self.players[1 - ind], music, delta)
        return None


class FadeOut:
    """fondu en fermeture"""
    def __init__(self, pkg):
        self.pkg = pkg
        self.alpha = 0
        self.init_image()

    def init_image(self):
        """initialise le fond noir"""
        dimensions = self.pkg["dimensions"]
        surface = self.pkg["pygame"].Surface
        self.image = surface(dimensions)
        self.image.convert()
        self.image.fill((0, 0, 0))

    def display(self):
        """affiche le fond noir"""
        self.image.set_alpha(self.alpha)
        surface = self.pkg["surface"]
        display = self.pkg["display"]
        rect = surface.blit(self.image, (0, 0))
        display.update(rect)

    def update(self):
        """Met à jour l'alpha de l'outro"""
        if self.alpha <= 255:
            self.display()
            self.alpha += 1
            return None
        return "exit"
