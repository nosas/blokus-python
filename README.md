# Blokus Python

A Python implementation of the Blokus board game.

## Overview

Blokus is a strategy board game where players place pieces of different shapes on a grid board. Each player starts with 21 polyominoes (shapes made of squares connected edge-to-edge) and takes turns placing them on the board. The goal is to place as many pieces as possible while blocking opponents.

This implementation provides a complete game engine that enforces all Blokus rules and allows for programmatic gameplay.

## Game Rules

Blokus is played on a 20×20 grid with four players, each having 21 pieces of a different color:
- Players take turns placing pieces on the board
- The first piece for each player must cover their starting corner
- Each new piece must touch at least one piece of the same color, but only at the corners (diagonal touch)
- Pieces cannot touch orthogonally (sides) with pieces of the same color
- When a player cannot place any more pieces, they pass their turn
- The game ends when all players can no longer place pieces
- Scoring: Players get points equal to the number of squares in the pieces they placed, with a 15-point bonus if all pieces were placed and an additional 5-point bonus if the smallest piece (1 square) was the last piece placed

## Installation

### Requirements

- Python 3.12+
- UV package manager (recommended)

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/blokus-python.git
   cd blokus-python
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. Install dependencies:
   ```
   uv pip install -e ".[dev]"
   ```

## Usage

### Basic Example

```python
from blokus.core.game import BlokusGame
from blokus.core.player import Player

# Create a new game with 4 players
game = BlokusGame()
game.add_player(Player("Player 1"))
game.add_player(Player("Player 2"))
game.add_player(Player("Player 3"))
game.add_player(Player("Player 4"))

# Start the game
game.start()

# Place a piece (once UI is implemented)
# game.place_piece(player_id, piece_id, row, col, orientation)

# Get the current game state
state = game.get_state()
print(f"Current player: {state.current_player}")
print(f"Board state:\n{state.board}")
```

## Roadmap

The project is being developed in multiple phases:


### Phase 1: Core Game Mechanics

1. Design Board Data Structure (XS)

    - [X] Implement a 2D grid representation (likely 20x20 standard size)
    - [X] Define constants for board dimensions

2. Design Piece Shapes (S)

    - [x] Create data structures for all 21 polyomino shapes per player
    - [ ] Define piece IDs and properties (size, shape)

3. Piece Set Management (XS)

    - [ ] Create data structure to represent a player's set of pieces
    - [ ] Implement methods to track available/used pieces

4. Player Initialization (XS)

    - [ ] Create player objects with color assignment
    - [ ] Assign initial piece sets to players

5. Basic Board Operations (S)

    - [ ] Implement methods to check and update board state
    - [ ] Create piece placement functionality

### Phase 2: Game Rules Implementation

6. First Move Validation (XS)

    - [ ] Implement logic for first move (must cover a corner)

7. Adjacency Rules Implementation (M)

    - [ ] Implement corner-to-corner contact validation
    - [ ] Implement checks to prevent same-color pieces touching sides

8. Valid Move Generation (M)

    - [ ] Create algorithm to find all valid placements for a given piece

9. Piece Manipulation (S)

    - [ ] Implement rotation functionality for pieces
    - [ ] Implement flipping functionality for pieces

### Phase 3: Game Flow

10. Turn Management (S)

    - [ ] Implement player rotation logic
    - [ ] Handle player pass conditions when no moves are available

11. Game End Detection (XS)

    - [ ] Detect when no players can make valid moves
    - [ ] Trigger game end state

12. Basic Scoring Implementation (XS)

    - [ ] Calculate remaining squares scoring
    - [ ] Implement win condition logic

### Phase 4: Basic UI

13. Board Visualization (M)

    - [ ] Create grid rendering system
    - [ ] Implement board state visualization

14. Piece Visualization (M)

    - [ ] Create visual representations for all pieces
    - [ ] Implement basic piece selection

15. Game Controls UI (S)

    - [ ] Create buttons for basic game actions (place piece, pass, etc.)
    - [ ] Add basic scoring display

### Phase 5: Core Game Testing

16. Rule Validation Testing (S)

    - [ ] Create unit tests for all game rules
    - [ ] Test edge cases for placement validation

17. Game Flow Testing (S)

    - [ ] Test complete game scenarios
    - [ ] Validate turn order and management
    - [ ] Test game end conditions

### Phase 6: Enhanced Game Features

18. Advanced Scoring Implementation (XS)

    - [ ] Implement bonus points for placing all pieces
    - [ ] Add extra bonus for playing smallest piece last

19. Player State Tracking (S)

    - [ ] Track placed pieces for each player
    - [ ] Maintain available moves for each player
    - [ ] Track player scores during gameplay

20. Game Variations: Two-Player Mode (S)

    - [ ] Implement controller for two colors per player
    - [ ] Adjust turn order for two-player mode

21. Game Variations: Three-Player Mode (S)

    - [ ] Implement shared color mechanics
    - [ ] Handle the alternating shared color turns

### Phase 7: Enhanced UI

22. Piece Manipulation UI (M)

    - [ ] Implement drag and drop functionality
    - [ ] Add rotation and flipping UI controls
    - [ ] Create preview for piece placement

23. Move Validation Feedback (S)

    - [ ] Add highlighting for valid move spots
    - [ ] Add visual feedback for invalid moves

24. Game Setup UI (S)

    - [ ] Create player selection and configuration screens
    - [ ] Implement game variation selection
    - [ ] Add options for scoring method

25. Feedback and Animation (M)

    - [ ] Implement animations for piece placement
    - [ ] Create end-game summary visuals

### Phase 8: Advanced Features

26. AI Player Implementation (L)

    - [ ] Create basic AI strategy for piece placement
    - [ ] Implement different difficulty levels

27. Game State Persistence (M)

    - [ ] Implement save/load functionality
    - [ ] Create game state serialization

28. Performance Optimization (M)

    - [ ] Benchmark move validation speed
    - [ ] Optimize critical path operations

### Phase 9: Deployment & Operations

29. Documentation (S)

    - [ ] Create developer documentation
    - [ ] Write user manual and tutorials

30. Multiplayer Infrastructure (L) - Optional

    - [ ] Design client-server architecture for online play
    - [ ] Implement game state synchronization

## Development

### Code Style

This project uses:
- Black for code formatting
- isort for import sorting
- Ruff for linting

### Useful Commands

```
# Run all code quality checks
make check

# Format code
make format

# Run tests
make test

# Run tests with coverage
make test-cov
```

## Contributing

Contributions are welcome! Here's how you can contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests to ensure they pass (`make test`)
5. Commit your changes (`git commit -m 'Add some amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

Please make sure your code follows the project's style guidelines by running `make check` and `make format` before submitting.

## Project Structure

```
blokus-python/
├── src/               # Source code
├── tests/             # Test suite
├── docs/              # Documentation
├── pyproject.toml     # Project configuration
├── Makefile           # Development utilities
└── README.md          # This file
```

## License

MIT License