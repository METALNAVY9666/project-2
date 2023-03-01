"""
ce fichier fonctionne un peu comme texture loader.
ignorez la classe Music, vous en n'aurez pas besoin

-- Fichiers
pour ajouter un son, il suffit de le mettre au format mp3 dans le repertoire sfx (vous pouvez aussi
le mettre dans un dossier, faudra juste changer le path)

-- Charger un fichier unique
supposons que vous voulez charger le son feur.mp3, dans le dossier music (sfx/music/)
alors:
SFX["feur"] = load_sound("sfx/music/feur")

-- Charger un repertoire entier
SFX["bro_quotes"] = load_dir("sfx/bro_quotes/")
(attention, le / à la fin est important)

-- Gérer le son
Il suffit d'appeller dans votre script le dictionnaire SFX (exactement comme texture_loader)
Exemple
from data.modules.audio import SFX

SFX["feur"].play()

Pour aller plus loin : https://www.pygame.org/docs/ref/mixer.html#pygame.mixer.Sound
"""
from os import listdir
import pygame
from data.modules.settings import read_settings


class Music:
    """joue de la musique en fonction du type de musique"""

    def __init__(self, pkg, prop):
        self.pkg = pkg
        self.loader = self.pkg["mixer"].music

        self.music = prop["music"]
        self.folder = prop["music_folder"]

        if self.folder:
            self.playlist = listdir(self.music)
            self.loader.load(self.music + self.playlist[0])
        else:
            self.loader.load(self.get_segment("intro"))

        self.reset_volume()

    def get_segment(self, segment):
        """renvoie le segment d'une musique (intro, outro, loop)"""
        return self.music.split(".")[0] + f"_{segment}.mp3"

    def reset_volume(self):
        """change le volume de la musique en fonction des paramètres"""
        settings = read_settings()
        self.loader.set_volume(settings["audio"]["music"] / 100)

    def end(self):
        """joue l'outro"""
        self.loader.load(self.get_segment("outro"))
        self.loader.play()

    def play(self):
        """ Joue l'audio """
        if self.folder:
            for elt in range(1, len(self.playlist)):
                print(self.music + self.playlist[elt])
                self.loader.queue(self.music + self.playlist[elt])
            self.loader.play()
        else:
            self.loader.play()
            self.loader.queue(self.get_segment("loop"), loops=-1)

    def pause(self, condition):
        """Pause ou relance l'audio"""
        if condition:
            self.loader.pause()
        else:
            self.loader.unpause()


pygame.mixer.init()

SFX = {}

volume = read_settings()["audio"]["effects"]


def load_sound(filepath):
    """charge un son"""
    sound = pygame.mixer.Sound(filepath)
    sound.set_volume(volume / 100)
    return sound


def load_dir(dirpath):
    """charge des sons dans un dossier"""
    sounds = {}
    for file in listdir(dirpath):
        filename = file[0:-4]
        filepath = dirpath + file
        sounds[filename] = load_sound(filepath)
    return sounds


SFX_PATH = "data/sfx/"
EFFECTS_PATH = SFX_PATH + "effects/"


folders = ("kim", "level", "events", "ui",
           "goku", "vegeta", "luffy", "itachi", "revive")

for folder in folders:
    SFX[folder] = load_dir(SFX_PATH + folder + "/")

SFX["explosion"] = load_sound(EFFECTS_PATH + "explosion.mp3")
