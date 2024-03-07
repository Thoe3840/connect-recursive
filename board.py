import numpy as np

class Board:
     # not bothering with protected attributes rn
    
    NOT_COMPLETE = 0
    PLAYER_ONE = 1
    PLAYER_TWO = 2
    DRAW = 3
    # stores current winner of this board
    complete = NOT_COMPLETE 

    def __init__(self, width, height, recursion_depth, num_to_connect):
        self.WIDTH = width
        self.HEIGHT = height

        # number of chips to connect in a row to complete the board
        self.NUM_TO_CONNECT = num_to_connect

       # 2d array of all chips placed, i.e., physical state of board
        self.chips = []
        for i in range(width):
            self.chips.append([0] * height)

        # 2d array of all sub-boards if they exist
        self.sub_boards = []
        if recursion_depth > 1:
            for i in range(width):
                # Corkovian code
                # don't know if Board(..) * height works here or whether there's pointer problems
                # and i can't be arsed to find out
                self.sub_boards.append([Board(width, height, recursion_depth - 1, num_to_connect) for j in range(height)])

    def __repr__(self):
        # number of chips played in this board
        return 'Board ({})'.format(np.count_nonzero(self.chips))
    
    # return whether the given location is within board parameters
    def is_in_board(self, x, y):
        return 0 <= x < self.WIDTH and 0 <= y < self.HEIGHT
    
    # return length of unbroken line of given player's chips
    def measure_line(self, start_x, start_y, d_x, d_y, player):
        length = 0
        x = start_x
        y = start_y
        
        while self.is_in_board(x, y) and self.chips[x][y] == player:
            length += 1
            x += d_x
            y += d_y

        return length

    # check whether the previous move connected the required number of if the board is full
    # return completion state
    def is_completed(self, previous_col):
        # check for full board
        if np.count_nonzero(self.chips) == self.WIDTH * self.HEIGHT:
            return self.DRAW
        
        # find y value of previously placed chip
        # go down from top of board until a non-zero chip is found
        # may replace this with additional parameter(s) dependent on implementation of placing a chip
        for previous_row, player in enumerate(self.chips[previous_col]):
            if player != 0:
                break

        #TODO not sure about this format currently
        #maybe refactor measure_line or use 'or's for these conditionals

        # check vertical (downwards is more efficient)
        if self.measure_line(previous_col, previous_row, 0, 1, player) >= self.NUM_TO_CONNECT:
            return player
        
        # check horizontal (add both directions)
        if self.measure_line(previous_col, previous_row, 1, 0, player) + self.measure_line(previous_col - 1, previous_row, -1, 0, player) >= self.NUM_TO_CONNECT:
            return player
        
        #check bottom left to top right diagonal
        if self.measure_line(previous_col, previous_row, 1, 1, player) + self.measure_line(previous_col - 1, previous_row - 1, -1, -1, player) >= self.NUM_TO_CONNECT:
            return player
        
        #check top left to bottom right diagonal
        if self.measure_line(previous_col, previous_row, 1, 1, player) + self.measure_line(previous_col - 1, previous_row - 1, -1, -1, player) >= self.NUM_TO_CONNECT:
            return player
        
        #check bottom left to top right diagonal
        if self.measure_line(previous_col, previous_row, 1, -1, player) + self.measure_line(previous_col - 1, previous_row + 1, -1, 1, player) >= self.NUM_TO_CONNECT:
            return player
        
        # board not yet complete
        return self.NOT_COMPLETE