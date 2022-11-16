"""this module contains a music test class"""
import sys
import pygame

clock = pygame.time

mixeur = pygame.mixer
mixeur.init()

game_music = mixeur.Sound("../sfx/music/fire_level_music.mp3")
game_music.play(loops=-1)

#waits 3 seconds
clock.delay(3000)

#fades the music out in 2 seconds
game_music.fadeout(2000)

input()
sys.exit()
