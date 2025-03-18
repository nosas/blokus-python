# Blokus Implementation: Phase 1 Technical Document
## Core Game Engine Development Guide

## Overview

Phase 1 focuses on implementing the core game engine for Blokus, creating the foundation upon which the entire project will be built. This phase spans two weeks and covers the essential data structures, game rules, and mechanics that power the Blokus experience. By the end of this phase, we will have a functionally complete game engine that enforces all Blokus rules and can be used to play a complete game programmatically.

## Timeline Summary

**Week 1: Data Models and Basic Mechanics**
- Days 1-2: Define board and piece data structures
- Days 3-4: Implement piece transformations
- Days 5-7: Create standard piece set

**Week 2: Game Rules and Flow**
- Days 1-3: Implement placement validation
- Days 4-5: Build turn management
- Days 6-7: Create scoring and end-game detection

## Project Structure

For Phase 1, establish the following directory structure:

```
blokus/
├── core/
│   ├── __init__.py
│   ├── board.py
│   ├── piece.py
│   ├── game.py
│   └── player.py
├── utils/
│   ├── __init__.py
│   ├── constants.py
│   ├── piece_data.py
│   └── validators.py
├── tests/
│   ├── __init__.py
│   ├── test_board.py
│   ├── test_piece.py
│   ├── test_game.py
│   └── test_player.py
└── main.py
```

## Detailed Implementation Guide

### Week 1: Data Models and Basic Mechanics

#### Days 1-2: Board and Piece Data Structures

**Task 1: Implement the `Color` enum**

```python
# core/constants.py
from enum import Enum

class Color(Enum):
    EMPTY = 0
    BLUE = 1
    YELLOW = 2
    RED = 3
    GREEN = 4

    @classmethod
    def get_player_colors(cls):
        """Return the four player colors (excluding EMPTY)."""
        return [cls.BLUE, cls.YELLOW, cls.RED, cls.GREEN]
```

**Task 2: Implement the `BlokusBoard` class**

```python
# core/board.py
import numpy as np
from .constants import Color

class BlokusBoard:
    """
    Represents the Blokus game board.

    Attributes:
        size (int): The size of the board (standard is 20x20)
        board (numpy.ndarray): 2D array representing the board state
    """

    def __init__(self, size=20):
        """
        Initialize a Blokus board.

        Args:
            size (int): The size of the board (default: 20)
        """
        self.size = size
        self.board = np.zeros((size, size), dtype=int)

    def get_cell(self, row, col):
        """
        Get the value of a specific cell on the board.

        Args:
            row (int): Row index
            col (int): Column index

        Returns:
            int: Cell value (0 for empty, 1-4 for player colors)
        """
        if 0 <= row < self.size and 0 <= col < self.size:
            return self.board[row, col]
        return None

    def set_cell(self, row, col, value):
        """
        Set the value of a specific cell on the board.

        Args:
            row (int): Row index
            col (int): Column index
            value (int): Cell value (0 for empty, 1-4 for player colors)

        Returns:
            bool: True if cell was set, False if out of bounds
        """
        if 0 <= row < self.size and 0 <= col < self.size:
            self.board[row, col] = value
            return True
        return False

    def reset(self):
        """Reset the board to its initial empty state."""
        self.board = np.zeros((self.size, self.size), dtype=int)

    def is_empty(self, row, col):
        """Check if a specific cell is empty."""
        return self.get_cell(row, col) == Color.EMPTY.value

    def is_on_board(self, row, col):
        """Check if coordinates are within board boundaries."""
        return 0 <= row < self.size and 0 <= col < self.size

    def clone(self):
        """Create a deep copy of the board."""
        new_board = BlokusBoard(self.size)
        new_board.board = self.board.copy()
        return new_board

    def get_corners(self):
        """Get the four corner positions of the board."""
        return [
            (0, 0),
            (0, self.size - 1),
            (self.size - 1, 0),
            (self.size - 1, self.size - 1)
        ]
```

**Task 3: Implement the `BlokusPiece` base class**

