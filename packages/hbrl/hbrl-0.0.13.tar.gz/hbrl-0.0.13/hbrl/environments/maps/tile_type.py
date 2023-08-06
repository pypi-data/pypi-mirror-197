from enum import Enum


class TileType(Enum):
    EMPTY = 0
    WALL = 1
    START = 2
    REWARD = 3
    TERMINAL_FAIL = 4