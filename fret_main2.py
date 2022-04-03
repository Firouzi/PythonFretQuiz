import pygame
pygame.init()
pygame.font.init()

from FretGame import FretGame
import os

### SETUP ###
os.environ['SDL_VIDEO_WINDOW_POS'] = str("800") + "," + str("30")
flags = pygame.DOUBLEBUF | pygame.HWSURFACE
screen = pygame.display.set_mode((1100, 1500), flags)
CLOCK = pygame.time.Clock()
DONE = False
GAME_FPS = 60


fretgame = FretGame(screen)
fretgame.initialize()

QUIT = False
while not QUIT:
    keysdown=pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            QUIT = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            fretgame.receiveClick(pygame.mouse.get_pos())
        if event.type == pygame.KEYDOWN:
            fretgame.receiveKeydown(event.key, keysdown)
    fretgame.render()
    pygame.display.update()
    CLOCK.tick(GAME_FPS)  # 60 FPS