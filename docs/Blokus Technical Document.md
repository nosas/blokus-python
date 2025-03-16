# Blokus Implementation Technical Document

## Executive Summary

This document outlines a comprehensive technical approach for implementing the board game Blokus in Python. The project will be developed over an 8-week timeline (with optional extensions) and will include core game mechanics, a playable interface, AI opponents of varying sophistication, and potential networking capabilities. This implementation will prioritize clean architecture, separation of concerns, and extensibility.

## 1. Project Objectives

- Create a feature-complete digital version of the Blokus board game
- Implement rule-enforcing game mechanics
- Develop intuitive user interface controls for piece manipulation
- Build AI opponents with multiple difficulty levels
- Support both single-player and multiplayer gameplay
- Ensure code quality, maintainability, and extensibility

## 2. Technical Architecture

### 2.1 Core Components

#### 2.1.1 Board Representation
- A 20×20 grid implemented using NumPy arrays for efficient operations
- Cell values will store player identifiers (0 for empty, 1-4 for players)
- Coordinate system: (0,0) at top-left, increasing right and down

```python
class BlokusBoard:
    def __init__(self, size=20):
        self.size = size
        self.board = np.zeros((size, size), dtype=int)
```

#### 2.1.2 Piece Representation
- Each piece defined as a 2D binary NumPy array (1s for filled squares)
- Piece class will encapsulate transformation operations
- Default piece set will include all 21 standard Blokus pieces for each player

```python
class BlokusPiece:
    def __init__(self, shape, color, piece_id=None):
        self.original_shape = shape.copy()
        self.shape = shape.copy()
        self.color = color
        self.piece_id = piece_id
        self.size = np.sum(shape)  # Number of squares
```

#### 2.1.3 Game State Manager
- Handles turn management and game rules enforcement
- Tracks player states, available pieces, and game phase
- Manages game progression and scoring

```python
class BlokusGame:
    def __init__(self, num_players=4):
        self.board = BlokusBoard()
        self.players = []
        self.current_player_idx = 0
        self.game_over = False
```

#### 2.1.4 User Interface Layer
- Separates presentation from game logic
- Provides methods for piece selection, orientation, and placement
- Handles rendering and user input processing

### 2.2 Data Flow

1. User/AI selects a piece from inventory
2. System presents legal orientations and placement options
3. User/AI chooses final orientation and position
4. System validates move against game rules
5. If valid, system updates board state and player inventory
6. System advances to next player's turn
7. Cycle repeats until game termination conditions are met

### 2.3 Technology Stack

- **Core Language**: Python 3.8+
- **Numerical Processing**: NumPy
- **UI Framework**: TBD based on requirements (Pygame, Tkinter, or web-based)
- **Testing Framework**: pytest
- **Optional Database**: SQLite for game state persistence
- **Optional Networking**: WebSockets for multiplayer support

## 3. Implementation Details

### 3.1 Board and Piece System

#### 3.1.1 Piece Transformations
All pieces must support the following transformations:
- Rotation (90° increments)
- Horizontal/vertical flipping
- Reset to original orientation

Implementation will use NumPy's built-in transformation functions:
```python
def rotate(self, rotations=1):
    self.shape = np.rot90(self.shape, k=4-rotations)  # Counter-clockwise by default
    return self

def flip(self):
    self.shape = np.fliplr(self.shape)
    return self
```

#### 3.1.2 Move Validation
The system must enforce all Blokus rules:
- First move for each player must cover a board corner
- Subsequent moves must touch at least one existing same-color piece at corners
- No same-color pieces can touch along sides
- No piece can overlap with any existing piece

```python
def is_valid_placement(self, piece, position, player_id, is_first_move=False):
    # 1. Check if piece fits on board
    # 2. Check for overlaps with existing pieces
    # 3. Verify first-move corner placement if applicable
    # 4. Check corner connectivity and side restrictions
```

#### 3.1.3 Corner Tracking
For efficiency, the system will maintain a set of valid corners for each player:
```python
def update_player_corners(self, player_id, piece, position):
    # After placing a piece, update the set of valid corners for this player
```

### 3.2 AI System Architecture

