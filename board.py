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

  def __init__(self, width: int, height: int, recursion_depth: int, num_to_connect: int):
    self.WIDTH = width
    self.HEIGHT = height

    # number of chips to connect in a row to complete the board
    self.NUM_TO_CONNECT = num_to_connect

    # 2d array of all chips placed, i.e., physical state of board
    self.chips = np.zeros(shape=(width, height), dtype=int)

    # 2d array of all sub-boards if they exist
    self.sub_boards = np.empty(shape=(width, height), dtype=object)
    if recursion_depth > 1:
      for i in range(width):
        self.sub_boards.append([Board(width, height, recursion_depth - 1, num_to_connect) for j in range(height)])

  def __repr__(self):
    # number of chips played in this board
    return 'Board ({} of {})'.format(np.count_nonzero(self.chips), self.WIDTH * self.HEIGHT)
  
  # return whether the given location is within board parameters
  def is_in_board(self, x: int, y: int) -> bool:
    return 0 <= x < self.WIDTH and 0 <= y < self.HEIGHT
  
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
  def is_completed(self, previous_col: int) -> int:    
    # find y value of previously placed chip
    # go down from top of board until a non-zero chip is found
    # may replace this with additional parameter(s) dependent on implementation of placing a chip
    for previous_row, player in enumerate(self.chips[previous_col]):
      if player != 0:
        break
    #previous_row = self.chips[previous_col].index(0)
        
    measure_dir = partial(self.measure_line, previous_col, previous_row, player)
    # check vertical (downwards is more efficient)
    if any(
      measure_dir(0, 1) >= self.NUM_TO_CONNECT,
      measure_dir(1, 0) + measure_dir(-1, 0) - 1 >= self.NUM_TO_CONNECT,
      measure_dir(1, 1) + measure_dir(-1, -1) - 1 >= self.NUM_TO_CONNECT,
      measure_dir(1, 1) + measure_dir(-1, -1) - 1 >= self.NUM_TO_CONNECT,
      measure_dir(1, -1) + measure_dir(-1, 1) - 1 >= self.NUM_TO_CONNECT,
    ):
      return player
    
    # check for full board
    if np.all(self.chips):
      return self.DRAW

    # board not yet complete
    return self.NOT_COMPLETE
  