```python
# core/piece.py
import numpy as np
from .constants import Color

class BlokusPiece:
    """
    Represents a Blokus game piece.

    Attributes:
        shape (numpy.ndarray): 2D binary array representing the piece's shape
        color (Color): The color of the piece
        piece_id (str): Unique identifier for the piece
    """

    def __init__(self, shape, color, piece_id=None):
        """
        Initialize a Blokus piece.

        Args:
            shape (numpy.ndarray or list): 2D array representing the piece's shape
            color (Color): The color of the piece
            piece_id (str, optional): Unique identifier for the piece
        """
        if isinstance(shape, list):
            shape = np.array(shape)

        self.original_shape = shape.copy()
        self.shape = shape.copy()
        self.color = color
        self.piece_id = piece_id

        # Calculate the number of squares in the piece
        self.size = np.sum(self.shape)

        # Calculate the shape dimensions
        self.height, self.width = self.shape.shape

    def get_size(self):
        """Get the number of squares in the piece."""
        return self.size

    def get_shape(self):
        """Get the current shape array."""
        return self.shape

    def get_dimensions(self):
        """Get the current height and width of the piece."""
        self.height, self.width = self.shape.shape
        return self.height, self.width

    def get_filled_cells(self):
        """
        Get the coordinates of all filled cells in the piece.

        Returns:
            list: List of (row, col) tuples for all filled cells
        """
        filled = []
        for r in range(self.height):
            for c in range(self.width):
                if self.shape[r, c] == 1:
                    filled.append((r, c))
        return filled
```

**Testing Board and Piece Classes**

Create comprehensive unit tests for both classes to verify functionality:

```python
# tests/test_board.py
import unittest
import numpy as np
from core.board import BlokusBoard
from core.constants import Color

class TestBlokusBoard(unittest.TestCase):
    def setUp(self):
        self.board = BlokusBoard(size=20)

    def test_initialization(self):
        self.assertEqual(self.board.size, 20)
        self.assertEqual(self.board.board.shape, (20, 20))
        self.assertEqual(np.sum(self.board.board), 0)  # All cells empty

    def test_get_set_cell(self):
        self.board.set_cell(5, 5, Color.BLUE.value)
        self.assertEqual(self.board.get_cell(5, 5), Color.BLUE.value)

    def test_out_of_bounds(self):
        self.assertFalse(self.board.set_cell(20, 20, Color.RED.value))
        self.assertIsNone(self.board.get_cell(20, 20))

    def test_is_empty(self):
        self.assertTrue(self.board.is_empty(5, 5))
        self.board.set_cell(5, 5, Color.BLUE.value)
        self.assertFalse(self.board.is_empty(5, 5))

    def test_clone(self):
        self.board.set_cell(5, 5, Color.BLUE.value)
        clone = self.board.clone()
        self.assertEqual(clone.get_cell(5, 5), Color.BLUE.value)

        # Ensure it's a deep copy
        clone.set_cell(6, 6, Color.RED.value)
        self.assertEqual(self.board.get_cell(6, 6), Color.EMPTY.value)
```

#### Days 3-4: Piece Transformations

**Task 4: Implement Piece Transformations**

Add the following methods to the `BlokusPiece` class:

