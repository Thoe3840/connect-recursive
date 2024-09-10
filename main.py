import pygame
from pygame import *

from board import Board
from view import View

pygame.init()

WIDTH = 7
HEIGHT = 6

board = Board(WIDTH, HEIGHT, 1, 4)
view = View(WIDTH, HEIGHT)
view.render_board(board)

running = True
while running:
  for event in pygame.event.get():
    if event.type == QUIT:
      running = False
      break
