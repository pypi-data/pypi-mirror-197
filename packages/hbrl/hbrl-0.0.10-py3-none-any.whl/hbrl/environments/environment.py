import abc
import copy
from typing import Union
from warnings import warn

import numpy as np
from gym.spaces import Box, Discrete
from abc import ABC


class Environment(ABC):

    name = "Default Environment"

    def __init__(self, state_space: Union[Box, Discrete], action_space: Union[Box, Discrete]):
        assert len(state_space.shape) == 1, "Environments with state space with multiple dimensions are not supported. " \
                                            "Flatten your state space or use another library."
        assert isinstance(state_space, Box) or isinstance(state_space, Discrete), \
            "State spaces with a different type than gym.spaces.Box or gym.spaces.Discrete ar not supported."
        self.state_space = state_space
        self.state_size = state_space.shape[0] if isinstance(state_space, Box) else state_space.n
        self.state_space_bounds = self.state_space.high
        self.state_space_offset = (self.state_space.high + self.state_space.low) / 2

        assert len(action_space.shape) == 1, "Environments with action space with multiple dimensions are not supported. " \
                                            "Flatten your action space or use another library."
        assert isinstance(action_space, Box) or isinstance(action_space, Discrete), \
            "Action spaces with a different type than gym.spaces.Box or gym.spaces.Discrete ar not supported."
        self.action_space = action_space
        self.nb_actions = action_space.shape[0] if isinstance(action_space, Box) else action_space.n
        self.action_space_bounds = self.action_space.high
        self.action_space_offset = (self.action_space.high + self.action_space.low) / 2

        self.episode_duration = 0  # Nb steps taken in the current episode
        self.state = None
        self.reset()

    def reset(self) -> np.ndarray:
        self.state = self.state_space.sample()
        self.episode_duration = 0
        return self.state

    def step(self, action: np.ndarray) -> (np.ndarray, float, bool):
        assert self.action_space.contains(action.astype(self.action_space.dtype))
        if not self.action_space.contains(action):
            warn("Environment received an action with stata-type" + str(action.dtype) +
                 " where its action space data-type is " + str(self.action_space.dtype) + ".")

        self.episode_duration += 1

        return np.random.rand(), 0.0, False

    @abc.abstractmethod
    def render(self) -> np.ndarray:
        """
        Return a numpy array that represent an image (with shape (_, _, 3)) of the environment in its current state.
        """
        pass

    def copy(self):
        """
        Returns a copy of this environment.
        """
        return copy.deepcopy(self)