```python
# core/piece.py (additions)

def rotate(self, rotations=1):
    """
    Rotate the piece 90 degrees clockwise, n times.

    Args:
        rotations (int): Number of 90-degree rotations (1-3)

    Returns:
        BlokusPiece: Self, for method chaining
    """
    # np.rot90 rotates counter-clockwise by default, so we use 4-rotations
    self.shape = np.rot90(self.shape, k=4-(rotations % 4))
    self.height, self.width = self.shape.shape
    return self

def flip(self):
    """
    Flip the piece horizontally.

    Returns:
        BlokusPiece: Self, for method chaining
    """
    self.shape = np.fliplr(self.shape)
    return self

def reset_orientation(self):
    """
    Reset the piece to its original orientation.

    Returns:
        BlokusPiece: Self, for method chaining
    """
    self.shape = self.original_shape.copy()
    self.height, self.width = self.shape.shape
    return self

def get_all_orientations(self):
    """
    Generate all unique orientations of this piece.

    Returns:
        list: List of shape arrays (numpy arrays)
    """
    orientations = []
    seen_shapes = set()

    # Save original orientation
    original = self.shape.copy()

    # Try all combinations of rotations and flips
    for flip in [False, True]:
        if flip:
            self.flip()

        for rotation in range(4):
            if rotation > 0:
                self.rotate()

            # Convert shape to hashable format
            shape_tuple = tuple(map(tuple, self.shape))

            # Only add if this is a new unique orientation
            if shape_tuple not in seen_shapes:
                seen_shapes.add(shape_tuple)
                orientations.append(self.shape.copy())

    # Restore original orientation
    self.shape = original
    self.height, self.width = self.shape.shape

    return orientations
```

**Testing Piece Transformations**

```python
# tests/test_piece_transformations.py
import unittest
import numpy as np
from core.piece import BlokusPiece
from core.constants import Color

class TestPieceTransformations(unittest.TestCase):
    def setUp(self):
        # Create an L-shaped piece
        shape = np.array([
            [1, 0],
            [1, 0],
            [1, 1]
        ])
        self.piece = BlokusPiece(shape, Color.BLUE, "L")

    def test_rotate_once(self):
        self.piece.rotate()
        expected = np.array([
            [1, 1, 1],
            [1, 0, 0]
        ])
        np.testing.assert_array_equal(self.piece.shape, expected)

    def test_rotate_twice(self):
        self.piece.rotate(2)
        expected = np.array([
            [1, 1],
            [0, 1],
            [0, 1]
        ])
        np.testing.assert_array_equal(self.piece.shape, expected)

    def test_flip(self):
        self.piece.flip()
        expected = np.array([
            [0, 1],
            [0, 1],
            [1, 1]
        ])
        np.testing.assert_array_equal(self.piece.shape, expected)

    def test_reset_orientation(self):
        self.piece.rotate().flip()
        self.piece.reset_orientation()
        original = np.array([
            [1, 0],
            [1, 0],
            [1, 1]
        ])
        np.testing.assert_array_equal(self.piece.shape, original)

    def test_get_all_orientations(self):
        orientations = self.piece.get_all_orientations()

        # L shape should have 8 unique orientations
        self.assertEqual(len(orientations), 8)

        # Verify all orientations are unique
        orientation_tuples = [tuple(map(tuple, o)) for o in orientations]
        self.assertEqual(len(set(orientation_tuples)), 8)
```

#### Days 5-7: Create Standard Piece Set

**Task 5: Define Piece Data**

