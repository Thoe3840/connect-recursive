import pygame
from pygame import *

DISPLAY_WIDTH = 700
DISPLAY_HEIGHT = 600

pygame.init()

DISP = display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
display.set_caption("Connect 4 Recursive")

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False