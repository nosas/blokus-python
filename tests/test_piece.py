import numpy as np
import pytest

from src.core.piece import BlokusPiece
from src.utils.constants import Color
from src.utils.piece_data import get_standard_piece_shapes


class TestStandardBlokusPieces:

    piece_shapes = get_standard_piece_shapes()

    def test_piece_count(self):
        assert len(self.piece_shapes) == 21

    def test_piece_sizes(self) -> None:
        # Count pieces by size
        sizes: dict[int, int] = {}

        for piece_shape in self.piece_shapes:
            size = piece_shape["shape"].sum()
            if size not in sizes:
                sizes[size] = 0
            sizes[size] += 1

        assert sizes[1] == 1
        assert sizes[2] == 1
        assert sizes[3] == 2
        assert sizes[4] == 5
        assert sizes[5] == 12

    def test_piece_uniqueness(self):
        # Verify all pieces have unique IDs
        piece_ids = [p["id"] for p in self.piece_shapes]
        assert len(piece_ids) == len(set(piece_ids))

    def test_piece_initialization(self):
        for piece_shape in self.piece_shapes:
            piece = BlokusPiece(
                shape=piece_shape["shape"],
                color=Color.EMPTY,
                piece_id=piece_shape["id"],
            )

            assert piece.get_piece_id() == piece_shape["id"]
            assert np.array_equal(piece.get_shape(), piece_shape["shape"])


class TestBlokusPiece:
    @pytest.fixture
    def simple_piece(self):
        # Create a simple L-shaped piece
        shape = np.array(
            [
                [1, 0],
                [1, 1],
            ]
        )
        return BlokusPiece(shape=shape, color=Color.BLUE, piece_id="test_L")

    def test_get_size(self, simple_piece):
        assert simple_piece.get_size() == 3

    def test_get_color(self, simple_piece):
        assert simple_piece.get_color() == Color.BLUE

    def test_get_dimensions(self, simple_piece):
        height, width = simple_piece.get_dimensions()
        assert height == 2
        assert width == 2

    def test_get_filled_cells(self, simple_piece):
        filled_cells = simple_piece.get_filled_cells()
        assert len(filled_cells) == 3
        assert (0, 0) in filled_cells
        assert (1, 0) in filled_cells
        assert (1, 1) in filled_cells

    def test_rotate(self, simple_piece):
        # Original shape:
        # 1 0
        # 1 1

        # After one rotation (90° clockwise):
        # 1 1
        # 1 0
        rotated_once = simple_piece.rotate()
        expected_shape = np.array(
            [
                [1, 1],
                [1, 0],
            ]
        )
        assert np.array_equal(rotated_once.get_shape(), expected_shape)

        # After another rotation (180° from original):
        # 1 1
        # 0 1
        rotated_twice = simple_piece.rotate()
        expected_shape = np.array(
            [
                [1, 1],
                [0, 1],
            ]
        )
        assert np.array_equal(rotated_twice.get_shape(), expected_shape)

        # After third rotation (270° from original):
        # 0 1
        # 1 1
        rotated_thrice = simple_piece.rotate()
        expected_shape = np.array(
            [
                [0, 1],
                [1, 1],
            ]
        )
        assert np.array_equal(rotated_thrice.get_shape(), expected_shape)

        # After fourth rotation (back to original):
        # 1 0
        # 1 1
        rotated_four_times = simple_piece.rotate()
        expected_shape = np.array(
            [
                [1, 0],
                [1, 1],
            ]
        )
        assert np.array_equal(rotated_four_times.get_shape(), expected_shape)

    def test_flip(self, simple_piece):
        # Original shape:
        # 1 0
        # 1 1

        # After horizontal flip:
        # 0 1
        # 1 1
        flipped = simple_piece.flip()
        expected_shape = np.array(
            [
                [0, 1],
                [1, 1],
            ]
        )
        assert np.array_equal(flipped.get_shape(), expected_shape)

        # Flip again to get back to original
        flipped_again = simple_piece.flip()
        expected_original = np.array(
            [
                [1, 0],
                [1, 1],
            ]
        )
        assert np.array_equal(flipped_again.get_shape(), expected_original)

    def test_reset_orientation(self, simple_piece):
        # Modify the piece with rotations and flips
        simple_piece.rotate().flip()

        # Reset to original orientation
        reset_piece = simple_piece.reset_orientation()
        expected_original = np.array(
            [
                [1, 0],
                [1, 1],
            ]
        )
        assert np.array_equal(reset_piece.get_shape(), expected_original)

    def test_get_all_orientations(self, simple_piece):
        # The L-shaped piece should have 4 unique orientations
        # (considering rotations and flips)
        orientations = simple_piece.get_all_orientations()

        # Check we have the right number of unique orientations
        assert len(orientations) == 4

        # Verify each orientation is unique
        unique_orientations = set()
        for orientation in orientations:
            orientation_tuple = tuple(map(tuple, orientation))
            unique_orientations.add(orientation_tuple)

        assert len(unique_orientations) == 4

        # Verify the original shape wasn't modified
        expected_original = np.array(
            [
                [1, 0],
                [1, 1],
            ]
        )
        assert np.array_equal(simple_piece.get_shape(), expected_original)

    def test_unknown_piece_id(self):
        # Test piece with no ID
        shape = np.array([[1]])
        piece = BlokusPiece(shape=shape, color=Color.RED)
        assert piece.get_piece_id() == "Unknown"

    def test_list_shape_conversion(self):
        # Test that list shapes are converted to numpy arrays
        list_shape = [[1, 0], [1, 1]]
        piece = BlokusPiece(shape=list_shape, color=Color.GREEN, piece_id="list_test")

        assert isinstance(piece.get_shape(), np.ndarray)
        expected_shape = np.array(
            [
                [1, 0],
                [1, 1],
            ]
        )
        assert np.array_equal(piece.get_shape(), expected_shape)
