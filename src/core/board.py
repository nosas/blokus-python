import numpy as np

from utils.constants import Color

from .piece import BlokusPiece


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

    def get_corners(self) -> set[tuple[int, int]]:
        """Get the corners of the board."""
        return {
            (0, 0),
            (0, self.size - 1),
            (self.size - 1, 0),
            (self.size - 1, self.size - 1),
        }

    def is_valid_placement(
        self,
        piece: BlokusPiece,
        position: tuple[int, int],
        player_color: Color,
        is_first_move: bool = False,
    ) -> bool:
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
        p_row, p_col = position
        p_shape = piece.get_shape()
        p_height, p_width = piece.get_dimensions()

        # Check 1: Piece must fit on board
        if p_row + p_height > self.size or p_col + p_width > self.size:
            return False

        # Check 2: Piece must not overlap with any existing pieces
        for r in range(p_height):
            for c in range(p_width):
                if p_shape[r, c] == 1:
                    if self.board[p_row + r, p_col + c] != Color.EMPTY.value:
                        return False

        # Check 3: First move must cover a corner
        if is_first_move:
            corners = self.get_corners()
            covers_corner = False

            for r in range(p_height):
                for c in range(p_width):
                    if p_shape[r, c] == 1 and (p_row + r, p_col + c) in corners:
                        covers_corner = True
                        break

            if not covers_corner:
                return False

        # Check 4: Non-first moves must touch at least one own piece at corner and must not
        # touch any own pieces along sides
        else:
            touches_corner = False
            touches_own_side = False
            player_value = player_color.value

            for r in range(p_height):
                for c in range(p_width):
                    if p_shape[r, c] == 1:
                        board_r, board_c = p_row + r, p_col + c

                        # Check corners (diagonal adjacency)
                        corners = {
                            (board_r - 1, board_c - 1),
                            (board_r - 1, board_c + 1),
                            (board_r + 1, board_c - 1),
                            (board_r + 1, board_c + 1),
                        }

                        for cr, cc in corners:
                            if self.is_on_board(cr, cc) and self.board[cr, cc] == player_value:
                                touches_corner = True

                        # Check sides (orthogonal adjacency)
                        sides = [
                            (board_r - 1, board_c),
                            (board_r + 1, board_c),
                            (board_r, board_c - 1),
                            (board_r, board_c + 1),
                        ]

                        for sr, sc in sides:
                            if self.is_on_board(sr, sc) and self.board[sr, sc] == player_value:
                                touches_own_side = True

            if not touches_corner or touches_own_side:
                return False

        return True

    def place_piece(
        self, piece: BlokusPiece, position: tuple[int, int], player_color: Color
    ) -> bool:
        """
        Place a piece on the board.

        Args:
            piece (BlokusPiece): The piece to place
            position (tuple): (row, col) tuple for top-left corner of piece
            player_color (Color): The color of the player making the move

        Returns:
            bool: Whether the piece was successfully placed
        """
        p_row, p_col = position
        p_shape = piece.get_shape()
        p_height, p_width = piece.get_dimensions()

        # Place the piece on the board
        for r in range(p_height):
            for c in range(p_width):
                if p_shape[r, c] == 1:
                    self.board[p_row + r, p_col + c] = player_color.value

        return True

    def get_player_corners(self, player_color: Color) -> set[tuple[int, int]]:
        """
        Get all valid corner positions for a player's pieces.

        Args:
            player_color (Color): The player's color

        Returns:
            list: List of (row, col) tuples for valid corners
        """
        player_value = player_color.value
        corners: set[tuple[int, int]] = set()

        # Scan the entire board
        for r in range(self.size):
            for c in range(self.size):
                # Skip non-empty cells
                if self.board[r, c] != Color.EMPTY.value:
                    continue

                # Check all diagonals for player's pieces
                diagonals = [(r - 1, c - 1), (r - 1, c + 1), (r + 1, c - 1), (r + 1, c + 1)]

                touches_corner = False
                for dr, dc in diagonals:
                    if self.is_on_board(dr, dc) and self.board[dr, dc] == player_value:
                        touches_corner = True
                        break

                # Check all sides for player's pieces
                sides = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]

                touches_side = False
                for sr, sc in sides:
                    if self.is_on_board(sr, sc) and self.board[sr, sc] == player_value:
                        touches_side = True
                        break

                # Valid corner: touches at corner but not at side
                if touches_corner and not touches_side:
                    corners.add((r, c))

        return corners

    def find_valid_placements(
        self, piece: BlokusPiece, player_color: Color, is_first_move: bool = False
    ) -> set[tuple[int, int]]:
        """
        Find all valid placements for a given piece.

        Args:
            piece (BlokusPiece): The piece to place
            player_color (Color): The player's color
            is_first_move (bool): Whether this is the player's first move

        Returns:
            set: Set of valid (row, col) positions
        """
        valid_placements: set[tuple[int, int]] = set()
        positions_to_check: set[tuple[int, int]] = set()

        # For first move, only check the corners
        if is_first_move:
            positions_to_check.update(self.get_corners())
        else:
            # Get all corner positions for this player
            corner_cells = self.get_player_corners(player_color)

            # Expand to all potential placements around these corners
            for cr, cc in corner_cells:
                # Consider positions where the piece might cover this corner
                piece_height, piece_width = piece.get_dimensions()
                for r in range(
                    max(0, cr - piece_height + 1), min(cr + 1, self.size - piece_height + 1)
                ):
                    for c in range(
                        max(0, cc - piece_width + 1), min(cc + 1, self.size - piece_width + 1)
                    ):
                        positions_to_check.add((r, c))

        # Check all potential positions
        for position in positions_to_check:
            if self.is_valid_placement(piece, position, player_color, is_first_move):
                valid_placements.add(position)

        return valid_placements
