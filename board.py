import numpy as np
from functools import partial

class Board:
  # not bothering with protected attributes rn
  NOT_COMPLETE = 0
  PLAYER_ONE = 1
  PLAYER_TWO = 2
  DRAW = 3
  # stores current winner of this board
  complete = NOT_COMPLETE

  def __init__(self, columns: int, rows: int, recursion_depth: int, num_to_connect: int):
    self.COLUMNS = columns
    self.ROWS = rows

    # number of chips to connect in a row to complete the board
    self.NUM_TO_CONNECT = num_to_connect

    # 2d array of all chips placed, i.e., physical state of board
    self.chips = np.zeros(shape=(columns, rows), dtype=int)

    # 2d array of all sub-boards if they exist
    self.sub_boards = np.empty(shape=(columns, rows), dtype=object)
    if recursion_depth > 1:
      for i in range(columns):
        self.sub_boards.append([Board(columns, rows, recursion_depth - 1, num_to_connect) for j in range(rows)])

  def __repr__(self):
    # number of chips played in this board
    return 'Board ({} of {})'.format(np.count_nonzero(self.chips), self.COLUMNS * self.ROWS)

  def get_chip(self, column: int, row: int) -> int:
    if self.is_in_board(column, row):
      return self.chips[column, row]
    return -1

  def set_chip(self, column: int, row: int, player: bool):
    self.chips[column, row] = self.PLAYER_ONE if player else self.PLAYER_TWO

  def can_play_here(self, column: int) -> bool:
    return self.complete == 0 and self.chips[column, 0] == 0

  def find_lowest_empty_row(self, column: int) -> int:
    for row in range(self.ROWS - 1, -1, -1):
      if self.chips[column, row] == 0:
        return row
    return -1

  # return whether the given location is within board parameters
  def is_in_board(self, column: int, row: int) -> bool:
    return 0 <= column < self.COLUMNS and 0 <= row < self.ROWS

  # return length of unbroken line of given player's chips
  def measure_line(self, start_x: int, start_y: int, player: int, d_x: int, d_y: int) -> int:
    length = 0
    x = start_x
    y = start_y

    while self.is_in_board(x, y) and self.chips[x, y] == player:
      length += 1
      x += d_x
      y += d_y

    return length

  # check whether the previous move connected the required number or the board is full
  # return completion state
  def update_status(self, previous_col: int, previous_row: int):
    player = self.chips[previous_col, previous_row]
    measure_dir = partial(self.measure_line, previous_col, previous_row, player)

    if any([
      measure_dir(0, 1) >= self.NUM_TO_CONNECT,
      measure_dir(1, 0) + measure_dir(-1, 0) - 1 >= self.NUM_TO_CONNECT,
      measure_dir(1, 1) + measure_dir(-1, -1) - 1 >= self.NUM_TO_CONNECT,
      measure_dir(1, -1) + measure_dir(-1, 1) - 1 >= self.NUM_TO_CONNECT,
    ]):
      self.complete = player

    # check for full board
    elif np.all(self.chips):
      self.complete = self.DRAW
