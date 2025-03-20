from enum import IntEnum, StrEnum


class Color(IntEnum):
    EMPTY = 0
    BLUE = 1
    YELLOW = 2
    RED = 3
    GREEN = 4

    @classmethod
    def get_player_colors(cls) -> list["Color"]:
        return [cls.BLUE, cls.YELLOW, cls.RED, cls.GREEN]


class Message(StrEnum):
    INVALID_MOVE = "Invalid move"
    PIECE_NOT_FOUND = "Piece not found"
    GAME_OVER = "Game is over"
    SUCCESS = "Success"
