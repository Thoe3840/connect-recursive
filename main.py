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

player = True  # player 1: T, player 2: F
running = True
while running:
  for event in pygame.event.get():
    if event.type == QUIT:
      running = False
      break

    elif event.type == MOUSEBUTTONDOWN and event.button == 1:  # left click
      column = view.which_column_clicked(mouse.get_pos()[0])
      if column != -1 and board.can_play_here(column):
        row = board.place_chip(column, player)
        view.update_chip(column, row, player)
        player = not player
        status = board.is_completed(column, row)
