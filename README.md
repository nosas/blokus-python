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

### Phase 1: Core Game Engine (2 weeks)
- **Week 1: Data Models and Basic Mechanics**
  - Board and piece data structures
  - Piece transformations (rotation, flipping)
  - Standard piece set implementation
- **Week 2: Game Rules and Flow**
  - Placement validation
  - Turn management
  - Scoring and end-game detection

### Phase 2: User Interface (2 weeks)
- Command-line interface
- Graphical user interface
- Piece manipulation controls

### Phase 3: AI Opponents (2 weeks)
- Basic rule-following AI
- Intermediate strategic AI
- Advanced AI with lookahead

### Phase 4: Multiplayer and Polish (2 weeks)
- Network play implementation
- Performance optimizations
- Final polish and bug fixes

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