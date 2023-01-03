"""contient les joueurs"""
from data.modules.texture_loader import GFX


class TestPlayer:
    """créée un joueur test"""
    def __init__(self, iden, pkg):
        self.delta = 1
        self.pkg = pkg
        self.player_pos = []
        self.velocity = 1
        self.dims = pkg["dimensions"]
        self.clamps = [[None]*2]*2
        for axis in [0, 1]:
            self.player_pos.append(self.dims[axis]//2 - 50)
        pyg = pkg["pygame"]
        self.controls = [
            [[pyg.K_LEFT, pyg.K_RIGHT], [pyg.K_UP, pyg.K_DOWN]],
            [[pyg.K_q, pyg.K_d], [pyg.K_z, pyg.K_s]]
        ]
        self.controls = self.controls[iden]

    def check_zone(self):
        """vérifie si le joueur peut faire bouger le fond"""
        left = self.player_pos[0] < self.dims[0]//3
        right = self.player_pos[0] > 2*self.dims[0]//3
        top = self.player_pos[1] < self.dims[1]//3
        bottom = self.player_pos[1] > 2*self.dims[1]//3
        return left, right, top, bottom

    def move(self, pos):
        """bouge le joueur en fonction du fond"""
        keys = self.pkg["pygame"].key.get_pressed()
        controls = self.controls
        speed = self.delta * self.velocity * 0.01

        if self.clamps is not None:
            for axis in [0, 1]:
                if self.clamps[axis][0] or self.clamps[axis][1]:
                    if keys[controls[axis][0]]:
                        self.player_pos[axis] -= 5 * speed
                    if keys[controls[axis][1]]:
                        self.player_pos[axis] += 5 * speed

        for axis in [0, 1]:
            temp_max = 2*self.dims[axis]//3
            if self.dims[axis]//3 < self.player_pos[axis] < temp_max:
                if keys[controls[axis][0]]:
                    pos[axis] += 5 * speed
                if keys[controls[axis][1]]:
                    pos[axis] -= 5 * speed

        bliting = (GFX["players"]["nyan"], self.player_pos)
        player_rect = self.pkg["surface"].blit(bliting[0], bliting[1])
        return pos, player_rect

    def update(self, delta, pause, pos):
        """met à jour le joueur"""
        self.delta = delta
        if pause:
            self.velocity = 0
        else:
            self.velocity = 20
        return self.move(pos)
