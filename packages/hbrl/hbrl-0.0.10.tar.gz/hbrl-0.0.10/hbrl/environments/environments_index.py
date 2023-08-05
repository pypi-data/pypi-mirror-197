from enum import Enum

ant_maze = False
try:
    import mujoco_py
    ant_maze = True
except ImportError:
    pass

class EnvironmentIndex(Enum):
    GRID_WORLD = "grid_world"
    POINT_MAZE = "point_maze"
    if ant_maze:
        ANT_MAZE = "ant_maze"
