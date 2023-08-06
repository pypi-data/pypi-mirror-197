import torch
from torch.distributions.normal import Normal


class UniformTorch(torch.distributions.uniform.Uniform):
    """
       For testing Likelihood Ratio.
    """

    def __init__(self, lower, upper):
        super(UniformTorch, self).__init__(lower, upper)

    def log_prob(self, sample):
        return super(UniformTorch, self).log_prob(sample).mean()
