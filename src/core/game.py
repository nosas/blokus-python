from utils.constants import Color, Message

from .board import BlokusBoard
from .piece import BlokusPiece
from .player import BlokusPlayer


class BlokusGame:
    """
    Main game class controlling Blokus gameplay.

    Attributes:
        board (BlokusBoard): The game board
        players (list): List of BlokusPlayer objects
        current_player_idx (int): Index of the current player
        move_history (list): List of all moves made
        game_over (bool): Whether the game has ended
    """

    def __init__(self, num_players: int = 4):
        self.board = BlokusBoard()
        self.players: list[BlokusPlayer] = []
        self.current_player_idx: int = 0
        self.move_history: list[dict] = []
        self.game_over: bool = False
        self.turns_played: int = 0

        # Initialize players
        player_colors = Color.get_player_colors()
        for i in range(min(num_players, 4)):
            self.players.append(BlokusPlayer(player_colors[i], i + 1))

    def get_current_player(self) -> BlokusPlayer:
        return self.players[self.current_player_idx]

    def make_move(
        self, piece_idx: int, position: tuple[int, int], rotation: int = 0, flip: bool = False
    ) -> tuple[bool, str]:
        """
        Execute a move if valid.

        Args:
            piece_idx (int): Index of the piece in the player's inventory
            position (tuple): (row, col) tuple for placement
            rotation (int): Number of 90-degree rotations (0-3)
            flip (bool): Whether to flip the piece

        Returns:
            bool: Whether the move was successfully executed
        """
        if self.game_over:
            return False, Message.GAME_OVER

        if not self.is_valid_move(piece_idx, position, rotation, flip):
            return False, Message.INVALID_MOVE

        player = self.get_current_player()

        # Get piece and apply transformations
        piece = player.get_piece(piece_idx)

        if piece is None:
            # NOTE: This code should never be reached, but it's here to satisfy the type checker
            return False, Message.PIECE_NOT_FOUND

        # Make a copy of the piece to avoid modifying the original
        temp_piece = BlokusPiece(piece.get_shape(), player.color, piece.get_piece_id())

        # Apply transformations
        if rotation > 0:
            temp_piece.rotate(rotation)
        if flip:
            temp_piece.flip()

        # Place the piece on the board
        self.board.place_piece(temp_piece, position, player.color)

        # Remove the piece from the player's inventory
        player.remove_piece(piece_idx)

        # Record the move
        self.move_history.append(
            {
                "player": player.player_id,
                "piece_id": piece.get_piece_id(),
                "position": position,
                "rotation": rotation,
                "flip": flip,
            }
        )

        # Update first_move flag
        player.first_move = False

        # Increment turns played
        self.turns_played += 1

        # Move to next player
        self._next_player()

        return True, Message.SUCCESS

    def is_valid_move(
        self, piece_idx: int, position: tuple[int, int], rotation: int = 0, flip: bool = False
    ) -> bool:
        """
        Check if a move is valid.

        A move is valid if:

        - The piece is in the player's inventory
        - The piece is not already on the board
        - The piece is not off the board
        - The piece is not overlapping another piece
        - The piece is not outside the board's boundaries
        - The piece is not rotated or flipped in a way that would cause it to overlap another piece

        Args:
            piece_idx (int): Index of the piece in the player's inventory
            position (tuple): (row, col) tuple for placement
            rotation (int): Number of 90-degree rotations (0-3)
            flip (bool): Whether to flip the piece

        Returns:
            bool: Whether the move is valid
        """
        player = self.get_current_player()

        # Get piece and apply transformations
        piece = player.get_piece(piece_idx)

        if piece is None:
            return False

        # Make a copy of the piece to avoid modifying the original
        temp_piece = BlokusPiece(piece.get_shape(), player.color, piece.get_piece_id())

        # Apply transformations
        if rotation > 0:
            temp_piece.rotate(rotation)
        if flip:
            temp_piece.flip()

        # Check if placement is valid
        return self.board.is_valid_placement(temp_piece, position, player.color, player.first_move)

    def _next_player(self) -> None:
        """Advance to the next player who can make a move."""
        original_player = self.current_player_idx
        players_checked = 0

        while players_checked < len(self.players):
            # Move to next player
            self.current_player_idx = (self.current_player_idx + 1) % len(self.players)
            players_checked += 1

            # If this player has pieces and can play, break
            if self._can_player_move(self.current_player_idx):
                return

        # If we've checked all players and none can move, game is over
        self.game_over = True

        # Revert to original player for final state
        self.current_player_idx = original_player

    def _can_player_move(self, player_idx: int) -> bool:
        """
        Check if a player can make any valid move.

        A player can make a move if:

        - They have pieces remaining
        - They have not made their first move yet
        - They have pieces that can be placed on the board
        - The piece is not rotated or flipped in a way that would cause it to overlap another piece

        Args:
            player_idx (int): Player index to check

        Returns:
            bool: Whether the player can make any move
        """
        player = self.players[player_idx]

        # If player has no pieces, they can't move
        if not player.has_pieces_remaining():
            return False

        # For first move, check if any piece can be placed at any corner
        if player.first_move:
            for corner in self.board.get_corners():
                for piece in player.pieces:
                    # Try all orientations
                    for flip in [False, True]:
                        temp_piece = BlokusPiece(piece.get_shape(), player.color)
                        if flip:
                            temp_piece.flip()

                        for rotation in range(4):
                            if rotation > 0:
                                temp_piece.rotate()

                            # If any orientation works, player can move
                            if self.board.is_valid_placement(
                                temp_piece, corner, player.color, True
                            ):
                                return True
            return False

        # For subsequent moves, check if any piece can be placed at any valid corner
        corners = self.board.get_player_corners(player.color)

        if not corners:
            return False

        # For each corner, check if any piece in any orientation can be placed
        for corner in corners:
            for piece in player.pieces:
                # Try each orientation
                for flip in [False, True]:
                    temp_piece = BlokusPiece(piece.get_shape(), player.color)
                    if flip:
                        temp_piece.flip()

                    for rotation in range(4):
                        if rotation > 0:
                            temp_piece.rotate()

                        # Check all possible positions that might cover this corner
                        piece_height, piece_width = temp_piece.get_dimensions()
                        for r_offset in range(piece_height):
                            for c_offset in range(piece_width):
                                pos_r = corner[0] - r_offset
                                pos_c = corner[1] - c_offset

                                # If piece would be off board, skip
                                if pos_r < 0 or pos_c < 0:
                                    continue

                                # If this placement works, player can move
                                if self.board.is_valid_placement(
                                    temp_piece, (pos_r, pos_c), player.color, False
                                ):
                                    return True

        # If no valid moves found, player cannot move
        return False
