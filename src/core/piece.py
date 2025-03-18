import numpy as np

from utils.constants import Color


class BlokusPiece:
    """
    Represents a Blokus game piece.

    Attributes:
        shape (numpy.ndarray): 2D binary array representing the piece's shape
        color (Color): The color of the piece
        piece_id (str): Unique identifier for the piece
    """

    def __init__(self, shape: np.ndarray, color: Color, piece_id: str | None = None):
        if isinstance(shape, list):
            shape = np.array(shape)

        self._original_shape = shape.copy()
        self._shape = shape.copy()
        self._color = color
        self._piece_id = piece_id
        # Calculate the number of squares in the piece
        self._size = np.sum(self._shape)
        # Calculate the shape dimensions
        self._height, self._width = self._shape.shape

    def get_size(self) -> int:
        """Get the number of squares in the piece."""
        return self._size

    def get_shape(self) -> np.ndarray:
        """Get the shape of the piece."""
        return self._shape

    def get_piece_id(self) -> str:
        """Get the piece ID."""
        return self._piece_id or "Unknown"

    def get_color(self) -> Color:
        """Get the color of the piece."""
        return self._color

    def get_dimensions(self) -> tuple[int, int]:
        """Get the dimensions of the piece."""
        return self._height, self._width

    def get_filled_cells(self) -> list[tuple[int, int]]:
        """Get the filled cells of the piece."""
        filled: list[tuple[int, int]] = []
        for row in range(self._height):
            for col in range(self._width):
                if self._shape[row, col] == 1:
                    filled.append((row, col))
        return filled
        # return [tuple(coords) for coords in np.argwhere(self._shape)]

    def rotate(self, rotations: int = 1) -> "BlokusPiece":
        """
        Rotate the piece 90 degrees clockwise, n times.

        Args:
            rotations (int): Number of 90-degree rotations (1-3)

        Returns:
            BlokusPiece: Self, for method chaining
        """
        # np.rot90 rotates counter-clockwise by default, so we use 4-rotations to ensure it is always clockwise
        self._shape = np.rot90(self._shape, k=4 - (rotations % 4))
        self._height, self._width = self._shape.shape
        return self

    def flip(self) -> "BlokusPiece":
        """
        Flip the piece horizontally (left-to-right, not up-to-down)

        Returns:
            BlokusPiece: Self, for method chaining
        """
        self._shape = np.fliplr(self._shape)
        return self

    def reset_orientation(self) -> "BlokusPiece":
        """
        Reset the piece to its original orientation.

        Returns:
            BlokusPiece: Self, for method chaining
        """
        self._shape = self._original_shape.copy()
        self._height, self._width = self._shape.shape
        return self

    def get_all_orientations(self) -> list[np.ndarray]:
        """
        Generate all unique orientations of this piece.

        Returns:
            list: List of shape arrays (numpy arrays)
        """
        orientations = []
        seen_shapes = set()

        # Save original orientation
        original = self._shape.copy()

        # Try all combinations of rotations and flips
        for flip in [False, True]:
            if flip:
                self.flip()

            for rotation in range(4):
                if rotation > 0:
                    self.rotate()

                # Convert shape to hashable format
                shape_tuple = tuple(map(tuple, self._shape))

                # Only add if this is a new unique orientation
                if shape_tuple not in seen_shapes:
                    seen_shapes.add(shape_tuple)
                    orientations.append(self._shape.copy())

        # Restore original orientation
        self._shape = original
        self._height, self._width = self._shape.shape

        return orientations