```python
# utils/piece_data.py
import numpy as np

def create_piece_shape(id_char, shape_array):
    """
    Create a standardized piece shape with metadata.

    Args:
        id_char (str): Single character ID for the piece
        shape_array (list): 2D array representing the piece shape

    Returns:
        dict: Piece definition with id and shape
    """
    return {
        "id": id_char,
        "shape": np.array(shape_array)
    }

def get_standard_piece_shapes():
    """
    Create the standard 21 Blokus pieces as shape definitions.

    Returns:
        list: List of piece shape definitions
    """
    pieces = []

    # 1-square piece (monomino)
    pieces.append(create_piece_shape("1", [[1]]))

    # 2-square piece (domino)
    pieces.append(create_piece_shape("2", [[1, 1]]))

    # 3-square pieces (trominoes)
    pieces.append(create_piece_shape("I3", [[1, 1, 1]]))
    pieces.append(create_piece_shape("V3", [[1, 0],
                                           [1, 1]]))

    # 4-square pieces (tetrominoes)
    pieces.append(create_piece_shape("I4", [[1, 1, 1, 1]]))
    pieces.append(create_piece_shape("L4", [[1, 0],
                                           [1, 0],
                                           [1, 1]]))
    pieces.append(create_piece_shape("Z4", [[1, 1, 0],
                                           [0, 1, 1]]))
    pieces.append(create_piece_shape("O4", [[1, 1],
                                           [1, 1]]))
    pieces.append(create_piece_shape("T4", [[1, 1, 1],
                                           [0, 1, 0]]))

    # 5-square pieces (pentominoes) - all 12 of them
    pieces.append(create_piece_shape("I5", [[1, 1, 1, 1, 1]]))

    pieces.append(create_piece_shape("L5", [[1, 0],
                                           [1, 0],
                                           [1, 0],
                                           [1, 1]]))

    pieces.append(create_piece_shape("Y5", [[0, 1],
                                           [1, 1],
                                           [0, 1],
                                           [0, 1]]))

    pieces.append(create_piece_shape("N5", [[0, 1],
                                           [1, 1],
                                           [1, 0],
                                           [1, 0]]))

    pieces.append(create_piece_shape("P5", [[1, 1],
                                           [1, 1],
                                           [1, 0]]))

    pieces.append(create_piece_shape("U5", [[1, 0, 1],
                                           [1, 1, 1]]))

    pieces.append(create_piece_shape("V5", [[1, 0, 0],
                                           [1, 0, 0],
                                           [1, 1, 1]]))

    pieces.append(create_piece_shape("Z5", [[1, 1, 0],
                                           [0, 1, 0],
                                           [0, 1, 1]]))

    pieces.append(create_piece_shape("T5", [[1, 1, 1],
                                           [0, 1, 0],
                                           [0, 1, 0]]))

    pieces.append(create_piece_shape("W5", [[1, 0, 0],
                                           [1, 1, 0],
                                           [0, 1, 1]]))

    pieces.append(create_piece_shape("F5", [[0, 1, 1],
                                           [1, 1, 0],
                                           [0, 1, 0]]))

    pieces.append(create_piece_shape("X5", [[0, 1, 0],
                                           [1, 1, 1],
                                           [0, 1, 0]]))

    return pieces
```

**Task 6: Implement Player Class**

```python
# core/player.py
from .piece import BlokusPiece
from utils.piece_data import get_standard_piece_shapes

class BlokusPlayer:
    """
    Represents a player in the Blokus game.

    Attributes:
        color (Color): The player's color
        pieces (list): List of BlokusPiece objects available to the player
        first_move (bool): Whether this is the player's first move
        player_id (int): Numeric ID for the player (1-4)
    """

    def __init__(self, color, player_id):
        """
        Initialize a Blokus player.

        Args:
            color (Color): The player's color
            player_id (int): Numeric ID for the player (1-4)
        """
        self.color = color
        self.player_id = player_id
        self.first_move = True
        self.pieces = []
        self.initialize_pieces()

    def initialize_pieces(self):
        """Initialize the standard set of 21 Blokus pieces."""
        self.pieces = []
        piece_shapes = get_standard_piece_shapes()

        for piece_data in piece_shapes:
            piece = BlokusPiece(
                piece_data["shape"],
                self.color,
                piece_data["id"]
            )
            self.pieces.append(piece)

    def get_piece(self, index):
        """Get a piece by index."""
        if 0 <= index < len(self.pieces):
            return self.pieces[index]
        return None

    def remove_piece(self, index):
        """Remove a piece from the player's inventory."""
        if 0 <= index < len(self.pieces):
            return self.pieces.pop(index)
        return None

    def has_pieces_remaining(self):
        """Check if the player has any pieces remaining."""
        return len(self.pieces) > 0

    def get_remaining_piece_count(self):
        """Get the number of pieces remaining."""
        return len(self.pieces)

    def get_pieces_by_size(self, size):
        """Get all pieces of a specific size."""
        return [p for p in self.pieces if p.get_size() == size]

    def get_smallest_piece(self):
        """Get the smallest remaining piece."""
        if not self.pieces:
            return None
        return min(self.pieces, key=lambda p: p.get_size())
```

**Testing Standard Piece Set**

