import abc
from abc import ABC
from typing import Union

import numpy as np
from gym.spaces import Box, Discrete
from hbrl.environments.environment import Environment


class GoalReachingEnv(Environment, ABC):

    name = ""

    def __init__(self, wrapped_environment, goal_space: Union[None, Box, Discrete]=None,
                 sparse_reward=True, reachability_threshold=1):
        assert isinstance(wrapped_environment, Environment)
        self.wrapped_environment = wrapped_environment
        self.goal_space = self.state_space if goal_space is None else goal_space
        assert isinstance(self.goal_space, (Box, Discrete))
        if isinstance(self.goal_space, Box):
            if isinstance(reachability_threshold, list):
                reachability_threshold = np.array(reachability_threshold)
            if isinstance(reachability_threshold, np.ndarray):
                assert self.reachability_threshold.shape[0] == self.goal_size
            self.reachability_threshold = reachability_threshold
        self.sparse_reward = sparse_reward
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
        return self.goal_space.sample()

    def reset(self):
        self.wrapped_environment.reset()
        self.goal = self.sample_goal()
        return self.state, self.goal

    def step(self, action):
        state, reward, done = self.wrapped_environment.step(action)
        if done:
            return state, reward, done

        if self.reached(state):
            return state, 0, True
        else:
            reward = self.reward(state, action)
            return state, reward, False

    def reached(self, state, goal=None) -> bool:
        if goal is None:
            goal = self.goal
        state_goal = self.get_goal_from_state(state)
        if isinstance(self.goal_space, Discrete):
            return state_goal == goal
        elif isinstance(self.reachability_threshold, np.ndarray):
            return (np.abs(state_goal - goal) <= self.reachability_threshold).all()
        else:
            return np.linalg.norm(state_goal - goal) <= self.reachability_threshold

    def reward(self, state, action, goal=None):
        goal = self.goal if goal is None else goal

        if self.sparse_reward:
            return 0 if self.reached(state, goal) else -1
        else:
            state_goal = self.get_goal_from_state(state)
            return - np.linalg.norm((state_goal - goal))

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