#### 3.2.1 Bot Interface
All AI players will implement a common interface:
```python
class BlokusBot:
    def get_move(self, game_state):
        """
        Returns a tuple of (piece_idx, position, rotation, flip)
        """
        pass
```

#### 3.2.2 Heuristic Evaluation System
Core evaluation functions that will power the rule-based AI:

```python
def evaluate_board_state(game_state, move=None, weights=None):
    # Apply weighted heuristics to generate a composite score:
    # - Territory control
    # - Corner availability
    # - Piece efficiency
    # - Opponent blocking
    # - Board coverage balance
    # - Endgame piece fitting
```

#### 3.2.3 Dynamic Strategy Selection
The stronger bots will select strategies based on game phase and position:

```python
def select_strategy(self, game_state):
    phase = self._determine_game_phase(game_state)
    position = self._assess_position(game_state)
    
    # Select strategy (expansion, defensive, efficient, balanced)
    # based on game phase and position
```

### 3.3 User Interface Implementation

#### 3.3.1 Piece Selection and Manipulation
The UI will provide controls for:
- Selecting pieces from inventory
- Rotating and flipping selected pieces
- Previewing piece placement before confirming

#### 3.3.2 Visual Feedback
The system will provide visual cues for:
- Valid and invalid placement positions
- Corner availability
- Potential moves and their outcomes

#### 3.3.3 Game State Visualization
The UI must clearly show:
- Current board state
- Player inventories
- Turn information
- Score tracking

## 4. Implementation Timeline

### 4.1 Phase 1: Core Game Engine (Weeks 1-2)

#### Week 1: Data Models and Basic Mechanics
| Day | Tasks | Deliverables | Technical Details |
|-----|-------|--------------|-------------------|
| 1-2 | Define board and piece data structures | BlokusBoard and BlokusPiece classes | Using NumPy arrays for efficient operations |
| 3-4 | Implement piece transformations | Rotation and flipping methods | Handle edge cases for non-rectangular pieces |
| 5-7 | Create standard piece set | Complete set of 21 piece definitions | Include metadata for identification and visualization |

#### Week 2: Game Rules and Flow
| Day | Tasks | Deliverables | Technical Details |
|-----|-------|--------------|-------------------|
| 1-3 | Implement placement validation | Complete rule enforcement system | Rigorous testing of all game rules |
| 4-5 | Build turn management | Game flow control and player rotation | Support for handling invalid moves and skipped turns |
| 6-7 | Create scoring and end-game detection | Scoring algorithms and game termination | Implement both basic and advanced scoring modes |

**Milestone 1**: Functional game engine with complete rule enforcement

### 4.2 Phase 2: Basic UI and Gameplay (Weeks 3-4)

#### Week 3: Playable Interface
| Day | Tasks | Deliverables | Technical Details |
|-----|-------|--------------|-------------------|
| 1-3 | Implement piece selection controls | Interactive piece inventory | Support for keyboard and mouse interaction |
| 4-5 | Create board visualization | Visual representation of game state | Clear distinction between players and empty cells |
| 6-7 | Integrate game state with UI | Complete input/output system | Ensure consistent state between model and view |

#### Week 4: Gameplay Polish
| Day | Tasks | Deliverables | Technical Details |
|-----|-------|--------------|-------------------|
| 1-2 | Add move feedback | Visual cues for legal/illegal moves | Highlight affected cells and error messages |
| 3-4 | Implement undo/redo | Move history and state restoration | Use command pattern for action tracking |
| 5-7 | Add save/load functionality | Game state serialization | JSON format for compatibility and readability |

**Milestone 2**: Fully playable game with basic UI

### 4.3 Phase 3: AI Players (Weeks 5-6)

#### Week 5: Basic AI Implementation
| Day | Tasks | Deliverables | Technical Details |
|-----|-------|--------------|-------------------|
| 1-3 | Create heuristic functions | Core evaluation metrics | Optimize for efficient calculation |
| 4-7 | Build rule-based bot | First functional AI player | Use composite scoring approach |

#### Week 6: Enhanced AI Capabilities
| Day | Tasks | Deliverables | Technical Details |
|-----|-------|--------------|-------------------|
| 1-3 | Implement phase-specific strategies | Strategic adaptation system | Separate early, mid, and endgame behaviors |
| 4-5 | Add position-based adaptations | Dynamic strategy selection | Adjust based on winning/losing position |
| 6-7 | Create testing framework | AI evaluation system | Metrics for bot performance comparison |

