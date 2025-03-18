# tests/test_placement.py
import numpy as np
import pytest

from src.core.board import BlokusBoard
from src.utils.constants import Color
from src.core.piece import BlokusPiece


class TestPlacementValidation:
    @pytest.fixture
    def board(self):
        return BlokusBoard(size=10)

    @pytest.fixture
    def piece(self):
        # Create a simple L-shaped piece
        return BlokusPiece(
            np.array(
                [
                    [1, 0],
                    [1, 1],
                ]
            ),
            Color.BLUE,
        )

    def test_first_move_corner(self, board, piece):
        # First move must cover a corner
        assert board.is_valid_placement(piece, (0, 0), Color.BLUE, is_first_move=True)

        # First move not covering corner is invalid
        assert not board.is_valid_placement(piece, (5, 5), Color.BLUE, is_first_move=True)

    def test_piece_overlap(self, board, piece):
        # Place a piece at (0, 0)
        board.place_piece(piece, (0, 0), Color.BLUE)

        # Try to place a piece overlapping with existing piece
        assert not board.is_valid_placement(piece, (0, 0), Color.RED, is_first_move=True)

    def test_corner_connectivity(self, board, piece):
        # Place first piece at corner
        board.place_piece(piece, (0, 0), Color.BLUE)

        # Place second piece that connects at corner
        second_piece = BlokusPiece(
            np.array(
                [
                    [1, 1],
                    [0, 1],
                ]
            ),
            Color.BLUE,
        )

        # Valid: connects at corner (2,2)
        assert board.is_valid_placement(second_piece, (0, 2), Color.BLUE)

        # Invalid: connects at side
        assert not board.is_valid_placement(second_piece, (1, 1), Color.BLUE)

        # Invalid: no connection
        assert not board.is_valid_placement(second_piece, (5, 5), Color.BLUE)

    def test_other_color_adjacency(self, board, piece):
        # Place blue piece at corner
        board.place_piece(piece, (0, 0), Color.BLUE)

        # First place a red piece at a position next to the blue piece
        first_red_piece = BlokusPiece(np.array([[1]]), Color.RED)
        board.place_piece(first_red_piece, (1, 1), Color.RED)

        # Now test that a second red piece can be adjacent to blue pieces
        red_piece = BlokusPiece(np.array([[1, 1]]), Color.RED)
        assert board.is_valid_placement(red_piece, (2, 2), Color.RED)

    def test_get_player_corners(self, board, piece):
        # Place a piece and check if corners are correctly identified
        board.place_piece(piece, (0, 0), Color.BLUE)

        corners = board.get_player_corners(Color.BLUE)
        assert len(corners) == 2
        assert (0, 2) in corners
        assert (2, 2) in corners

        # Place another piece and check updated corners
        second_piece = BlokusPiece(np.array([[1, 1]]), Color.BLUE)
        board.place_piece(second_piece, (2, 2), Color.BLUE)

        updated_corners = board.get_player_corners(Color.BLUE)
        assert len(updated_corners) == 4
        expected_corners = {(0, 2), (1, 4), (3, 4), (3, 1)}
        assert updated_corners == expected_corners

        # Check that the corner where the second piece was placed is no longer valid
        assert (2, 2) not in updated_corners

    def test_piece_rotation_and_orientation(self, board):
        """Test placing pieces in different orientations."""
        # Create an L-shaped piece
        piece = BlokusPiece(
            np.array(
                [
                    [1, 0],
                    [1, 0],
                    [1, 1],
                ]
            ),
            Color.BLUE,
        )

        # Place the piece in its original orientation
        assert board.is_valid_placement(piece, (0, 0), Color.BLUE, is_first_move=True)
        board.place_piece(piece, (0, 0), Color.BLUE)

        # Create a rotated version of the same piece
        rotated_piece = BlokusPiece(
            np.array(
                [
                    [1, 0],
                    [1, 0],
                    [1, 1],
                ]
            ),
            Color.BLUE,
        )
        rotated_piece.rotate(1)  # 90 degrees clockwise

        # Test the rotated piece can be placed connecting at corners
        assert board.is_valid_placement(rotated_piece, (0, 2), Color.BLUE, is_first_move=False)

    def test_board_boundary(self, board):
        """Test piece placement at board boundaries."""
        # Create a piece
        piece = BlokusPiece(np.array([[1, 1, 1]]), Color.BLUE)

        # Place at top-right corner
        assert board.is_valid_placement(piece, (0, board.size - 3), Color.BLUE, is_first_move=True)

        # Test placement that would extend beyond the board
        assert not board.is_valid_placement(
            piece, (0, board.size - 2), Color.BLUE, is_first_move=True
        )

        # Test placement at bottom boundary
        assert board.is_valid_placement(piece, (board.size - 1, 0), Color.BLUE, is_first_move=True)

    def test_multiple_player_moves(self, board):
        """Test a sequence of moves from multiple players."""
        # First player (Blue) places at a corner
        blue_piece = BlokusPiece(
            np.array(
                [
                    [1, 1],
                    [1, 0],
                ]
            ),
            Color.BLUE,
        )
        board.place_piece(blue_piece, (0, 0), Color.BLUE)

        # Second player (Yellow) places at a different corner
        yellow_piece = BlokusPiece(
            np.array(
                [
                    [1, 1],
                    [1, 0],
                ]
            ),
            Color.YELLOW,
        )
        assert board.is_valid_placement(
            yellow_piece, (0, board.size - 2), Color.YELLOW, is_first_move=True
        )
        board.place_piece(yellow_piece, (0, board.size - 2), Color.YELLOW)

        # Blue's second move connecting at corner
        blue_piece2 = BlokusPiece(
            np.array(
                [
                    [1, 0],
                    [1, 1],
                ]
            ),
            Color.BLUE,
        )
        assert board.is_valid_placement(blue_piece2, (2, 1), Color.BLUE, is_first_move=False)
        board.place_piece(blue_piece2, (2, 1), Color.BLUE)

        # Yellow's second move - should connect at corner only
        yellow_piece2 = BlokusPiece(np.array([[1, 1]]), Color.YELLOW)
        assert not board.is_valid_placement(
            yellow_piece2, (0, board.size - 3), Color.YELLOW, is_first_move=False
        )
        assert board.is_valid_placement(
            yellow_piece2, (2, board.size - 4), Color.YELLOW, is_first_move=False
        )

    def test_complex_pieces(self, board):
        """Test placement of more complex piece shapes."""
        # Create a T-shaped pentomino
        t_piece = BlokusPiece(
            np.array(
                [
                    [1, 1, 1],
                    [0, 1, 0],
                    [0, 1, 0],
                ]
            ),
            Color.BLUE,
        )

        # First move at corner
        assert board.is_valid_placement(t_piece, (0, 0), Color.BLUE, is_first_move=True)
        board.place_piece(t_piece, (0, 0), Color.BLUE)

        # Get valid corners after placement
        corners = board.get_player_corners(Color.BLUE)
        expected_corners = {(3, 0), (3, 2), (1, 3)}
        assert len(corners) == 3
        assert corners == expected_corners

        # Try an X-shaped pentomino
        x_piece = BlokusPiece(
            np.array(
                [
                    [0, 1, 0],
                    [1, 1, 1],
                    [0, 1, 0],
                ]
            ),
            Color.BLUE,
        )

        # Should be able to place at a valid corner
        # NOTE: It's placed at (3, 1) because the placement calculation is done by the piece's
        # top-left corner. So, we're placing the top-left corner at (3, 1), but the piece's
        # top-middle cell at (3, 2) will corner the bottom-most piece's cell at (2, 1).
        assert board.is_valid_placement(x_piece, (3, 1), Color.BLUE, is_first_move=False)

    def test_crowded_board_placement(self, board):
        """Test placement in a more crowded board scenario."""
        # Fill part of the board with pieces from different players
        blue_piece = BlokusPiece(np.array([[1, 1], [1, 0]]), Color.BLUE)
        red_piece = BlokusPiece(np.array([[1, 1], [1, 0]]), Color.RED)
        yellow_piece = BlokusPiece(np.array([[1, 1], [1, 0]]), Color.YELLOW)
        green_piece = BlokusPiece(np.array([[1, 1], [1, 0]]), Color.GREEN)

        board.place_piece(blue_piece, (0, 0), Color.BLUE)
        board.place_piece(red_piece, (board.size - 2, 0), Color.RED)
        board.place_piece(yellow_piece, (0, board.size - 2), Color.YELLOW)
        board.place_piece(green_piece, (board.size - 2, board.size - 2), Color.GREEN)

        # Now try to place a piece in a tight spot
        small_piece = BlokusPiece(np.array([[1]]), Color.BLUE)
        # These should be valid/invalid based on corner connectivity rules
        assert board.is_valid_placement(small_piece, (2, 1), Color.BLUE, is_first_move=False)
        assert not board.is_valid_placement(small_piece, (1, 1), Color.BLUE, is_first_move=False)
