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
This module defines the class for European call problem.
"""


import numpy as np
from scipy.stats import norm

from QFinance.pricing.lognormal import LogNormal
from QFinance.algorithms import SimpleQMC


class EuropeanCallQMC:
    """
    European long call pricing problem using Quantum Monte Carlo.
    """

    def __init__(self, s0: float, k: float, t: float, r: float, sigma: float) -> None:
        """
        :param s0: initial stock price
        :param k: strike price
        :param r: risk-free interest rate
        :param sigma: volatility
        :param t: time to maturity
        :param num_qubits: number of qubits to use
        """
        self.s0_ = s0
        self.k_ = k
        self.t_ = t
        self.r_ = r
        self.sigma_ = sigma
        self.lognormal = None
        self.price_grid = None 
        self.probs = None
        self.sqrt_probs = None
        self.numq = 3 # number of qubits to use
        # self.get_log_normal()
        self.qmc = None
        self.ae_problem = None
        self.method = "MLAE"
        self.accepted_methods = ["MLAE", "IQAE"]
        self.mlae_config = None
        self.iqae_config = None

        self.scaling_ = None
        self.exact_price_ = None
        self.tail_compensation_ = None
        

    def init_check(self) -> None:
        """
        Check that the parameters are valid.
        """
        if self.s0_ <= 0:
            raise ValueError(f'The initial stock price must be positive, but {self.s0_} is given.')
        if self.k_ <= 0:
            raise ValueError(f'The strike price must be positive, but {self.k_} is given.')
        if self.t_ <= 0:
            raise ValueError(f'The time to maturity must be positive, but {self.t_} is given.')
        if self.r_ <= 0:
            raise ValueError(f'The risk-free interest rate must be positive, but {self.r_} is given.')
        if self.sigma_ <= 0:
            raise ValueError(f'The volatility must be positive, but {self.sigma_} is given.')

    def check_method(self) -> None:
        """
        Check that the method is valid.
        """
        if self.method not in self.accepted_methods:
            raise ValueError(f'The method must be in {self.accepted_methods}, but {self.method} is given.')

    def show_info(self):
        """
        Print the relevant information for the option pricing problem.
        """
        print("\nEuropean call option pricing with the following parameters:")
        print(f"current stock price: \t\ts0 = {self.s0}")
        print(f"strike price: \t\t\tk = {self.k}")
        print(f"time to maturity (in years): \tt = {self.t}")
        print(f"risk-free interest rate: \tr = {self.r}")
        print(f"volatility: \t\t\tsigma = {self.sigma}\n")

    @property
    def exact_price(self) -> float:
        """
        calculate the exact price of the option
        """
        if self.exact_price_ is None:
            self.exact_price_ = self.get_exact_price()
        return self.exact_price_


    @property
    def s0(self) -> float:
        """
        :return: initial stock price 
        """
        return self.s0_
    
    @s0.setter
    def s0(self, s0: float) -> None:
        """
        :param s0: initial stock price
        """
        if s0 <= 0:
            raise ValueError(f'The initial stock price must be positive, but {s0} is given.')
        self.s0_ = s0
    
    @property
    def k(self) -> float:
        """
        :return: strike price
        """
        return self.k_
    
    @k.setter
    def k(self, k: float) -> None:
        """
        :param k: strike price
        """
        if k <= 0:
            raise ValueError(f'The strike price must be positive, but {k} is given.')
        self.k_ = k

    @property
    def t(self) -> float:
        """
        :return: time to maturity
        """
        return self.t_

    @t.setter
    def t(self, t: float) -> None:
        """
        :param t: time to maturity
        """
        if t <= 0:
            raise ValueError(f'The time to maturity must be positive, but {t} is given.')
        self.t_ = t

    @property
    def r(self) -> float:
        """
        :return: risk-free interest rate
        """
        return self.r_
    
    @r.setter
    def r(self, r: float) -> None:
        """
        :param r: risk-free interest rate
        """
        if r <= 0:
            raise ValueError(f'The risk-free interest rate must be positive, but {r} is given.')
        self.r_ = r

    @property
    def sigma(self) -> float:
        """
        :return: volatility
        """
        return self.sigma_

    @sigma.setter
    def sigma(self, sigma: float) -> None:
        """
        :param sigma: volatility
        """
        if sigma <= 0:
            raise ValueError(f'The volatility must be positive, but {sigma} is given.')
        self.sigma_ = sigma

    @property
    def tail_compensation(self) -> float:
        """
        :return: tail compensation
        """
        if self.tail_compensation_ is None:
            raise ValueError(f'The tail compensation is not calculated yet.')
        return self.tail_compensation_

    def set_num_qubits(self, num_qubits: int) -> None:
        """
        Set the number of qubits to use.
        :param num_qubits: number of qubits to use
        """
        self.numq = num_qubits
        # update price_grid and sqrt_probs
        self.get_log_normal()

    
    def set_scaling(self, scaling: float) -> None:
        """
        Set the scaling factor for the payoff function.
        :param scaling: the scaling factor
        """
        # check that scaling is in appropriate range
        if scaling <= 1E-3:
            raise ValueError(f'The scaling factor must be greater than 1E-3, but {scaling} is given.')
        if scaling >= 0.5:
            raise ValueError(f'The scaling factor is too large, {scaling} is given.')
        self.scaling_ = scaling

    def get_exact_price(self) -> float:
        """
        Calculate the exact price of the option.
        """
        d1 = (np.log(self.s0 / self.k) + (self.r + 0.5 * self.sigma ** 2) * self.t) / (self.sigma * np.sqrt(self.t))
        d2 = d1 - self.sigma * np.sqrt(self.t)
        return self.s0 * norm.cdf(d1) - self.k * np.exp(-1 * self.r * self.t) * norm.cdf(d2)

    def get_log_normal(self) -> LogNormal:
        """
        Get the desired log-normal distribution, which is the distribution of the stock price.
        sT = s0 * exp((r - 0.5 * sigma ** 2) * t + sigma * sqrt(t) * Z)
        sT ~ LogNormal((r - 0.5 * sigma ** 2) * t, sigma * sqrt(t))
        """
        LNmu = (self.r_ - 0.5 * self.sigma_ ** 2) * self.t_ + np.log(self.s0_)
        LNsigma = self.sigma_ * np.sqrt(self.t_)
        self.lognormal = LogNormal(LNmu, LNsigma)
        self.lognormal.set_num_sample_qubits(self.numq)

        price_grid, self.probs = self.lognormal.discrete_pdf()

        # calculate the tail compensation
        smin = price_grid[0]
        smax = price_grid[-1]
        self.tail_compensation_ = 1 - self.lognormal.cdf(smax)
        # print(f"price grid is {price_grid}")
        # print(f"probs are {self.probs}")
        # price_grid, self.probs = self.lognormal.discrete_pdf_slanted(self.k)
        self.price_grid = price_grid
        self.sqrt_probs = np.sqrt(self.probs)
        return self.lognormal


    def calc_grid_expectation(self) -> float:
        """
        Calculate the theoretical (grid coarse grained) expectation of the payoff function.
        :return: the expectation
        """
        payoff = np.maximum(self.price_grid - self.k_, 0)
        grid_expectation = np.sum(payoff * self.probs)
        return grid_expectation
    

    def calc_grid_P1(self) -> float:
        """
        Calculate the theoretical probability P1 which will be compared against the measured amplitude.
        :return: the probability
        """
        s = self.qmc.pwl.scaling_
        ymin = self.qmc.pwl.ymin
        ymax = self.qmc.pwl.ymax
        grid_expectation = self.calc_grid_expectation()
        slope = 2 * s / (ymax - ymin)
        intercept = 1 / 2 - s * ( 2 * ymin / (ymax - ymin) + 1)
        # grid_P1 = 2 * s / (ymax - ymin) * grid_expectation + 1 / 2 - s * ( 2 * ymin / (ymax - ymin) + 1)
        grid_P1 = slope * grid_expectation + intercept
        print(f"The linear transform is P1 = {slope:.5e} * Exp + {intercept:.5e}.\n")
        return grid_P1


    def reduce_to_aep(self) -> float:
        """
        Reduce the European call problem to amplitude estimation problem.
        :return: the option price
        """
        # step1: create the QMC object
        self.qmc = SimpleQMC(self.numq)

        # step2: load the LogNormal distribution
        dist = self.sqrt_probs
        self.qmc.load_dist(dist)

        # step3: set the payoff function
        price_min = self.price_grid[0]
        price_max = self.price_grid[-1]
        domain = (price_min, price_max)
        # check that the strike price is within the domain of the price grid
        assert self.k_ >= price_min and self.k_ <= price_max, "The strike price is out of the domain of the price grid."
        self.qmc.set_linear(domain, self.k_)
        if self.scaling_ is not None:
            self.qmc.set_scaling(self.scaling_)

        # duplicate: already done in self.qmc.run_mlae
        # # step4: amplitude estimation
        # self.ae_problem = self.qmc.create_AEProblem()


    def get_price(self) -> float:
        """
        Get the option price e^{-r*T} * E[max(0, sT - k)]
        :return: the option price
        """
        if self.ae_problem is None:
            self.reduce_to_aep()

        if self.method == "MLAE":
            self.measured_expectation = self.qmc.run_mlae_demo()
        elif self.method == "IQAE":
            self.measured_expectation = self.qmc.run_iqae()
        self.measured_P1 = self.qmc.measured_P1
        self.measured_price = np.exp(-self.r_ * self.t_) * self.measured_expectation

        return self.measured_price
    

    def get_price_mlae(self, Q_powers: list[int], shots: list[int], precision: float = 1E-4) -> float:
        """
        Get the option price e^{-r*T} * E[max(0, sT - k)]
        :return: the option price
        """
        if self.ae_problem is None:
            self.reduce_to_aep()

        self.measured_expectation = self.qmc.run_mlae(Q_powers, shots, precision)
        
        self.measured_P1 = self.qmc.measured_P1
        self.measured_price = np.exp(-self.r_ * self.t_) * self.measured_expectation

        return self.measured_price
    

    def get_price_and_error(self) -> tuple[float, float]:
        """
        Get the option price and the error.
        :return: the option price and the error
        """
        self.get_price()

        self.expectation_random_error = self.qmc.expectation_random_error

        return self.measured_price, np.exp(-self.r_ * self.t_) * self.expectation_random_error
    

    def get_price_and_error_mlae(self, Q_powers: list[int], shots: list[int], precision: float = 1E-4) -> tuple[float, float]:
        """
        Get the option price and the error.
        The option price is manually compensated by the system error.
        :return: the compensated option price and the error
        """
        self.get_price_mlae(Q_powers, shots, precision)

        self.expectation_random_error = self.qmc.expectation_random_error
        price_random_error_radius = np.exp(-self.r_ * self.t_) * self.expectation_random_error

        # grid_expectation = self.calc_grid_expectation()
        # grid_price = np.exp(-self.r_ * self.t_) * grid_expectation
        # self.price_system_error = self.exact_price - grid_price

        self.compensated_price = self.measured_price + self.tail_compensation

        # price_error_radius = price_random_error_radius + price_system_error_radius
        
        return self.compensated_price, price_random_error_radius
    

    def print_error_info(self):
        """
        print the debug information after the calculation
        """
        measured_expectation = self.measured_expectation
        measured_P1 = self.measured_P1

        grid_expectation = self.calc_grid_expectation()
        grid_P1 = self.calc_grid_P1()
        grid_price = np.exp(-self.r_ * self.t_) * grid_expectation
        # print(f"grid price: \t\t{grid_price:.5e}")
        # print(f"measured price: \t{self.measured_price:.5e}")

        P1_random_error = abs(grid_P1 - measured_P1) / grid_P1
        # print(f"grid expectation: \t{grid_expectation:.5e}")
        # print(f"measured expectation: \t{measured_expectation:.5e}")
        expectation_relative_error_random = abs(grid_expectation - measured_expectation) / grid_expectation
        # expectation_relative_error_overall = abs(expectation_theoretical - measured_expectation) / expectation_theoretical

        random_error_amplification_ratio = expectation_relative_error_random / P1_random_error

        # print the relative error in percentage
        print(f"Random error of P1: \t{P1_random_error * 100:.3f}%", "(from amplitude estimation)")
        print(f"Random error of Exp: \t{expectation_relative_error_random * 100:.3f}%")
        print(f"Amplification ratio: \t{random_error_amplification_ratio:.2f}\n")

        # if self.measured_price is not None:
        #     price_qmc = self.measured_price
        #     price_overall_error = abs(self.exact_price - price_qmc) / self.exact_price
        #     price_random_error = abs(grid_price - price_qmc) / grid_price
        #     print(f"Random error of option price: \t{price_random_error * 100:.3f}%")
        #     print(f"Overall error of option price: \t{price_overall_error * 100:.3f}%")

        if self.compensated_price is not None:
            price_overall_error = abs(self.exact_price - self.compensated_price) / self.exact_price
            print(f"Overall error of option price: \t{price_overall_error * 100:.3f}%")