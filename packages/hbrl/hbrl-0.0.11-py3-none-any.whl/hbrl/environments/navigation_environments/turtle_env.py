"""
This environment simulate a turtle bot behaviour.
"""
import math
import time

import numpy as np
from hbrl.environments.navigation_environment import NavigationEnv, MapsIndex, GoalReachingNavEnv
from gym.spaces import Box
from math import pi


class TurtleEnv(NavigationEnv):

    name = "TurtleEnv"

    def __init__(self, map_tag: MapsIndex = MapsIndex.EMPTY):
        state_space = Box(low=np.array([-pi, -2, -2]), high=np.array([pi, 2, 2]))
        actions_bounds = np.array([0.2, 1])
        action_space = Box(low=-actions_bounds, high=actions_bounds)
        super().__init__(map_tag, state_space, action_space)

    def __getattr__(self, item):
        if item.startswith("_"):
            raise AttributeError(f"accessing private attribute '{item}' is prohibited")

    def reset(self):
        """
        Publish a bool message on reset topic
        :return:
        """
        self.state = super().reset()
        self.state[-1] = 0
        return self.state

    def step(self, action):
        action = np.clip(action, self.action_space.low, self.action_space.high)
        num_sub_steps = 10
        dt = 1.0 / num_sub_steps
        for _ in np.linspace(0, 1, num_sub_steps):
            # Compute new_orientation

            self.state[3] += dt * action[0] / 2  # New angular velocity
            self.state[3] = np.clip(self.state[3], self.action_space.low[0], self.action_space.high[0])
            self.state[2] += self.state[3]  # New orientation
            if self.state[2] > pi:
                self.state[2] -= 2 * pi
            elif self.state[2] < - pi:
                self.state[2] += 2 * pi

            linear_velocity = np.clip(self.state[4] + dt * action[1],
                                      self.action_space.low[1], self.action_space.high[1])  # New linear velocity
            new_state = self.state.copy()
            new_state[0] += math.cos(self.state[2]) * linear_velocity
            new_state[1] += math.sin(self.state[2]) * linear_velocity

            if self.reachable(new_state):
                self.state = new_state

            self.state[3] += dt * action[0] / 2  # New angular velocity
            self.state[3] = np.clip(self.state[3], self.action_space.low[0], self.action_space.high[0])
            self.state[2] += self.state[3]  # New orientation
            if self.state[2] > pi:
                self.state[2] -= 2 * pi
            elif self.state[2] < - pi:
                self.state[2] += 2 * pi

        return self.state, *super().get_reward_done(self.state)


class GCTurtleEnv(GoalReachingNavEnv):

    name = "GoalConditionedTurtleEnv"

    def __init__(self, map_tag: MapsIndex = MapsIndex.EMPTY, sparse_reward=True):
        turtle_env = TurtleEnv(map_tag)
        goal_space = Box(low=turtle_env.state_space.low[:2], high=turtle_env.state_space.high[:2])
        super().__init__(turtle_env, goal_space=goal_space, sparse_reward=sparse_reward)

    def get_goal_from_state(self, state):
        """
        Apply a projection P: S -> G on the given state
        """
        return state[:2].copy()

    def get_state_from_goal(self, goal):
        """
        Apply a \bar{P}:G -> S projection on the given state
        """
        return np.concatenate((goal, np.zeros(1)))