```python
# tests/test_pieces.py
import unittest
from core.player import BlokusPlayer
from core.constants import Color

class TestStandardPieceSet(unittest.TestCase):
    def setUp(self):
        self.player = BlokusPlayer(Color.BLUE, 1)

    def test_piece_count(self):
        self.assertEqual(len(self.player.pieces), 21)

    def test_piece_sizes(self):
        # Count pieces by size
        sizes = {}
        for piece in self.player.pieces:
            size = piece.get_size()
            if size not in sizes:
                sizes[size] = 0
            sizes[size] += 1

        # Verify correct distribution
        self.assertEqual(sizes[1], 1)  # One 1-square piece
        self.assertEqual(sizes[2], 1)  # One 2-square piece
        self.assertEqual(sizes[3], 2)  # Two 3-square pieces
        self.assertEqual(sizes[4], 5)  # Five 4-square pieces
        self.assertEqual(sizes[5], 12)  # Twelve 5-square pieces

    def test_piece_uniqueness(self):
        # Verify all pieces have unique IDs
        piece_ids = [p.piece_id for p in self.player.pieces]
        self.assertEqual(len(piece_ids), len(set(piece_ids)))
```

### Week 2: Game Rules and Flow

#### Days 1-3: Implement Placement Validation

**Task 7: Game Board Placement Validation**

Add validation methods to the `BlokusBoard` class:

```python
# core/board.py (additions)

def is_valid_placement(self, piece, position, player_color, is_first_move=False):
    """
    Check if a piece can be legally placed at the given position.

    Args:
        piece (BlokusPiece): The piece to place
        position (tuple): (row, col) tuple for top-left corner of piece
        player_color (Color): The color of the player making the move
        is_first_move (bool): Whether this is the player's first move

    Returns:
        bool: Whether the placement is valid
    """
    row, col = position
    shape = piece.get_shape()
    height, width = piece.get_dimensions()

    # Check 1: Piece must fit on board
    if row + height > self.size or col + width > self.size:
        return False

    # Check 2: Piece must not overlap with any existing pieces
    for r in range(height):
        for c in range(width):
            if shape[r, c] == 1:
                if self.board[row + r, col + c] != Color.EMPTY.value:
                    return False

    # Check 3: First move must cover a corner
    if is_first_move:
        corners = self.get_corners()
        covers_corner = False

        for r in range(height):
            for c in range(width):
                if shape[r, c] == 1 and (row + r, col + c) in corners:
                    covers_corner = True
                    break

        if not covers_corner:
            return False

    # Check 4: Non-first moves must touch at least one own piece at corner
    # and must not touch any own pieces along sides
    else:
        touches_corner = False
        touches_side = False
        player_value = player_color.value

        for r in range(height):
            for c in range(width):
                if shape[r, c] == 1:
                    board_r, board_c = row + r, col + c

                    # Check corners (diagonal adjacency)
                    corners = [
                        (board_r - 1, board_c - 1), (board_r - 1, board_c + 1),
                        (board_r + 1, board_c - 1), (board_r + 1, board_c + 1)
                    ]

                    for cr, cc in corners:
                        if self.is_on_board(cr, cc) and self.board[cr, cc] == player_value:
                            touches_corner = True

                    # Check sides (orthogonal adjacency)
                    sides = [
                        (board_r - 1, board_c), (board_r + 1, board_c),
                        (board_r, board_c - 1), (board_r, board_c + 1)
                    ]

                    for sr, sc in sides:
                        if self.is_on_board(sr, sc) and self.board[sr, sc] == player_value:
                            touches_side = True

        if not touches_corner or touches_side:
            return False

    return True

def place_piece(self, piece, position, player_color):
    """
    Place a piece on the board.

    Args:
        piece (BlokusPiece): The piece to place
        position (tuple): (row, col) tuple for top-left corner of piece
        player_color (Color): The color of the player making the move

    Returns:
        bool: Whether the piece was successfully placed
    """
    row, col = position
    shape = piece.get_shape()
    height, width = piece.get_dimensions()

    # Place the piece on the board
    for r in range(height):
        for c in range(width):
            if shape[r, c] == 1:
                self.board[row + r, col + c] = player_color.value

    return True
```

