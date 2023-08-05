from enum import Enum


class MapsIndex(Enum):
    EMPTY = "empty_room"
    FOUR_ROOMS = "four_rooms"
    HARD = "hard_maze"
    MEDIUM = "medium_maze"
    EXTREME = "extreme_maze"
    IMPOSSIBLE = "impossible_maze"
    SORB_4_ROOMS = "four_rooms_sorb"
    JOIN_ROOMS = "join_rooms_medium"
