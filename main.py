import pygame
from pygame import *

from board import Board

DISPLAY_WIDTH = 700
DISPLAY_HEIGHT = 600
WIDTH = 7
HEIGHT = 6

pygame.init()

DISP = display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
display.set_caption("Connect 4 Recursive")

# testing board class
board = Board(WIDTH, HEIGHT, 2)
print(board)
print(board.chips)
print(board.sub_boards)

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False