from typing import Union

import numpy as np
import torch
from gym.spaces import Box


def signlog(target):
    """
    This function can be applied on the critic target to help convergence.
    It scales down the critic target value, so it's no more necessary to normalise the reward.
    This function is similar to a Tanh, but it is not bounded between -1 and 1, so when the target q-value is high,
    signlog(target) can still be different enough from signlog(target - 1).

    usage:
    self.critic(state, action,

    """
    return torch.sign(target) * torch.log(target + 1)


def scale_tensor(data: Union[np.ndarray, torch.Tensor], input_space: Box, output_space: Box):
    """
    Scale an action within the given bounds action_low to action_high, to our action_space.
    The result action is also clipped to fit in the action space in case the given action wasn't exactly inside
    the given bounds.
    Useless if our action space is discrete.
    @return: scaled and clipped actions. WARNING: actions are both attribute and result. They are modified by the
    function. They are also returned for better convenience.
    """
    assert isinstance(data, (np.ndarray, torch.Tensor))
    assert isinstance(input_space, Box)
    assert isinstance(output_space, Box)

    source_low, source_high = input_space.low, input_space.high
    target_low, target_high = output_space.low, output_space.high
    if isinstance(data, torch.Tensor):
        source_low, source_high = torch.tensor(input_space.low), torch.tensor(source_high)
        target_low, target_high = torch.tensor(target_low), torch.tensor(target_high)

    # Scale action to the action space
    source_range = source_high - input_space.low
    target_range = target_high - target_low

    scale = target_range / source_range
    data = data * scale
    data = data + (target_low - (input_space.low * scale))
    clip_fun = np.clip if isinstance(data, np.ndarray) else torch.clamp
    data = clip_fun(data, target_low, target_high)
    return data
