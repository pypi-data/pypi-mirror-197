import abc
from abc import ABC
from math import pi
from typing import Union

from environments import NavigationEnv, GoalReachingNavEnv, MapsIndex
from gym.spaces import Box, Discrete
import numpy as np

from hbrl.environments.environment import Environment


class TurtleEnv(NavigationEnv):
    def __init__(self, map_tag: MapsIndex, reset_anywhere=False):
        state_bounds = np.array([0, 0, 1, 1, 2 * pi])
        state_space = Box(low=-state_bounds, high=state_bounds)
        action_space = Box(-1, 1, (2,))

        super().__init__(map_tag, state_space, action_space, reset_anywhere)

    def reset(self):
        # TODO
        pass
    def step(self, action):
        # TODO
        pass

class GCEnv(Environment, ABC):

    def __init__(self, wrapped_environment, goal_space: Union[None, Box, Discrete]=None):
        self.wrapped_environment = wrapped_environment
        assert isinstance(self.wrapped_environment, Environment)
        self.goal_space = self.state_space if goal_space is None else goal_space
        assert isinstance(self.goal_space, (Box, Discrete))
        self.goal = None
        self.reset()

    def __getattr__(self, name):
        """Returns an attribute with ``name``, unless ``name`` starts with an underscore."""
        if name.startswith("_"):
            raise AttributeError(f"accessing private attribute '{name}' is prohibited")
        return getattr(self.wrapped_environment, name)

    @property
    def goal_size(self):
        return self.goal_space.shape[0]

    def sample_goal(self):
        return self.state_space.sample()

    def reset(self):
        self.wrapped_environment.reset()
        self.goal = self.sample_goal()
        return self.state, self.goal

    @abc.abstractmethod
    def reached(self, state, goal=None) -> bool:
        pass

    @abc.abstractmethod
    def reward(self, state, action, goal=None):
        pass

    def get_goal_from_state(self, state):
        """
        Apply a projection P: S -> G on the given state
        """
        return state

    def get_state_from_goal(self, goal):
        """
        Apply a \bar{P}:G -> S projection on the given state
        """
        return goal


class GoalReachingTurtleEnv(TurtleEnv, GoalReachingNavEnv):

    def __init__(self, map_tag: MapsIndex, reset_anywhere=False):
        wrapped_env = TurtleEnv(map_tag, reset_anywhere)
        GoalReachingNavEnv.__init__(self, wrapped_env)

    def reached(self):
        print("blabla")

    def get_goal_from_state(self, state):
        print("blabla")

    def get_state_from_goal(self, goal):
        print("blabla")

if __name__ == "__main__":
    environment = TurtleEnv(MapsIndex.EMPTY)
    gc_environment = GCNavigationEnv(TurtleEnv, MapsIndex.EMPTY)