import pytest

from src.core.game import BlokusGame
from src.utils.constants import Color, Message


class TestGameManagement:
    @pytest.fixture
    def game(self) -> BlokusGame:
        return BlokusGame(num_players=4)

    def test_initialization(self, game: BlokusGame):
        assert len(game.players) == 4
        assert game.current_player_idx == 0
        assert game.game_over is False

    def test_current_player(self, game: BlokusGame):
        player = game.get_current_player()
        assert player.color == Color.BLUE
        assert player.player_id == 1

    def test_make_valid_move(self, game: BlokusGame):
        # Get a simple piece (the 1x1 square is always index 0)
        piece_idx = 0
        position = (0, 0)  # Corner position

        success, message = game.make_move(piece_idx, position)
        assert success is True

        # Check move was recorded, player advanced, and first_move flag was updated
        assert len(game.move_history) == 1
        assert game.current_player_idx == 1
        assert game.players[0].first_move is False

    def test_make_invalid_move(self, game: BlokusGame):
        # Try to place at non-corner
        piece_idx = 0
        position = (5, 5)  # Not a corner

        success, message = game.make_move(piece_idx, position)
        assert success is False

        # Check no move was recorded, player did not advance, and first_move flag was not updated
        assert len(game.move_history) == 0
        assert game.current_player_idx == 0
        assert game.players[0].first_move is True

    def test_next_player(self, game: BlokusGame):
        # Place pieces for all players
        for i in range(4):
            game.make_move(0, list(game.board.get_corners())[i])

        # Should wrap back to first player
        assert game.current_player_idx == 0

    def test_can_player_move(self, game: BlokusGame):
        # Initially all players can move
        for i in range(4):
            assert game._can_player_move(i) is True

        # Make first player place all pieces
        player = game.players[0]
        while player.has_pieces_remaining():
            # Remove a piece without placing it
            player.remove_piece(0)

        # Now first player can't move
        assert game._can_player_move(0) is False

    def test_game_over_detection(self, game: BlokusGame):
        """Test that game_over flag is set when no players can move."""
        # Make all players unable to place pieces
        for player in game.players:
            while player.has_pieces_remaining():
                player.remove_piece(0)

        # Force check for next player
        game._next_player()

        # Game should be over
        assert game.game_over is True

    def test_move_with_rotation_and_flip(self, game: BlokusGame):
        """Test making moves with piece rotation and flipping."""
        # Get an L-shaped piece (find appropriate index based on shape)
        # For this test, we'll assume piece at index 1 is L-shaped
        piece_idx = 1

        # Place with rotation
        success, message = game.make_move(piece_idx, (0, 0), rotation=1, flip=False)
        assert success is True

        # Check move was recorded with rotation
        assert game.move_history[-1]["rotation"] == 1
        assert game.move_history[-1]["flip"] is False

        # Place piece for second player with flip
        success, message = game.make_move(0, (0, game.board.size - 1), rotation=0, flip=True)
        assert success is True

        # Check move was recorded with flip
        assert game.move_history[-1]["flip"] is True

    def test_move_history_recording(self, game: BlokusGame):
        """Test that move history records all necessary information."""
        piece_idx = 0
        position = (0, 0)

        success, message = game.make_move(piece_idx, position)
        assert success is True

        # Check move history details
        move_record = game.move_history[0]
        assert move_record["player"] == 1  # Player ID
        assert move_record["position"] == position
        assert "piece_id" in move_record
        assert "rotation" in move_record
        assert "flip" in move_record

    def test_skip_blocked_player(self, game: BlokusGame):
        """Test that the game skips players who cannot make moves."""
        # Make second player unable to place pieces
        player = game.players[1]
        while player.has_pieces_remaining():
            player.remove_piece(0)

        # Make first player's move
        game.make_move(0, (0, 0))

        # Game should skip to third player
        assert game.current_player_idx == 2

    def test_three_player_game(self):
        """Test initialization and function with three players."""
        game = BlokusGame(num_players=3)

        # Should have 3 players
        assert len(game.players) == 3

        # Make moves for all players
        game.make_move(0, (0, 0))  # Player 1
        game.make_move(0, (0, game.board.size - 1))  # Player 2
        game.make_move(0, (game.board.size - 1, 0))  # Player 3

        # Should wrap back to first player
        assert game.current_player_idx == 0

    def test_invalid_piece_index(self, game: BlokusGame):
        """Test behavior with invalid piece indices."""
        # Try with negative index
        success, message = game.make_move(-1, (0, 0))
        assert success is False

        # Try with index beyond available pieces
        large_idx = len(game.players[0].pieces) + 10
        success, message = game.make_move(large_idx, (0, 0))
        assert success is False

    def test_turns_played_counter(self, game: BlokusGame):
        """Test that turns_played gets incremented correctly."""
        assert game.turns_played == 0

        # Make a valid move
        game.make_move(0, (0, 0))
        assert game.turns_played == 1

        # Make another valid move
        game.make_move(0, (0, game.board.size - 1))
        assert game.turns_played == 2

        # Try an invalid move
        game.make_move(0, (5, 5))  # Non-corner for first move
        # Counter should not increment
        assert game.turns_played == 2

    def test_move_when_game_is_over(self, game: BlokusGame):
        """Test that moves are rejected when the game is over."""
        # Manually set game over flag
        game.game_over = True

        # Try to make a move
        success, message = game.make_move(0, (0, 0))

        # Move should be rejected with game over message
        assert success is False
        assert message == Message.GAME_OVER

        # Game state shouldn't change
        assert len(game.move_history) == 0
        assert game.current_player_idx == 0

    def test_error_messages_invalid_move(self, game: BlokusGame):
        """Test that appropriate error messages are returned for invalid moves."""
        # Test invalid move message
        success, message = game.make_move(0, (5, 5))
        assert success is False
        assert message == Message.INVALID_MOVE

    def test_error_messages_game_over(self, game: BlokusGame):
        """Test that appropriate error messages are returned for invalid moves."""
        # Test game over message
        game.game_over = True
        success, message = game.make_move(0, (0, 0))
        assert success is False
        assert message == Message.GAME_OVER

    def test_corner_placement_after_first_move(self, game: BlokusGame):
        """Test that after first move, players can only place at their corners."""
        # Make first move for player 1
        game.make_move(0, (0, 0))

        # Now player 2's turn
        # Try to place at a corner (should succeed)
        player2_piece_idx = 0
        corner_pos = (0, game.board.size - 1)
        success, _ = game.make_move(player2_piece_idx, corner_pos)
        assert success is True

        # Make player 3's move
        game.make_move(0, (game.board.size - 1, 0))

        # Make player 4's move
        game.make_move(0, (game.board.size - 1, game.board.size - 1))

        # Now back to player 1
        # First move flag should be False
        assert game.players[0].first_move is False

        # Should only be able to place connecting to corners
        # Get corners for player 1
        corners = game.board.get_player_corners(Color.BLUE)

        # Try to place at a non-corner (should fail)
        # Choose a position that's definitely not a corner
        non_corner_pos = (5, 5)
        # Verify it's not in corners
        assert non_corner_pos not in corners

        success, _ = game.make_move(0, non_corner_pos)
        assert success is False

    def test_can_player_move_first_move_scenarios(self, game: BlokusGame):
        """Test different scenarios for the can_player_move method with first moves."""
        # Initially all players should be able to move
        for i in range(len(game.players)):
            assert game._can_player_move(i) is True

        # Block all corner positions to prevent first moves
        corners = list(game.board.get_corners())

        # Create some temp players just to place pieces at corners
        for i, corner in enumerate(corners, start=1):
            # This is a bit of a hack, but we're just trying to occupy all corners
            color = Color(i)
            game.board.board[corner[0]][corner[1]] = color.value

        # Now players with first_move=True should not be able to move
        # Since real pieces haven't been placed, we need to manually set first_move
        for player in game.players:
            player.first_move = True

        # Check all players can't move (since corners are blocked)
        for i in range(len(game.players)):
            assert game._can_player_move(i) is False

    def test_complex_cannot_move_scenario(self, game: BlokusGame):
        """Test a more complex scenario where a player with pieces can't move.

        For this test, we need to create a situation where a player has pieces but all their
        corners are blocked.
        """
        # Make first player place at corner
        game.make_move(0, (0, 0))
        # Second player places
        game.make_move(0, (0, game.board.size - 1))

        # Simulate a board state where player has no valid moves
        # This is tricky to set up - we'll mock it by manipulating the board directly
        player2 = game.players[1]
        game.board.board[1][1] = player2.color.value

        assert game._can_player_move(0) is False