**Milestone 3**: Functional AI opponents with varying strategies

### 4.4 Phase 4: Advanced Features (Weeks 7-8)

#### Week 7: Game Variants and AI Improvements
| Day | Tasks | Deliverables | Technical Details |
|-----|-------|--------------|-------------------|
| 1-3 | Add variant support | Blokus Duo and Trigon modes | Configurable rule sets and board sizes |
| 4-7 | Implement MCTS-based bot | Stronger AI player | Optimized tree search with pruning |

#### Week 8: Final Polish and Infrastructure
| Day | Tasks | Deliverables | Technical Details |
|-----|-------|--------------|-------------------|
| 1-3 | Create bot arena | Automated testing environment | Tournament and league systems |
| 4-5 | Performance optimization | Improved execution speed | Profile and optimize critical paths |
| 6-7 | Documentation and cleanup | Complete code documentation | Include developer and user guides |

**Milestone 4**: Complete game with multiple AI difficulty levels

### 4.5 Phase 5: Optional Enhancements (Weeks 9-10+)

- Network multiplayer support
- Tournament and ranking system
- Advanced game statistics and visualization
- Reinforcement learning-based AI (if resources permit)

## 5. Technical Implementation Guidelines

### 5.1 Code Organization

```
blokus/
├── core/
│   ├── board.py       # Board representation and operations
│   ├── piece.py       # Piece definitions and transformations
│   ├── game.py        # Game state and rules management
│   └── player.py      # Player state tracking
├── ai/
│   ├── bot_interface.py     # Common bot interface
│   ├── heuristics.py        # Evaluation functions
│   ├── rule_based_bot.py    # Simple rule-based AI
│   ├── strategic_bot.py     # Advanced strategy-based AI
│   └── mcts_bot.py          # Monte Carlo Tree Search implementation
├── ui/
│   ├── renderer.py          # Game state visualization
│   ├── input_handler.py     # User input processing
│   └── game_interface.py    # UI integration with game logic
├── utils/
│   ├── serialization.py     # Save/load functionality
│   ├── piece_data.py        # Standard piece definitions
│   └── testing.py           # Testing utilities
└── main.py                  # Application entry point
```

### 5.2 Coding Standards

- Follow PEP 8 style guidelines
- Use type hints for improved readability and IDE support
- Document all public methods with docstrings
- Maintain test coverage of at least 80% for core functionality
- Use meaningful variable names that reflect domain concepts

### 5.3 Performance Considerations

- Optimize move validation for speed (critical path)
- Cache piece orientations to avoid redundant calculations
- Use NumPy vectorized operations where possible
- Implement efficient corner tracking to reduce search space
- Consider parallelization for AI move calculation

### 5.4 Testing Strategy

- Unit tests for all core game mechanics
- Integration tests for complete game flow
- AI bot tournament testing for performance evaluation
- Edge case validation for complex rule interactions
- Performance benchmarking for optimization verification

## 6. Risk Assessment and Mitigation

| Risk | Probability | Impact | Mitigation Strategy |
|------|------------|--------|---------------------|
| Complex rule implementation bugs | High | Medium | Comprehensive test suite, formal verification of core rules |
| Performance bottlenecks in AI | Medium | High | Incremental optimization, profiling-guided improvements |
| UI responsiveness issues | Medium | Medium | Separate rendering thread, throttle visualization updates |
| Scope creep beyond essential features | High | Medium | Strict prioritization, phased deliverables, clear milestone criteria |
| Technical debt from rapid implementation | Medium | High | Regular refactoring sessions, code reviews, maintainability metrics |

## 7. Key Interfaces and APIs

### 7.1 Game Engine API

```python
# Core game manipulation
game.initialize()
game.place_piece(piece_idx, position, rotation, flip)
game.is_valid_move(piece_idx, position, rotation, flip)
game.get_valid_moves()
game.get_game_state()
game.get_current_player()

# Game flow control
game.next_turn()
game.is_game_over()
game.get_scores()
```

