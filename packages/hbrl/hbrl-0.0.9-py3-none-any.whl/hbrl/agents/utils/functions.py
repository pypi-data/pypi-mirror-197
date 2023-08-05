import torch


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
