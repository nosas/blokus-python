from utils.constants import Color
from utils.piece_data import get_standard_piece_shapes

from .piece import BlokusPiece


class BlokusPlayer:
    """
    Represents a player in the Blokus game.

    Attributes:
        color (Color): The player's color
        pieces (list): List of BlokusPiece objects available to the player
        first_move (bool): Whether this is the player's first move
        player_id (int): Numeric ID for the player (1-4)
    """

    def __init__(self, color: Color, player_id: int):
        self.color: Color = color
        self.player_id: int = player_id
        self.first_move: bool = True
        self.pieces: list[BlokusPiece] = []
        self.initialize_pieces()

    def initialize_pieces(self) -> None:
        """Initialize the standard set of 21 Blokus pieces."""
        self.pieces = []
        piece_shapes = get_standard_piece_shapes()

        for piece_data in piece_shapes:
            piece = BlokusPiece(
                shape=piece_data["shape"],
                color=self.color,
                piece_id=piece_data["id"],
            )
            self.pieces.append(piece)

    def get_piece(self, index: int) -> BlokusPiece | None:
        """Get a piece by index."""
        if 0 <= index < len(self.pieces):
            return self.pieces[index]
        return None

    def remove_piece(self, index: int) -> BlokusPiece | None:
        """Remove a piece from the player's inventory."""
        if 0 <= index < len(self.pieces):
            return self.pieces.pop(index)
        return None

    def has_pieces_remaining(self) -> bool:
        """Check if the player has any pieces remaining."""
        return len(self.pieces) > 0

    def get_remaining_piece_count(self) -> int:
        """Get the number of pieces remaining."""
        return len(self.pieces)

    def get_pieces_by_size(self, size: int) -> list[BlokusPiece]:
        """Get all pieces of a specific size."""
        return [p for p in self.pieces if p.get_size() == size]

    def get_smallest_piece(self) -> BlokusPiece | None:
        """Get the smallest remaining piece."""
        if not self.pieces:
            return None
        return min(self.pieces, key=lambda p: p.get_size())

    def toggle_first_move(self) -> None:
        """Toggle the first move flag."""
        if self.first_move is True:
            self.first_move = False
        else:
            raise ValueError("First move flag is already set.")
