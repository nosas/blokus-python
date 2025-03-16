import numpy as np
import pytest

from src.core.board import BlokusBoard
from src.utils.constants import Color


@pytest.fixture
def board() -> BlokusBoard:
    return BlokusBoard()


class TestBoard:
    def test_board_initialization(self, board: BlokusBoard):
        assert board.size == 20
        assert board.board.shape == (20, 20)
        assert board.board.dtype == np.int8
        assert board.board.sum() == 0

    def test_get_set_cell(self, board: BlokusBoard):
        board = BlokusBoard()
        board.set_cell(5, 5, Color.BLUE.value)
        assert board.get_cell(5, 5) == Color.BLUE.value

    def test_out_of_bounds(self, board: BlokusBoard):
        board = BlokusBoard()
        assert not board.set_cell(20, 20, Color.RED.value)
        assert board.get_cell(20, 20) is None

    def test_is_empty(self, board: BlokusBoard):
        board = BlokusBoard()
        assert board.is_empty(5, 5)
        board.set_cell(5, 5, Color.BLUE.value)
        assert not board.is_empty(5, 5)

    def test_clone(self, board: BlokusBoard):
        board = BlokusBoard()
        board.set_cell(5, 5, Color.BLUE.value)
        clone = board.clone()
        assert clone.get_cell(5, 5) == Color.BLUE.value

        # Ensure it's a deep copy
        clone.set_cell(6, 6, Color.RED.value)
        assert board.get_cell(6, 6) == Color.EMPTY.value