### 7.2 Bot Interface

```python
# Required methods for all bots
bot.get_move(game_state)
bot.get_name()

# Optional methods for advanced bots
bot.update_strategy(game_state)
bot.analyze_opponents(move_history)
```

### 7.3 UI Handler Interface

```python
# UI interaction
ui.select_piece(piece_idx)
ui.rotate_piece()
ui.flip_piece()
ui.preview_placement(position)
ui.confirm_placement(position)

# State visualization
ui.render_board(board_state)
ui.render_inventory(player_pieces)
ui.render_scores(player_scores)
ui.show_feedback(message, message_type)
```

## 8. Data Structures

### 8.1 Game State

```python
{
    "board": 2D array (20x20),
    "current_player": int,
    "players": [
        {
            "id": int,
            "color": Color enum,
            "pieces": [BlokusPiece objects],
            "first_move": bool,
            "score": int
        },
        # Additional players...
    ],
    "turns_played": int,
    "game_over": bool
}
```

### 8.2 Move Representation

```python
{
    "piece_idx": int,      # Index in player's inventory
    "position": (row, col),  # Top-left position on board
    "rotation": int,        # 0-3 (90° increments)
    "flip": bool,           # Horizontal flip
    "player_id": int        # Player making the move
}
```

### 8.3 Piece Inventory

Initial set of 21 pieces per player, with decreasing inventory as game progresses.

## 9. Extension Points

The implementation includes several planned extension points for future enhancements:

1. **Game Variant Support**: Configuration system for board size, starting positions, and rule variations
2. **AI Strategy Plugins**: Framework for adding new AI strategies without modifying core code
3. **UI Theme System**: Customizable visual presentation via themes
4. **Networking Layer**: Abstract interface for local vs. remote gameplay
5. **Analytics Module**: Hook points for collecting and analyzing game statistics

## 10. Conclusion

This technical document provides a comprehensive blueprint for implementing Blokus in Python. The 8-week timeline delivers a complete solution with core game mechanics, playable interface, and multiple AI opponents. The architecture emphasizes clean separation of concerns, extensibility, and performance optimization where critical.

By following this implementation plan, the development team will create a robust, maintainable Blokus application capable of serving as both an enjoyable game and a platform for AI experimentation and enhancement.

## Appendix A: Standard Piece Definitions

```python
def create_standard_piece_set():
    """Create the standard 21 Blokus pieces as numpy arrays."""
    pieces = []
    
    # 1-square piece (monomino)
    pieces.append(np.array([[1]]))
    
    # 2-square piece (domino)
    pieces.append(np.array([[1, 1]]))
    
    # 3-square pieces (trominoes)
    pieces.append(np.array([[1, 1, 1]]))  # I
    pieces.append(np.array([[1, 1],
                           [1, 0]]))      # L
    
    # 4-square pieces (tetrominoes)
    pieces.append(np.array([[1, 1, 1, 1]]))  # I
    pieces.append(np.array([[1, 1, 1],
                           [1, 0, 0]]))      # L
    pieces.append(np.array([[1, 1, 0],
                           [0, 1, 1]]))      # Z
    pieces.append(np.array([[1, 1],
                           [1, 1]]))         # O
    pieces.append(np.array([[1, 1, 1],
                           [0, 1, 0]]))      # T
    
    # 5-square pieces (pentominoes) - all 12 of them
    # ... (detailed definitions provided in code)
    
    return pieces
```

## Appendix B: Glossary of Terms

| Term | Definition |
|------|------------|
| **Blokus** | A strategy board game for 2-4 players where players place pieces on a grid, touching only at corners |
| **Piece** | A polyomino shape composed of 1-5 connected squares that players place on the board |
| **Corner** | A point where the corners of four cells meet, used for connecting pieces of the same color |
| **First move** | Each player's first piece must cover one of the board's corner cells |
| **Valid placement** | A piece position that follows all game rules (corner connectivity, no side touching, etc.) |
| **Phase** | A stage of the game (opening, middle, endgame) with different strategic priorities |
| **Heuristic** | An evaluation function that scores board positions based on strategic criteria |
| **MCTS** | Monte Carlo Tree Search, an algorithm for decision making used in advanced AI |
