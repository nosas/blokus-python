from enum import Enum


class Color(Enum):
    EMPTY = 0
    BLUE = 1
    YELLOW = 2
    RED = 3
    GREEN = 4

    @classmethod
    def get_player_colors(cls) -> list["Color"]:
        return [cls.BLUE, cls.YELLOW, cls.RED, cls.GREEN]
