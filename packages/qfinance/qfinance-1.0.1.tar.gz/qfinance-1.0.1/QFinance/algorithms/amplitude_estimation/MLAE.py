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
This module implements the Maximum Likelihood Amplitude Estimation algorithm.
Reference: http://arxiv.org/abs/1904.10246
"""

import numpy as np
import scipy.special
import time

from QCompute import *
from copy import deepcopy

from QFinance.utils import sub_qreg, full_qreg
from QFinance.algorithms.amplitude_estimation.AE_problem import AEProblem



class MLAE:
    """
    The Maximum Likelihood Amplitude Estimation class.
    """

    def __init__(self, problem: AEProblem):
        """
        Initialize the MLAE class.
        :param problem: the amplitude estimation problem
        :param num_qubits: number of qubits that operator Q acts on
        :param Q_power_list: the chosen set of Q powers, {m_k} in the paper
        :param shots_list: the number of shots for each Q power, {N_k} in the paper
        """
        self.problem = problem
        self.num_qubits_ = problem.num_qubits

        # the number of terms in the likelihood function
        # equal to M + 1 in the paper
        self.num_terms_ = 10

        # list of Q powers, {m_0, m_1, ..., m_M} in the paper
        self.Q_power_list = []
        # list of number of shots for each Q power, {N_0, N_1, ..., N_M} in the paper
        self.shots_list = []

        # used to store the list of measured 1s in each shot, 
        # {h_0, h_1, ..., h_M} in the paper
        self.heads_list = []

        # because a = sin^2(theta_a), the interval to search for optimal theta_a can be taken to be [0, pi/2]
        # but when theta = 0 or pi/2, sin(theta) = 0,
        # and the corresponding log-likelihood function is ill-defined
        # so we need to exclude these two points
        theta_min = 0 + 10 ** (-4)
        theta_max = np.pi / 2 - 10 ** (-4)
        # self.theta_range = [0, np.pi / 2]
        self.theta_range = [theta_min, theta_max]

        self.estimated_amp = 0
        self.estimated_theta = 0
        # the estimation precision of a
        self.epsilon = 10 ** (-4)

        self.num_queries_ = None
        self.fisher_info_ = None

    @property
    def num_qubits(self):
        """
        Return the number of qubits.
        """
        return self.num_qubits_

    @property
    def num_terms(self):
        """
        Return the number of terms in the likelihood function.
        num_terms = M + 1 in the paper
        """
        return self.num_terms_

    @num_terms.setter
    def num_terms(self, M):
        """
        Set the number of terms in the likelihood function.
        """
        self.num_terms_ = M
    
    def set_grid_precision(self, epsilon):
        """
        Set the estimation precision of a.
        """
        self.epsilon = epsilon

    def check_parameters_before_run(self):
        """
        Check whether the parameters are valid before running the algorithm.
        """
        assert self.num_qubits > 0, "The number of qubits must be positive."
        assert len(self.Q_power_list) == len(self.shots_list), \
            "The number of Q powers and the number of shots must be the same."
        assert len(self.Q_power_list) == self.num_terms_, \
            "The number of Q powers and the number of terms must be the same."

    def check_parameters_after_run(self):
        """
        Check whether the parameters are valid after running the algorithm.
        """
        assert len(self.heads_list) == len(self.Q_power_list), \
            "The number of measured heads and the number of Q powers must be the same."
        for i in range(len(self.heads_list)):
            assert self.heads_list[i] <= self.shots_list[i], \
                "The number of measured heads cannot be greater than the number of shots."
            assert self.heads_list[i] >= 0, "The number of measured heads cannot be negative."

    def setup_linear_scheme(self, n_shots: int) -> None:
        """
        Set up the linear scheme for the MLAE algorithm.
        In the linear scheme, the Q powers are chosen to be m_k = k
        m_0 = 0, m_1 = 1, ..., m_M = M
        while the number of shots for each Q power are chosen to be N_k = n_shots
        """
        # first, check that num_terms_ is valid
        assert self.num_terms_ > 0, "The number of terms must be positive."
        self.Q_power_list = [i for i in range(self.num_terms_)]
        self.shots_list = [n_shots for i in range(self.num_terms_)]

    def setup_exponential_scheme(self, n_shots: int) -> None:
        """
        Set up the exponential scheme for the MLAE algorithm.
        In the exponential scheme, the Q powers are chosen to be m_k = 2^{k-1}
        m_0 = 0, m_1 = 1, ..., m_M = 2^{M-1}
        while the number of shots for each Q power are chosen to be N_k = n_shots
        """
        # first, check that num_terms_ is valid
        assert self.num_terms_ > 0, "The number of terms must be positive."
        self.Q_power_list = [2 ** (i - 1) for i in range(1, self.num_terms_)]
        self.Q_power_list.insert(0, 0)
        self.shots_list = [n_shots for i in range(self.num_terms_)]

    def setup_arbitrary_scheme(self, Q_power_list: list[int], shots_list: list[int]) -> None:
        """
        Set up the arbitrary scheme for the MLAE algorithm.
        In the arbitrary scheme, the Q powers and the number of shots for each Q power
        are chosen arbitrarily.
        """
        assert len(Q_power_list) == len(shots_list), \
            "The number of Q powers and the number of shots must be the same."
        self.num_terms = len(Q_power_list)
        # in case the user gives a numpy array instead of a list
        self.Q_power_list = list(Q_power_list)
        self.shots_list = list(shots_list)


    def run(self):
        """
        step 1. Run the MLAE algorithm.
        step 2. calculate the optimal theta_a.
        """
        self.check_parameters_before_run()
        print("\n=================== Running MLAE algorithm ======================")
        print("powers of Q are:", self.Q_power_list)
        print("number of shots are:", self.shots_list)

        for k in range(self.num_terms_):
            # print(f"\niteration {k} of {self.num_terms_ - 1}...")
            m_k = self.Q_power_list[k]
            N_k = self.shots_list[k]
            h_k = self.measure_Qm(m_k, N_k)
            self.heads_list.append(h_k)
        self.check_parameters_after_run()
        print("===================== MLAE algorithm finished. ====================\n")

        # calculate the optimal theta_a from the measured {h_0, h_1, ..., h_M}
        self.estimated_theta, log_likelihood = self.calc_optimal_theta()
        self.estimated_amp = np.sin(self.estimated_theta) ** 2
        self.calc_fisher_information(self.estimated_amp)
        self.calc_num_oracle_queries()

    def measure_Qm(self, m: int, N: int) -> int:
        """
        Apply operator Q^k to the state |0>^num_qubits and measure the last qubit.
        Return the number of 1s in the sample.
        k: the power of Q. Note that k must be non-negative integer.
        N: the number of shots.
        """
        if m < 0:
            raise ValueError(f"Power k must be non-negative integer, but {m} is given.")
        if N <= 0:
            raise ValueError(f"Number of shots num must be positive integer, but {N} is given.")
        
        # intialize the environment
        env = QEnv()
        # TODO: provide different backends
        env.backend(BackendName.LocalBaiduSim2)
        q = env.Q
        q.createList(self.num_qubits)
        envA = deepcopy(self.problem.envA)
        opA = envA.convertToProcedure("opA", env)()
        envQ = deepcopy(self.problem.envQ)
        opQ = envQ.convertToProcedure("opQ", env)()

        print(f"\nApplying Q^{m} to the state A|0>^{self.num_qubits}...")
        tic = time.perf_counter()
        # apply Q^k to the state |psi> = A|0>^n
        opA(*full_qreg(q))
        for _ in range(m):
            opQ(*full_qreg(q))
        
        # measure the last qubit
        MeasureZ([q[self.num_qubits - 1]], [0])
        taskResult = env.commit(N)
        counts_dict = taskResult['counts']
        
        toc = time.perf_counter()
        print(f"Time elapsed: {toc - tic:0.4f} seconds.")

        num_0 = counts_dict.get("0", 0)
        num_1 = counts_dict.get("1", 0)
        # TODO: deal with the case when num_0 + num_1 < N

        h = num_1
        return h

    def log_likelihood_single_term(self, h: int, theta: float, m: int, N: int) -> float:
        """
        Calculate the log likelihood function log L_k(h_k; theta_a)
        :param h: the number of measured 1s in N measurements
        :param theta: the parameter theta
        :param m: the power of Q
        :param N: the number of shots
        :return: the log likelihood of a single term in the likelihood function
        """ 
        # deal with the case where theta = 0 or pi/2
        # the log likelihood function is not defined when theta = 0
        # TODO: the best practice is to preclude this case in the theta_range
        # if theta == 0:
        #     if h == 0:
        #         return 0
        #     else:
        #         return -np.inf
        # # the log likelihood function is not defined when theta = pi/2
        # if theta == np.pi / 2:
        #     if h == N:
        #         return 0
        #     else:
        #         return -np.inf
        amplified_angle = (2 * m + 1) * theta
        l1 = np.log(np.sin(amplified_angle) ** 2)
        l2 = np.log(np.cos(amplified_angle) ** 2)
        return h * l1 + (N - h) * l2

    def log_likelihood_total(self, theta: float) -> float:
        """
        Calculate the total log likelihood function log L(theta_a)
        :return: the total log likelihood
        """
        log_likelihood = 0
        for i in range(self.num_terms_):
            log_likelihood += self.log_likelihood_single_term(self.heads_list[i],
                                                              theta,
                                                              self.Q_power_list[i],
                                                              self.shots_list[i])
        return log_likelihood

    def calc_optimal_theta(self) -> tuple:
        """
        Calculate the optimal theta_a from log L(theta_a)
        :return: the optimal theta_a and the corresponding log likelihood
        """
        theta_min, theta_max = self.theta_range
        num_grid = (theta_max - theta_min) / self.epsilon
        num_grid = int(np.floor(num_grid))
        theta_grid = np.linspace(theta_min, theta_max, num_grid)
        log_likelihoods = self.log_likelihood_total(theta_grid)
        place = np.argmax(log_likelihoods)
        optimal_theta = theta_grid[place]
        max_likelihood = log_likelihoods[place]
        return (optimal_theta, max_likelihood)

    def calc_num_oracle_queries(self):
        """
        Return the number of oracle queries.
        """
        num = 0
        for k in range(self.num_terms_):
            m_k = self.Q_power_list[k]
            N_k = self.shots_list[k]
            num += (2 * m_k + 1) * N_k
            #num += (2 * self.Q_power_list[k] + 1) * self.shots_list[k]
        self.num_queries_ = num

    def calc_fisher_information(self, a: float):
        """
        Return the Fisher information w.r.t. the parameter a.
        """
        fisher = 0
        for k in range(self.num_terms_):
            m_k = self.Q_power_list[k]
            N_k = self.shots_list[k]
            fisher += (2 * m_k + 1) ** 2 * N_k
        fisher = fisher / (a * (1 - a))
        self.fisher_info_ = fisher

    def estimated_error(self) -> float:
        """
        Return the approximate estimation error,
        calculated from the Fisher information.
        """
        error = 0
        for k in range(self.num_terms_):
            m_k = self.Q_power_list[k]
            N_k = self.shots_list[k]
            error += (2 * m_k + 1) ** 2 * N_k
        return 1 / np.sqrt(error)