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

column = -1
player = True  # player 1: T, player 2: F
running = True
while running:
  previous_column = column
  column = view.which_column_selected(mouse.get_pos()[0])

  for event in pygame.event.get():
    if event.type == QUIT:
      running = False
      break

    # left click on column with a space
    elif event.type == MOUSEBUTTONDOWN and event.button == 1 and column != -1 and board.can_play_here(column):
      row = board.find_lowest_empty_row(column)
      board.set_chip(column, row, player)
      view.update_chip(column, row, player)
      player = not player
      board.update_status(column, row)

  # update selected column highlights
  if column != previous_column and board.complete == Board.NOT_COMPLETE:
    if column != -1: view.highlight_selected_columnn(column, board.find_lowest_empty_row(column), True)
    if previous_column != -1: view.highlight_selected_columnn(previous_column, board.find_lowest_empty_row(previous_column), False)
