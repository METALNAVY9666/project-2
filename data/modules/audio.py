"""contient les classes permettant de jouer de la musique"""
from os import listdir


class Music:
    """joue de la musique en fonction du type de musique"""

    def __init__(self, pkg, prop, settings):
        self.pkg = pkg
        self.loader = self.pkg["mixer"].music

        self.music = prop["music"]
        self.folder = prop["music_folder"]

        if self.folder:
            self.playlist = listdir(self.music)
            self.loader.load(self.music+self.playlist[0])
        else:
            self.loader.load(self.get_segment("intro"))

        self.loader.set_volume(settings["audio"]["music"]/100)

    def get_segment(self, segment):
        """renvoie le segment d'une musique (intro, outro, loop)"""
        return self.music.split(".")[0] + f"_{segment}.mp3"

    def play(self):
        if self.folder:
            for elt in range(1, len(self.playlist)):
                print(self.music+self.playlist[elt])
                self.loader.queue(self.music+self.playlist[elt])
            self.loader.play()
        else:
            self.loader.play()
            self.loader.queue(self.get_segment("loop"), loops=-1)

    def pause(self, condition):
        if condition:
            self.loader.pause()
        else:
            self.loader.unpause()
