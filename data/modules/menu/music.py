"""Contient une fonction de musique de menu."""
from data.modules.settings import read_settings


class Music:
    """joue de la musique en fonction du type de musique de manière plus simple"""

    def __init__(self, mixer, music):
        self.loader = mixer.music

        filepath = self.get_file_path("music", music)
        self.loader.load(filepath)

        self.init_settings()

    def init_settings(self):
        """initialise les paramètres"""
        settings = read_settings()
        self.loader.set_volume(settings["audio"]["music"] / 100)

    def get_file_path(self, category, music):
        """renvoie le chemin du fichier"""
        return f"data/sfx/{category}/{music}.mp3"

    def play(self):
        """ Joue l'audio """
        self.loader.play()

    def stop(self):
        """équivoque hein"""
        self.loader.stop()