**Task 8: Helper Functions for Move Generation**

```python
# core/board.py (additions)

def get_player_corners(self, player_color):
    """
    Get all valid corner positions for a player's pieces.

    Args:
        player_color (Color): The player's color

    Returns:
        list: List of (row, col) tuples for valid corners
    """
    player_value = player_color.value
    corners = []

    # Scan the entire board
    for r in range(self.size):
        for c in range(self.size):
            # Skip non-empty cells
            if self.board[r, c] != Color.EMPTY.value:
                continue

            # Check all diagonals for player's pieces
            diagonals = [
                (r-1, c-1), (r-1, c+1),
                (r+1, c-1), (r+1, c+1)
            ]

            touches_corner = False
            for dr, dc in diagonals:
                if (self.is_on_board(dr, dc) and
                    self.board[dr, dc] == player_value):
                    touches_corner = True
                    break

            # Check all sides for player's pieces
            sides = [
                (r-1, c), (r+1, c),
                (r, c-1), (r, c+1)
            ]

            touches_side = False
            for sr, sc in sides:
                if (self.is_on_board(sr, sc) and
                    self.board[sr, sc] == player_value):
                    touches_side = True
                    break

            # Valid corner: touches at corner but not at side
            if touches_corner and not touches_side:
                corners.append((r, c))

    return corners

def find_valid_placements(self, piece, player_color, is_first_move=False):
    """
    Find all valid placements for a given piece.

    Args:
        piece (BlokusPiece): The piece to place
        player_color (Color): The player's color
        is_first_move (bool): Whether this is the player's first move

    Returns:
        list: List of valid (row, col) positions
    """
    valid_placements = []

    # For first move, only check the corners
    if is_first_move:
        positions_to_check = self.get_corners()
    else:
        # Get all corner positions for this player
        corner_cells = self.get_player_corners(player_color)

        # Expand to all potential placements around these corners
        positions_to_check = set()
        for cr, cc in corner_cells:
            # Consider positions where the piece might cover this corner
            piece_height, piece_width = piece.get_dimensions()
            for r in range(max(0, cr - piece_height + 1), min(cr + 1, self.size - piece_height + 1)):
                for c in range(max(0, cc - piece_width + 1), min(cc + 1, self.size - piece_width + 1)):
                    positions_to_check.add((r, c))

    # Check all potential positions
    for position in positions_to_check:
        if self.is_valid_placement(piece, position, player_color, is_first_move):
            valid_placements.append(position)

    return valid_placements
```

**Testing Placement Validation**

```python
# tests/test_placement.py
import unittest
import numpy as np
from core.board import BlokusBoard
from core.piece import BlokusPiece
from core.constants import Color

class TestPlacementValidation(unittest.TestCase):
    def setUp(self):
        self.board = BlokusBoard(size=20)

        # Create a simple L-shaped piece
        self.piece = BlokusPiece(np.array([
            [1, 0],
            [1, 1]
        ]), Color.BLUE)

    def test_first_move_corner(self):
        # First move must cover a corner
        self.assertTrue(self.board.is_valid_placement(
            self.piece, (0, 0), Color.BLUE, is_first_move=True
        ))

        # First move not covering corner is invalid
        self.assertFalse(self.board.is_valid_placement(
            self.piece, (5, 5), Color.BLUE, is_first_move=True
        ))

    def test_piece_overlap(self):
        # Place a piece at (0, 0)
        self.board.place_piece(self.piece, (0, 0), Color.BLUE)

        # Try to place a piece overlapping with existing piece
        self.assertFalse(self.board.is_valid_placement(
            self.piece, (0, 0), Color.RED, is_first_move=True
        ))

    def test_corner_connectivity(self):
        # Place first piece at corner
        self.board.place_piece(self.piece,