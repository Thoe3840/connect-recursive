import numpy as np

class Board:
     # not bothering with protected attributes rn

    def __init__(self, width, height, recursion_depth):
        # stores current winner of this board (0 : not won)
        self.complete = 0

       # 2d array of all chips placed, i.e., physical state of board
        self.chips = []
        for i in range(width):
            self.chips.append([0] * height)

        # 2d array of all sub-boards if they exist
        self.sub_boards = None
        if recursion_depth > 1:
            self.sub_boards = []
            for i in range(width):
                # Corkovian code
                # don't know if Board(..) * height works here or whether there's pointer problems
                # and i can't be arsed to find out
                self.sub_boards.append([Board(width, height, recursion_depth - 1) for j in range(height)])

    def __repr__(self):
        # number of chips played in this board
        return 'Board ({})'.format(np.count_nonzero(self.chips))