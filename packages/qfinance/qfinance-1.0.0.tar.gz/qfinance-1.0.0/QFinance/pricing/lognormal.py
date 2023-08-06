#!/usr/bin/python3
# -*- coding: utf8 -*-

# Copyright (c) 2022 Baidu, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
This module defines the LogNormal distribution class and related functions.
"""

import numpy as np
from scipy.stats import norm

class LogNormal:
    """
    This class defines the LogNormal distribution.
    """
    def __init__(self, mu, sigma):
        """
        Initialize the LogNormal distribution.
        X ~ LogNormal(mu, sigma) is often written as X ~ exp(mu + sigma * Z), where Z ~ N(0, 1).
        
        mu (float): The mean of the distribution.
        sigma (float): The standard deviation of the distribution.
        """
        self.mu_ = mu
        self.sigma_ = sigma
        self.num_sample_qubits_ = None
        self.num_grid_points_ = 0
        self.cutoff_min_ = np.maximum(0.0, self.mean - 3 * self.stddev)
        self.cutoff_max_ = self.mean + 3 * self.stddev

    def set_num_sample_qubits(self, num_sample_qubits):
        """
        Set the number of sample qubits.
        """
        self.num_sample_qubits_ = num_sample_qubits
        self.num_grid_points_ = 2 ** num_sample_qubits
    
    def sample(self, num_samples = 10000):
        """
        Sample from the LogNormal distribution.

        Args:
            num_samples (int): The number of samples.

        Returns:
            numpy.ndarray: The samples.
        """
        return np.exp(self.mu_ + self.sigma_ * np.random.randn(num_samples))

    @property
    def cutoff_min(self) -> float:
        """
        The minimum value used in discrete probability distribution.
        """
        return self.cutoff_min_
    
    @cutoff_min.setter
    def cutoff_min(self, cutoff_min: float):
        """
        Set the minimum value used in discrete probability distribution.
        """
        self.cutoff_min_ = cutoff_min
    
    @property
    def cutoff_max(self) -> float:
        """
        The maximum value used in discrete probability distribution.
        """
        return self.cutoff_max_
    
    @cutoff_max.setter
    def cutoff_max(self, cutoff_max: float):
        """
        Set the maximum value used in discrete probability distribution.
        """
        self.cutoff_max_ = cutoff_max

    def discrete_pdf(self):
        """
        Calculate the discrete probability distribution.
        """
        grid = np.linspace(self.cutoff_min, self.cutoff_max, self.num_grid_points_)
        prob = self.pdf(grid)
        # Normalize the probability distribution, so that the sum of the probabilities is 1.
        prob /= np.sum(prob)
        return grid, prob
    

    def discrete_pdf_slanted(self, K: float):
        """
        Calculate the discrete pdf function customized for max{S-K, 0}.
        Accumulate the probability mass of the grid points that are smaller than K.
        """
        self.cutoff_min = max(K - self.stddev, 0)
        self.cutoff_max = self.cutoff_min + 6 * self.stddev
        grid = np.linspace(self.cutoff_min, self.cutoff_max, self.num_grid_points_)
        prob = [0] * self.num_grid_points_

        prob[0] = self.cdf(self.cutoff_min)
        # Calculate the probability of the grid points that are larger than K.
        for i in range(1, self.num_grid_points_):
            prob[i] = self.cdf(grid[i]) - self.cdf(grid[i - 1])
        
        # Normalize the probability distribution, so that the sum of the probabilities is 1.
        prob /= np.sum(prob)
        return grid, prob

    

    def pdf(self, x):
        """
        Calculate the probability density function of the distribution.

        Args:
            x (float): The value of the random variable.
        """
        return np.exp(-0.5 * ((np.log(x) - self.mu_) / self.sigma_) ** 2) / (x * self.sigma_ * np.sqrt(2 * np.pi))

    def cdf(self, x):
        """
        Calculate the cumulative density function of the distribution.

        Args:
            x (float): The value of the random variable.

        Returns:
            float: The cumulative density function of the distribution.
        """
        return norm.cdf((np.log(x) - self.mu_) / self.sigma_)

    def inv_cdf(self, p):
        """
        Calculate the inverse cumulative density function of the distribution.

        Args:
            p (float): The probability.

        Returns:
            float: The inverse cumulative density function of the distribution.
        """
        return np.exp(self.mu_ + self.sigma_ * norm.ppf(p))

    @property
    def mean(self):
        """
        Calculate the mean of the distribution.

        Returns:
            float: The mean of the distribution.
        """
        return np.exp(self.mu_ + 0.5 * self.sigma_ ** 2)

    @property
    def variance(self):
        """
        Calculate the variance of the distribution.

        Returns:
            float: The variance of the distribution.
        """
        return (np.exp(self.sigma_ ** 2) - 1) * np.exp(2 * self.mu_ + self.sigma_ ** 2)

    @property
    def stddev(self):
        """
        Calculate the standard deviation of the distribution.

        Returns:
            float: The standard deviation of the distribution.
        """
        return np.sqrt(self.variance)

    @property
    def skewness(self):
        """
        Calculate the skewness of the distribution.

        Returns:
            float: The skewness of the distribution.
        """
        return (np.exp(self.sigma_ ** 2) + 2) * np.sqrt(np.exp(self.sigma_ ** 2) - 1)