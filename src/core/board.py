import numpy as np

from utils.constants import Color


class BlokusBoard:

    def __init__(self, size: int = 20):
        self.size = size
        self.reset()

    def get_cell(self, row: int, col: int) -> int | None:
        if self.is_on_board(row, col):
            return self.board[row, col]
        return None

    def set_cell(self, row: int, col: int, value: int) -> bool:
        if self.is_on_board(row, col):
            self.board[row, col] = value
            return True
        return False

    def reset(self):
        """Reset the board to its initial empty state."""
        self.board = np.zeros((self.size, self.size), dtype=np.int8)

    def is_empty(self, row: int, col: int) -> bool:
        return self.get_cell(row, col) == Color.EMPTY.value

    def is_on_board(self, row: int, col: int) -> bool:
        return 0 <= row < self.size and 0 <= col < self.size

    def clone(self) -> "BlokusBoard":
        """Create a deep copy of the board."""
        new_board = BlokusBoard(self.size)
        new_board.board = self.board.copy()
        return new_board

    def get_corners(self) -> list[tuple[int, int]]:
        """Get the corners of the board."""
        return [
            (0, 0),
            (0, self.size - 1),
            (self.size - 1, 0),
            (self.size - 1, self.size - 1),
        ]
