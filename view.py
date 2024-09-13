from pygame import *
from pyautogui import size as screen_size

from board import Board

from random import randint

class View:
  DEFAULT_CHIP_SIZE = 100  # diameter
  BORDER_PROPORTION = 0.1  # proportion of chip size put between chips

  DARK_BLUE = (20, 0, 75)
  BLUE = (40, 90, 155)
  RED = (170, 30, 30)
  GREEN = (0, 200, 0)
  YELLOW = (230, 210, 40)
  LIGHT_GREY = (100, 100, 100)
  
  COLOUR_MAP = {
    Board.NOT_COMPLETE: BLUE,
    Board.PLAYER_ONE: RED,
    Board.PLAYER_TWO: YELLOW,
    Board.DRAW: LIGHT_GREY,
  }

  def __init__(self, columns: int, rows: int):
    self.COLUMNS = columns
    self.ROWS = rows
    self.CHIP_SIZE = self.chip_size(columns, rows)
    self.CHIP_WITH_BORDER_SIZE = self.CHIP_SIZE * (1 + self.BORDER_PROPORTION)
    self.DISPLAY_WIDTH = columns * self.CHIP_WITH_BORDER_SIZE
    self.DISPLAY_HEIGHT = rows * self.CHIP_WITH_BORDER_SIZE
    self.screen = display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))
    display.set_caption("Connect Recursive")
    self.screen.fill(self.DARK_BLUE)

  def chip_size(self, columns: int, rows: int):
    width, height = screen_size()
    width_max_chip_size = (width - 100) // (columns * (1 + self.BORDER_PROPORTION))
    height_max_chip_size = (height - 100) // (rows * (1 + self.BORDER_PROPORTION))
    return min(self.DEFAULT_CHIP_SIZE, width_max_chip_size, height_max_chip_size)

  def render_board(self, board: Board):
    for i in range(self.COLUMNS):
      for j in range(self.ROWS):
        draw.circle(
          self.screen,
          self.COLOUR_MAP[board.get_chip(i, j)],
          ((i + 0.5) * self.CHIP_WITH_BORDER_SIZE, (j + 0.5) * self.CHIP_WITH_BORDER_SIZE),
          self.CHIP_SIZE // 2,
        )
    display.update()

  def update_chip(self, column: int, row: int, player: bool):
    draw.circle(
      self.screen,
      self.COLOUR_MAP[Board.PLAYER_ONE if player else Board.PLAYER_TWO],
      ((column + 0.5) * self.CHIP_WITH_BORDER_SIZE, (row + 0.5) * self.CHIP_WITH_BORDER_SIZE),
      self.CHIP_SIZE // 2,
    )
    display.update()

  def which_column_clicked(self, x: int):
    x -= self.CHIP_SIZE * self.BORDER_PROPORTION // 2
    if x % self.CHIP_WITH_BORDER_SIZE <= self.CHIP_SIZE:
      return int(x // self.CHIP_WITH_BORDER_SIZE)
    return -1
