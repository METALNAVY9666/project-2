"""contient le décompte avant le début du combat"""


class Countdown:
    """fait le décompte avant le début"""
    def __init__(self, pkg) -> None:
        self.timer = 0
        self.pkg = pkg

    def update(self):
        clock = self.timer
        fps = self.pkg["FPS"]
        if clock < 5 * fps:
            clock += 1
            if clock == 0:
                print("3")
            elif clock == fps:
                print("2")
            elif clock == 2 * fps:
                print("1")
            elif clock == 3 * fps:
                print("GO")