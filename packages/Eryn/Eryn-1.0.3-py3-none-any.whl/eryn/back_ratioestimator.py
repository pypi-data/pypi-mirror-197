import torch
from torch import nn
from torch.nn import functional as F

import numpy as np
from nets import MLP

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


class RatioEstimator(nn.Module):
    """
       Performs estimation of the likelihood-to-evidence ratio.
    """

    def __init__(self, param_size, context_size, hidden_sizes):
        super(RatioEstimator, self).__init__()

        self.estimate = MLP(
            param_size + context_size,
            hidden_sizes,
            1,
            act_func=F.elu,
            activate_output=False,
        )

    def forward(self, inputs, outputs):

        log_ratios = self.log_ratio(inputs, outputs)

        return log_ratios, log_ratios.sigmoid()

    def log_ratio(self, inputs, outputs):

        z = torch.cat([inputs, outputs], dim=1)

        return self.estimate(z)

