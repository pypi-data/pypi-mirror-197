from .environments_index import EnvironmentIndex
from .maps.maps_index import MapsIndex
from .grid_world import *
from .point_env import *

# Import ant maze ONLY if mujoco_py is installed
try:
    from .ant_maze import AntMaze
except ImportError:
    pass

from .environment import Environment
from .goal_reaching_environment import GoalReachingEnv
from .navigation_environment import NavigationEnv, GoalReachingNavEnv
