"""contient les joueurs"""
from data.modules.texture_loader import GFX


class TestPlayer:
    """créée un joueur test"""
    def __init__(self, iden, pkg):
        self.iden = iden
        self.pkg = pkg
        self.pos = [0, 0]
        self.player_pos = []
        for axe in [0, 1]:
            self.player_pos.append(pkg["dimensions"][axe]//2)
        self.delta = 1
        self.velocity = 1
        pyg = pkg["pygame"]
        self.controls = [
            [pyg.K_LEFT, pyg.K_UP, pyg.K_RIGHT, pyg.K_DOWN],
            [pyg.K_q, pyg.K_z, pyg.K_d, pyg.K_s]
        ]

    def move(self):
        """bouge le joueur"""
        keys = self.pkg["pygame"].key.get_pressed()
        controls = self.controls[self.iden]
        speed = self.delta * self.velocity * 0.01
        if keys[controls[0]]:
            self.pos[0] += 5 * speed
        if keys[controls[1]]:
            self.pos[1] += 5 * speed
        if keys[controls[2]]:
            self.pos[0] -= 5 * speed
        if keys[controls[3]]:
            self.pos[1] -= 5 * speed
        bliting = (GFX["players"]["nyan"], self.player_pos)
        player_rect = self.pkg["surface"].blit(bliting[0], bliting[1])
        return self.pos, player_rect

    def update(self, delta, pause):
        """met à jour le joueur"""
        self.delta = delta
        if pause:
            self.velocity = 0
        else:
            self.velocity = 20
        return self.move()
