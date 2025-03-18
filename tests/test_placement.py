# tests/test_placement.py
import numpy as np
import pytest

from src.core.board import BlokusBoard
from src.core.piece import BlokusPiece
from src.utils.constants import Color


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


class TestFindValidPlacements:
    @pytest.fixture
    def board(self):
        return BlokusBoard(size=10)

    @pytest.fixture
    def simple_piece(self):
        # Create a simple 2x2 L-shaped piece
        return BlokusPiece(
            np.array([[1]]),
            Color.BLUE,
        )

    def test_first_move_valid_placements(self, board, simple_piece):
        """Test that first move returns only corner positions."""
        valid_placements = board.find_valid_placements(
            simple_piece, Color.BLUE, is_first_move=True
        )

        # Should be exactly 4 valid placements (one for each corner)
        assert len(valid_placements) == 4
        assert (0, 0) in valid_placements
        assert (0, board.size - 1) in valid_placements
        assert (board.size - 1, 0) in valid_placements
        assert (board.size - 1, board.size - 1) in valid_placements

    def test_second_move_valid_placements(self, board, simple_piece):
        """Test finding valid placements for a second move."""
        # Place first piece at corner
        board.place_piece(simple_piece, (0, 0), Color.BLUE)

        # Get valid placements for second piece
        second_piece = BlokusPiece(
            np.array(
                [
                    [1, 1],
                    [0, 1],
                ]
            ),
            Color.BLUE,
        )

        valid_placements = board.find_valid_placements(
            second_piece, Color.BLUE, is_first_move=False
        )

        # Should include positions where piece connects at corners
        assert len(valid_placements) == 1
        assert (1, 1) in valid_placements

        # Count should match all possible placements around the corners
        corners = board.get_player_corners(Color.BLUE)
        assert len(corners) == 1

    def test_no_valid_placements(self, board):
        """Test when there are no valid placements for a piece."""
        # Create a large piece
        large_piece = BlokusPiece(
            np.array(
                [
                    [1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1],
                ]
            ),
            Color.BLUE,
        )

        # Place a piece that blocks most corners
        small_piece = BlokusPiece(np.array([[1]]), Color.BLUE)
        for corner in [
            (0, 0),
            (0, board.size - 1),
            (board.size - 1, 0),
            (board.size - 1, board.size - 1),
        ]:
            board.place_piece(small_piece, corner, Color.BLUE)

        # Place the large piece so it blocks all other corners on a size 10 board
        board.place_piece(large_piece, (1, 1), Color.BLUE)

        # Large piece should have no valid placements since corners are blocked
        # and it can't connect properly
        valid_placements = board.find_valid_placements(
            large_piece, Color.BLUE, is_first_move=False
        )
        assert len(valid_placements) == 0

    def test_multiple_players_valid_placements(self, board, simple_piece):
        """Test finding valid placements with multiple players on the board."""
        # Blue player's first move
        board.place_piece(simple_piece, (0, 0), Color.BLUE)

        # Red player's first move
        red_piece = BlokusPiece(
            np.array(
                [
                    [0, 1],
                    [1, 1],
                ]
            ),
            Color.RED,
        )
        board.place_piece(red_piece, (board.size - 2, board.size - 2), Color.RED)

        # Find valid placements for blue's second piece
        small_piece = BlokusPiece(np.array([[1, 1]]), Color.BLUE)
        blue_placements = board.find_valid_placements(small_piece, Color.BLUE, is_first_move=False)

        # Find valid placements for red's second piece
        red_placements = board.find_valid_placements(small_piece, Color.RED, is_first_move=False)

        # Both players should have valid placements
        assert len(blue_placements) == 1
        assert len(red_placements) == 2

        # The two sets of valid placements should be different
        assert set(blue_placements) != set(red_placements)

    def test_all_rotations_and_flips(self, board):
        """Test finding valid placements considering all rotations and flips."""
        # Create an L-shaped piece and place it
        l_piece = BlokusPiece(
            np.array(
                [
                    [1, 0],
                    [1, 0],
                    [1, 1],
                ]
            ),
            Color.BLUE,
        )
        board.place_piece(l_piece, (0, 0), Color.BLUE)

        # Create a piece with distinct shape to test orientations
        t_piece = BlokusPiece(
            np.array(
                [
                    [0, 1, 0],
                    [1, 1, 1],
                ]
            ),
            Color.BLUE,
        )

        # Get valid placements without any transformations
        normal_placements = board.find_valid_placements(t_piece, Color.BLUE, is_first_move=False)
        expected_normal_placements = {(3, 1), (0, 2), (2, 2)}
        assert set(normal_placements) == expected_normal_placements

        # Now test with a rotation
        t_piece.rotate(1)  # 90 degrees clockwise
        rotated_placements = board.find_valid_placements(t_piece, Color.BLUE, is_first_move=False)
        expected_rotated_placements = {(3, 2)}
        assert rotated_placements == expected_rotated_placements

        # The placements should be different as the piece shape has changed
        assert normal_placements != rotated_placements

        # Try with a horiztonal flip
        t_piece.flip()
        flipped_placements = board.find_valid_placements(t_piece, Color.BLUE, is_first_move=False)
        assert flipped_placements == expected_normal_placements
