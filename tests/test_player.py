import pytest

from src.core.player import BlokusPlayer
from src.utils.constants import Color


@pytest.fixture()
def player():
    return BlokusPlayer(Color.BLUE, 1)


class TestBlokusPlayer:

    def test_player_initialization(self, player: BlokusPlayer):
        assert player.color == Color.BLUE
        assert player.player_id == 1

    def test_player_initializes_pieces(self, player: BlokusPlayer):
        assert len(player.pieces) == 21

    def test_player_initializes_pieces_with_correct_sizes(self, player: BlokusPlayer):
        sizes = [piece.get_size() for piece in player.pieces]
        ids = [piece.get_piece_id() for piece in player.pieces]
        colors = [piece.get_color() for piece in player.pieces]

        assert sorted(sizes) == [1, 2, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
        assert len(ids) == len(set(ids))
        assert all(color == Color.BLUE for color in colors)

    def test_get_piece(self, player: BlokusPlayer):
        # Get a valid piece
        piece = player.get_piece(0)
        assert piece is not None
        assert piece.get_color() == Color.BLUE

        # Get an invalid piece
        assert player.get_piece(100) is None
        assert player.get_piece(-1) is None

    def test_remove_piece(self, player: BlokusPlayer):
        initial_count = len(player.pieces)

        # Remove a valid piece
        piece = player.remove_piece(0)
        assert piece is not None
        assert len(player.pieces) == initial_count - 1

        # Try to remove an invalid piece
        assert player.remove_piece(100) is None
        assert player.remove_piece(-1) is None
        assert len(player.pieces) == initial_count - 1

    def test_has_pieces_remaining(self, player: BlokusPlayer):
        assert player.has_pieces_remaining() is True

        # Remove all pieces
        initial_count = len(player.pieces)
        for i in range(initial_count):
            player.remove_piece(0)

        assert player.has_pieces_remaining() is False

    def test_get_remaining_piece_count(self, player: BlokusPlayer):
        initial_count = len(player.pieces)
        assert player.get_remaining_piece_count() == initial_count

        # Remove a piece
        player.remove_piece(0)
        assert player.get_remaining_piece_count() == initial_count - 1

    def test_get_pieces_by_size(self, player: BlokusPlayer):
        # Test getting pieces of size 1
        size_1_pieces = player.get_pieces_by_size(1)
        assert len(size_1_pieces) == 1

        # Test getting pieces of size 5
        size_5_pieces = player.get_pieces_by_size(5)
        assert len(size_5_pieces) == 12

        # Test getting pieces of a size that doesn't exist
        size_6_pieces = player.get_pieces_by_size(6)
        assert len(size_6_pieces) == 0

    def test_get_smallest_piece(self, player: BlokusPlayer):
        smallest = player.get_smallest_piece()
        assert smallest is not None
        assert smallest.get_size() == 1

        # Remove all size 1 pieces
        for piece in player.get_pieces_by_size(1):
            player.pieces.remove(piece)

        # Now the smallest should be size 2
        smallest = player.get_smallest_piece()
        assert smallest is not None
        assert smallest.get_size() == 2

        # Test with no pieces
        player.pieces = []
        assert player.get_smallest_piece() is None

    def test_toggle_first_move(self, player: BlokusPlayer):
        assert player.first_move is True
        player.toggle_first_move()
        assert player.first_move is False

        # Trying to toggle again should raise an error
        with pytest.raises(ValueError):
            player.toggle_first_move()
