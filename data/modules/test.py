"""this module contains a music test"""
import sys
import pygame

clock = pygame.time

mixeur = pygame.mixer
mixeur.init()

game_music = mixeur.Sound("../sfx/music/fire_level_music.mp3")

#fades the music in in 3 seconds
game_music.play(fade_ms=3000)

#waits 3 seconds
clock.delay(3000)

#fades the music out in 2 seconds
game_music.fadeout(2000)

input()

sys.exit()
