import numpy as np

from src.core.game import BlokusGame
from src.core.piece import BlokusPiece


def print_board(board):
    """Print a text representation of the board with colored pieces."""
    # ANSI color codes
    colors = {
        0: "\033[0m·",  # Reset + dot for empty
        1: "\033[94mB\033[0m",  # Blue
        2: "\033[93mY\033[0m",  # Yellow
        3: "\033[91mR\033[0m",  # Red
        4: "\033[92mG\033[0m",  # Green
    }

    for row in board:
        print(" ".join(colors[cell] for cell in row))


def demo_game():
    """Run a simple demo of the Blokus game engine."""
    print("Initializing Blokus game...")
    num_players = 4
    game = BlokusGame(num_players=num_players)
    player_names = ["Blue", "Yellow", "Red", "Green"]

    # Place first pieces for all players
    corners = game.board.get_corners()
    for i in range(num_players):
        player = game.get_current_player()
        print(f"\n{player_names[i]} player's turn")
        # print(f"Press Enter to place first piece at {corners[i]}...")
        # input()
        success, message = game.make_move(0, corners[i])
        if not success:
            print(f"Error: {message}")
            return
        print_board(game.board.board)

    print("\nBoard after first moves:")
    print_board(game.board.board)

    # Make additional moves until game is over
    while not game.game_over:
        player = game.get_current_player()
        player_name = player_names[game.current_player_idx]

        print(f"\n{player_name} player's turn")
        # print("Press Enter to make a move...")
        # input()

        # Try pieces in random order until finding a valid placement
        available_pieces = list(range(len(player.pieces)))
        np.random.shuffle(available_pieces)

        move_made = False
        for piece_idx in available_pieces:
            piece = player.get_piece(piece_idx)

            # Randomly choose orientation
            rotation = np.random.randint(0, 4)  # Random rotation 0-3
            flip = bool(np.random.choice([True, False]))  # Random flip

            # Create a new piece instance with random orientation
            temp_piece = BlokusPiece(piece.get_shape(), player.color, piece.get_piece_id())
            if rotation > 0:
                temp_piece.rotate(rotation)
            if flip:
                temp_piece.flip()

            # Find all valid placements for this orientation
            valid_placements = game.board.find_valid_placements(temp_piece, player.color)

            if valid_placements:
                valid_placements_list = list(valid_placements)
                position = valid_placements_list[np.random.randint(0, len(valid_placements_list))]

                # Make the move
                success, message = game.make_move(piece_idx, position, rotation, flip)
                if success:
                    print(
                        f"{player_name} player placed piece {piece_idx} at {position} "
                        f"(rotation: {rotation}, flip: {flip})"
                    )
                    print_board(game.board.board)
                    move_made = True
                    break
                else:
                    print(f"Unexpected error: {message}")
            if move_made:
                break

        if not move_made:
            print(f"{player_name} player couldn't place any pieces, skipping turn")

    print("\nGame Over!")
    print("Final board:")
    print_board(game.board.board)

    # Print final scores (lower is better - counts remaining squares)
    scores = []
    for i, player in enumerate(game.players):
        score = sum(piece.get_size() for piece in player.pieces)
        scores.append(score)
        print(f"{player_names[i]} score: {score}")

    # Print the winner
    winner = player_names[np.argmin(scores)]
    print(f"\n{winner} wins!")

    print(f"Move history: {game.move_history}")


if __name__ == "__main__":
    demo_game()
